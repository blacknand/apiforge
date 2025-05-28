import pytest
import os
from apiforge.config import ConfigParser
from .test_core import EXPECTED_KEYS

def test_yaml_config():
    os.environ["API_BEARER_TOKEN"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    config = ConfigParser.load_config("configs/open_api_config.yaml", "prod")
    payload = {"id": 1, "title": "foo", "body": "bar", "userId": 1}
    put_payload = {"title": "foo", "body": "bar", "userId": 1}
    assert isinstance(config, dict)
    print(config)
    assert config["base_url"] == "https://jsonplaceholder.typicode.com"
    assert config["auth"]["headers"]["Authorization"] == "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    assert len(config["endpoints"]) == 4
    assert config["endpoints"][0] == {
        "method": "GET",
        "path": "posts",
        "params": {"userId": 1},
        "expected_status": 200,
        "expected_keys": EXPECTED_KEYS,
        "payload": None
    }
    assert config["endpoints"][1] == {
        "method": "POST",
        "path": "posts",
        "payload": payload,
        "expected_status": 201,
        "expected_keys": EXPECTED_KEYS,
        "params": {}
    }
    assert config["endpoints"][2] == {
        "method": "PUT",
        "path": "posts/{id}",
        "payload": put_payload,
        "expected_status": 200,
        "expected_keys": EXPECTED_KEYS,
        "params": {"id": 1}
    }
    assert config["endpoints"][3] == {
        "method": "DELETE",
        "path": "posts/{id}",
        "expected_status": 200,
        "expected_keys": [],
        "params": {"id": 1},
        "payload": None
    }

def test_config():
    config = ConfigParser.load_config("configs/api_config.yaml", "staging")
    assert config["base_url"] == "https://staging.example.com"

def test_load_config_missing_file():
    with pytest.raises(RuntimeError): ConfigParser.load_config("configs/non_existent_config.yaml")

def test_load_config_empty_yaml(tmp_path):
    empty_file = tmp_path / "invalid.yaml"
    with open(empty_file, "w") as f: f.write("")
    config = ConfigParser.load_config(str(empty_file))
    assert config is None