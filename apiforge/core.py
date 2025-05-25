import requests
import time
from tenacity import retry, stop_after_attempt, wait_fixed, stop_after_delay, retry_if_exception_type
from typing import Dict, Any, Optional, List, Union, Tuple
from .config import ConfigParser
from .reporter import Reporter
from .utils import validate_response

class APIForge:
    def __init__(self, base_url: str, auth: Optional[Dict[str, Any]] = None):
        self.base_url = base_url.rstrip('/')
        self.auth = auth or {}
        self.session = requests.Session()

    @classmethod
    def from_config(cls, config_path: str) -> 'APIForge':
        config = ConfigParser.load_config(config_path, "prod")
        return cls(config["base_url"], config.get("auth"))
    
    # TODO: introduce threads + thread safety somehow
    """
    - raise AssertionError if the response status is not correct
    - raise any requests exception 
    """
    
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
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        valid_methods = ["PUT", "DELETE", "GET", "POST"]
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
        except requests.RequestException as e:
            raise RuntimeError(f"API request failed after retries: {str(e)}")
        except ValueError as e:
            raise RuntimeError(f"API error: {str(e)}")
        except AssertionError as e:
            raise RuntimeError(f"API test failed: {str(e)}")
        
    def run_config_tests(self, config_path: str, env: str = "prod", reporter: Optional[Reporter] = None) -> list[Dict[str, Any]]:
        config = ConfigParser.load_config(config_path, env)
        results = []
        for endpoint in config["endpoints"]:
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
        return results