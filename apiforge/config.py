import yaml
from typing import Dict, Any, Optional

class ConfigParser:
    @staticmethod
    def load_yaml(file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'r') as f: return yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load config: {str(e)}")
        
    @staticmethod
    def load_config(file_path: str, env: str = "prod") -> Optional[Dict[str, Any]]:
        config = ConfigParser.load_yaml(file_path)
        if config is None:
            return None  # Return None for empty files
        if not isinstance(config, dict):
            raise RuntimeError("Configuration file must parse to a dictionary")
        if "environments" in config:
            config["base_url"] = config["environments"].get(env, config["base_url"])
        return config