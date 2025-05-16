import pytest
from apiforge.utils import validate_response
from apiforge.core import APIForge
from .test_core import EXPECTED_KEYS

def test_valid_response():
    data = {"title": "foo", "body": "bar", "userId": 1}
    expected_keys = ["title", "body"]
    assert (validate_response(data, expected_keys=expected_keys)) is True

def test_missing_keys():
    data = {"title": "foot"}
    expected_keys = ["title", "body"]
    assert (validate_response(data, expected_keys=expected_keys)) is False

def testing_invalid_dict():
    data = {"title"}
    expected_keys = ["title"]
    assert (validate_response(data, expected_keys=expected_keys)) is False

def testing_empty_keys():
    data = {"title": "foot"}
    expected_keys = []
    assert (validate_response(data, expected_keys=expected_keys)) is True