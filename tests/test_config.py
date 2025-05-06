import pytest
from apiforge.core import APIForge
from apiforge.config import ConfigParser
from apiforge.reporter import TestReporter

def test_config():
    config = ConfigParser.load_config("configs/api_config.yaml")
    assert isinstance(config, dict)
    assert config["base_url"] == "https://jsonplaceholder.typicode.com"
    assert config["auth"]["headers"]["Authorization"] == "Bearer dummy_token"
    assert len(config["endpoints"]) == 2
    assert config["endpoints"][0] == {"method": "GET", "path": "posts", "expected_status": 200}
    assert config["endpoints"][1]["method"] == "POST"
    assert config["endpoints"][1]["payload"] == {"title": "foo", "body": "bar", "userId": 1}

def test_load_config_missing_file():
    with pytest.raises(RuntimeError): ConfigParser.load_config("configs/non_existent_config.yaml")

def test_load_config_invalid_yaml(tmp_path):
    invalid_file = tmp_path / "invalid.yaml"
    with open(invalid_file, "w") as f: f.write("invalid: : : yaml")
    with pytest.raises(RuntimeError): ConfigParser.load_config(str(invalid_file))

def test_load_config_empty_yaml(tmp_path):
    empty_file = tmp_path / "invalid.yaml"
    with open(empty_file, "w") as f: f.write("")
    config = ConfigParser.load_config(str(empty_file))
    assert config is None

def test_run_config_tests(api_forge: APIForge, tmp_path: str):
    reporter = TestReporter(str(tmp_path))
    results = api_forge.run_config_tests("configs/api_config.yaml", reporter)
    assert len(results) == 2