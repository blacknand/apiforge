import requests
from tenacity import retry, stop_after_attempt, wait_fixed, stop_after_delay, retry_if_exception_type, RetryError
from typing import Dict, Any, Optional, List, Union, Tuple
from .config import ConfigParser
from .reporter import Reporter
from .utils import validate_response
from .generator import TestGenerator

class APIForge:
    def __init__(self, base_url: str, auth: Optional[Dict[str, Any]] = None):
        self.base_url = base_url.rstrip('/')
        self.auth = auth or {}
        self.session = requests.Session()

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
        response = self.session.request(method, url, params=params, **self.auth, **kwargs)
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
        try:
            reporter = kwargs.pop("reporter", None)
            result = self.send_request(url=url, method=method, params=params, expected_status=expected_status, **kwargs)
            if expected_keys is not None and not validate_response(result, expected_keys): raise AssertionError("Response validation failed: missing expected keys")
            # if reporter:
            #     test_config = {"method": method, "endpoint": endpoint, "params": params}
            #     reporter.log_api_result(test_config, result, True)
            return result
        except RetryError as e:
            # Wrap tenacity.RetryError in RuntimeError
            original_exception = e.last_attempt.exception() if e.last_attempt else e
            raise RuntimeError(f"API request failed after retries: {str(original_exception)}") from e
        except requests.RequestException as e:
            raise RuntimeError(f"API request failed after retries: {str(e)}")
        except ValueError as e:
            raise RuntimeError(f"API error: {str(e)}")
        except AssertionError as e:
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
    
    def run_generated_tests(self, spec: Union[str, Dict[str, Any]], reporter: Optional[Reporter] = None) -> List[Dict[str, Any]]:
        generator = TestGenerator()
        try:
            endpoints = generator.generate_tests(spec)
        except RuntimeError as e:
            raise RuntimeError(f"Failed to generate tests: {str(e)}")
        
        results = []
        for endpoint in endpoints:
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