from typing import Any

def validate_response(data: Any, expected_keys: list) -> bool:
    if not isinstance(data, dict):
        return False
    return all(key in data for key in expected_keys)