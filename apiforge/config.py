import yaml
from typing import Dict, Any

class ConfigParser:
    @staticmethod
    def load_yaml(file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load config: {str(e)}")
        
    @staticmethod
    def load_config(file_path: str, env: str) -> Dict[str, Any]:
        config = ConfigParser.load_yaml(file_path)
        config["base_url"] = config["enviroments"].get(env, config["base_url"])
        return config