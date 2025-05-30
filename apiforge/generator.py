import os
from .config import ConfigParser
from typing import Dict, Any, List, Union

class TestGenerator:
    def __init__(self, config_file: str = "configs/open_api_config.yaml"):
        self.config_file = config_file

    def generate_tests(self, spec: Union[str, Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if spec and isinstance(spec, str):
            if not spec.startswith("http") and not os.path.exists(spec):
                raise RuntimeError("Invalid file passed")

        try:
            if spec: config = ConfigParser.load_config(spec, for_generator=True)     
            else: config = ConfigParser.load_config(self.config_file, for_generator=True)
            endpoints = config.get("endpoints", [])
            return endpoints
        except Exception as e:
            raise RuntimeError(f"The following exception occured when attempting to invoke load_config: {e}")