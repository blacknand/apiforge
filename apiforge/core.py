import requests
from typing import Dict, Any, Optional
from .config import ConfigParser
from .reporter import Reporter

class APIForge:
    def __init__(self, base_url: str, auth: Optional[Dict[str, Any]] = None):
        self.base_url = base_url.rstrip('/')
        self.auth = auth or {}
        self.session = requests.Session()

    @classmethod
    def from_config(cls, config_path: str) -> 'APIForge':
        config = ConfigParser.load_config(config_path, "prod")
        print("-------------------- config -----------------------")
        print(config)
        print("-------------------- config -----------------------")
        return cls(config["base_url"], config.get("auth"))

    def run_test(self, method: str, endpoint: str, expected_status: int = 200, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        valid_methods = ["PUT", "DELETE", "GET", "POST"]
        if not isinstance(method, str): raise TypeError("Expected method to be a str")
        if str.upper(method) not in valid_methods: raise ValueError(f"Invalid HTTP method passed. Recieved {method} but accepted HTTP methods are {valid_methods}")
        try:
            reporter = kwargs.pop("reporter", None)
            method = str.upper(method)
            response = self.session.request(method, url, **self.auth, **kwargs)
            if response.status_code != expected_status:
                raise AssertionError(
                    f"Expected {expected_status}, got {response.status_code}: {response.text}"
                )
            result = response.json()
            if reporter:
                test_config = {"method": method, "endpoint": endpoint}
                reporter.log_result(test_config, result, response.status_code == expected_status)
            return result
        except requests.RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}")
        
    def run_config_tests(self, config_path: str, env: str = "prod", reporter: Optional[Reporter] = None) -> list[Dict[str, Any]]:
        config = ConfigParser.load_config(config_path, env)
        results = []
        for endpoint in config["endpoints"]:
            result = self.run_test(
                method=endpoint["method"],
                endpoint=endpoint["path"],
                expected_status=endpoint["expected_status"],
                json=endpoint.get("payload"),
                reporter=reporter
            )
            print("------------------------- result -----------------------------")
            print(result)
            print("------------------------- result -----------------------------")
            results.append(result)
        return results