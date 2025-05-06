from typing import Dict, Any, List

class TestGenerator:
    def generate_tests(self, spec: Dict[str, Any]) -> List[Dict[str, Any]]:
        tests = []
        tests.append({
            "method": "GET",
            "endpoint": "example",
            "expected_status": 200
        })
        return tests