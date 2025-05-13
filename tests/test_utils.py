from apiforge.utils import validate_response
from apiforge.core import APIForge
from .test_core import EXPECTED_KEYS

def api_forge():
    return APIForge.from_config("configs/api_config.yaml")

def test_valid_response():
    data = {"title": "foo", "body": "bar", "userId": 1}
    expected_keys = ["title", "body"]
    assert (validate_response(data, expected_keys=expected_keys), True)

def test_missing_keys():
    data = {"title": "foot"}
    expected_keys = ["title", "body"]
    assert (validate_response(data, expected_keys=expected_keys), False)

def testing_invalid_dict():
    data = {"title": "foot"}
    expected_keys = ["title"]
    assert (validate_response(data, expected_keys=expected_keys), False)

def testing_empty_keys():
    data = {"title": "foot"}
    expected_keys = []
    assert (validate_response(data, expected_keys=expected_keys), True)
