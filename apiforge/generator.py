from prance import ResolvingParser
from typing import Dict, Any, List, Union

class TestGenerator:
    def __init__(self, config_file: str = "configs/open_api_config.yaml"):
        self.config_file = config_file

    def generate_tests(self, spec: Union[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        parser = ResolvingParser(self.config_file)
        parser.parse()
        spec = parser.specification
        tests = []

        for path, path_def in spec.get("paths", {}).items():
            # print(path)
            for method, method_def in path_def.items():
                # TODO: add patch support in core.py
                if method.lower() not in ["get", "post", "put", "delete", "patch"]:
                    continue

                test_case = {}
                test_case["method"] = method
                test_case["endpoint"] = path

                print(test_case)

                # print(f"{method}\n\n{method_def}\n")

if __name__  == "__main__":
    t = TestGenerator()
    t.generate_tests("NaN")