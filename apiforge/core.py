import requests
from typing import Dict, Any, Optional

class APIForge:
    def __init__(self, base_url: str, auth: Optional[Dict[str, Any]] = None):
        self.base_url = base_url.rstrip('/')
        self.auth = auth or {}
        self.session = requests.Session()

    def run_test(self, method: str, endpoint: str, expected_status: int = 200, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.request(method, url, **self.auth, **kwargs)
            if response.status_code != expected_status:
                raise AssertionError(
                    f"Expected {expected_status}, got {response.status_code}: {response.text}"
                )
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}")