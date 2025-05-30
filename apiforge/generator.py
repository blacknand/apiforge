from .config import ConfigParser
from prance import ResolvingParser
from typing import Dict, Any, List, Union

class TestGenerator:
    def __init__(self, config_file: str = "configs/open_api_config.yaml"):
        self.config_file = config_file

    def generate_tests(self, spec: Union[str, Dict[str, Any]] = {}) -> List[Dict[str, Any]]:

        config = ConfigParser.load_config(spec, env="prod")     # Base server env
        endpoints = config["endpoints"]
        print(endpoints)

if __name__  == "__main__":
    # standalone: python3 -m apiforge.generator
    t = TestGenerator()
    t.generate_tests()
