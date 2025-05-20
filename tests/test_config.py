import pytest
from apiforge.config import ConfigParser
from .test_core import EXPECTED_KEYS

def test_yaml_config():
    config = ConfigParser.load_config("configs/api_config.yaml", "prod")
    payload = {"title": "foo", "body": "bar", "userId": 1}
    assert isinstance(config, dict)
    assert config["base_url"] == "https://jsonplaceholder.typicode.com"
    assert config["auth"]["headers"]["Authorization"] == "Bearer dummy_token"
    assert len(config["endpoints"]) == 4
    assert config["endpoints"][0] == {"method": "GET", "path": "posts", "params": {"userId": 1}, "expected_status": 200, "expected_keys": EXPECTED_KEYS}
    assert config["endpoints"][1] == {"method": "POST", "path": "posts", "payload": payload, "expected_status": 201, "expected_keys": EXPECTED_KEYS}
    assert config["endpoints"][2] == {"method": "PUT", "path": "posts/1", "payload": payload, "expected_status": 200, "expected_keys": EXPECTED_KEYS}
    assert config["endpoints"][3] == {"method": "DELETE", "path": "posts/1", "expected_status": 200, "expected_keys": []}

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