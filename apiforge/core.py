import requests
import time
from concurrent.futures import ThreadPoolExecutor
from tenacity import retry, stop_after_attempt, wait_fixed, stop_after_delay, retry_if_exception_type, RetryError
from typing import Dict, Any, Optional, List, Union, Tuple
from .config import ConfigParser
from .reporter import Reporter
from .utils import validate_response
from .generator import TestGenerator

class APIForge:
    def __init__(self, base_url: str, auth: Optional[Dict[str, Any]] = None, max_workers: int = 10):
        self.base_url = base_url.rstrip('/')
        self.auth = auth or {}
        self._session = requests.Session()
        self.max_workers = max_workers

    @classmethod
    def from_config(cls, config: Union[str, Dict[str, Any]], env: str = "Prod") -> 'APIForge':
        config_data = ConfigParser.load_config(config, env)
        return cls(config_data.get("base_url", ""), config_data.get("auth"))
    
    # Retry 3 times, with a 2 second delay in between and stop execution after 15 seconds with no response 
    @retry(
    stop=stop_after_delay(15) | stop_after_attempt(3),
    wait=wait_fixed(2),
    retry=(retry_if_exception_type(requests.ConnectionError) | retry_if_exception_type(requests.Timeout))
    )
    def send_request(self, url: str, method: str, params: Dict[str, Any] = {}, expected_status: int = 200, **kwargs) -> Dict[str, Any]:
        method = str.upper(method)
        response = self._session.request(method, url, params=params, **self.auth, **kwargs)
        if response.status_code == 404: raise ValueError(f"Endpoint not found: {response.status_code}")
        if response.status_code != expected_status: raise AssertionError(f"Expected {expected_status}, got {response.status_code}: {response.text}")
        try:
            result = response.json()
        except ValueError as e:
            raise ValueError(f"Failed to parse JSON response: {e}")
        return result

    def run_test(self, method: str, endpoint: str, params: Dict[str, Any] = {}, expected_status: int = 200, expected_keys: Optional[Union[List[str], Tuple[str]]] = None,  **kwargs) -> Dict[str, Any]:
        params = params.copy()
        formatted_endpoint = endpoint
        for param_name in list(params.keys()):
            placeholder = f"{{{param_name}}}"
            if placeholder in formatted_endpoint:
                formatted_endpoint = formatted_endpoint.replace(placeholder, str(params[param_name]))
                del params[param_name]  # Remove path parameter from params to avoid sending as query param
        url = f"{self.base_url}/{formatted_endpoint.lstrip('/')}"
        valid_methods = ["PUT", "DELETE", "GET", "POST", "PATCH"]
        if not isinstance(method, str): raise TypeError("Expected method to be a str")
        if str.upper(method) not in valid_methods: raise ValueError(f"Invalid HTTP method passed. Recieved {method} but accepted HTTP methods are {valid_methods}")
        reporter = kwargs.pop("reporter", None)
        try:
            result = self.send_request(url=url, method=method, params=params, expected_status=expected_status, **kwargs)
            if expected_keys is not None and not validate_response(result, expected_keys): raise AssertionError("Response validation failed: missing expected keys")
            if reporter:
                test_config = {"method": method, "endpoint": endpoint, "params": params}
                reporter.log_api_result(test=test_config, result=result, success=True)
            return result
        except RetryError as e:
            # Wrap tenacity.RetryError in RuntimeError
            original_exception = e.last_attempt.exception() if e.last_attempt else e
            if reporter: reporter.log_api_result(test={"method": method, "endpoint": formatted_endpoint, "params": params}, result=original_exception, success=False)
            raise RuntimeError(f"API request failed after retries: {str(original_exception)}") from e 
        except requests.RequestException as e:
            if reporter: reporter.log_api_result(test={"method": method, "endpoint": formatted_endpoint, "params": params}, result=e, success=False)
            raise RuntimeError(f"API request failed after retries: {str(e)}")
        except ValueError as e:
            if reporter: reporter.log_api_result(test={"method": method, "endpoint": formatted_endpoint, "params": params}, result=e, success=False)
            raise RuntimeError(f"API error: {str(e)}")
        except AssertionError as e:
            if reporter: reporter.log_api_result(test={"method": method, "endpoint": formatted_endpoint, "params": params}, result=e, success=False)
            raise RuntimeError(f"API test failed: {str(e)}")
        
    def run_config_tests(self, config: Union[str, Dict[str, Any]], env: str = "prod", reporter: Optional[Reporter] = None) -> list[Dict[str, Any]]:
        config_data = ConfigParser.load_config(config, env)
        results = []
        for endpoint in config_data["endpoints"]:
            try:
                result = self.run_test(
                    method=endpoint["method"],
                    endpoint=endpoint["path"],
                    params=endpoint.get("params", {}),
                    expected_status=endpoint["expected_status"],
                    json=endpoint.get("payload"),
                    reporter=reporter,
                    expected_keys=endpoint.get("expected_keys")
                )
                results.append(result)
            except RuntimeError as e:
                if reporter:
                    test_config = {
                        "method": endpoint["method"],
                        "endpoint": endpoint["path"],
                        "params": endpoint.get("params", {})
                    }
                    reporter.log_api_result(test_config, None, False, str(e))
                results.append({"error": str(e)})
        return results

    def _run_test_task(self, endpoint, reporter):
        test_config = {
            "method": endpoint["method"],
            "endpoint": endpoint["path"],
            "params": endpoint.get("params", {}),
            "expected_status": endpoint["expected_status"],
            "expected_keys": endpoint.get("expected_keys", [])
        }
        try:
            result = self.run_test(
                method=endpoint["method"],
                endpoint=endpoint["path"],
                params=endpoint.get("params", {}),
                expected_status=endpoint["expected_status"],
                expected_keys=endpoint.get("expected_keys"),
                json=endpoint.get("payload"),
                reporter=reporter
            )
            return result, True
        except RuntimeError as e:
            return {"error": str(e)}, False
    
    def run_generated_tests(self, spec: Union[str, Dict[str, Any]], reporter: Optional[Reporter] = None) -> List[Dict[str, Any]]:
        generator = TestGenerator()
        if reporter: reporter.log_generic_output(output=f"Starting generated tests with spec: {spec}", method="APIForge::run_generated_tests")
        try:
            endpoints = generator.generate_tests(spec)
            if reporter: reporter.log_generic_output(output=f"Generated {len(endpoints)} test endpoints", method="APIForge::run_generated_tests")
        except RuntimeError as e:
            if reporter: reporter.log_error(method="APIForge::run_generated_tests", error=e)
            raise RuntimeError(f"Failed to generate tests: {str(e)}")
        
        results = []
        success_count = 0
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [executor.submit(self._run_test_task, endpoint, reporter) for endpoint in endpoints]
                for future in futures:
                    result, success = future.result()
                    results.append(result)
                    if success: success_count += 1

        if reporter:
            elapsed_time = time.time() - start_time
            reporter.log_generic_output(
                        output=
                        f"Completed {len(endpoints)} tests: {success_count} passed, "
                        f"{len(endpoints) - success_count} failed in {elapsed_time:.2f} seconds",
                        method="APIForge::run_generated_tests"
                    )
        
        return results
    
    # @contextmanager
    # def get_session(self):
    #     with self._lock:
    #         session = self._session
    #         try: yield session
    #         finally: session.close()