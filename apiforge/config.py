import yaml
import os
import re
from prance import ResolvingParser
from typing import Dict, Any, Optional, Union

class ConfigParser:
    @staticmethod
    def load_yaml(file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'r') as f: return yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load config: {str(e)}")
        
    @staticmethod
    def load_config(spec: Union[str, Dict[str, Any]], env: str = "prod") -> Optional[Dict[str, Any]]:
        # Try parsing as OAS first
        try: 
            if isinstance(spec, dict): parser = ResolvingParser(specification_dict=spec)
            elif isinstance(spec, str): parser = ResolvingParser(spec)
            parser.parse()
            spec = parser.specification
            if not spec.get("openapi") or re.match(r"^3\.0\.\d+$", spec.get("openapi")):
                raise RuntimeError("Invalid OpenAPI spec")
        except Exception as e:
            # Fallback to custom YAML
            if isinstance(spec, str):
                config = ConfigParser.load_yaml(spec)
                if config is None:
                    return None
                if not isinstance(config, dict):
                    raise RuntimeError("Configuration file must parse to a dictionary")
                if "environments" in config:
                    config["base_url"] = config["environments"].get(env, config["base_url"])
                return config
            else: return {}

        # Select server based on env
        server = next(
            (s for s in spec.get("servers", []) if s["description"].lower().startswith(env)),
            spec.get("servers", [{}])[0]
        )
        base_url = server.get("url", "")

        # Extract auth
        auth = {"headers": {"Authorization": "Bearer dummy_token"}}  # Default
        if spec.get("security"):
            security_scheme = spec.get("components", {}).get("securitySchemes", {}).get("bearerAuth", {})
            if security_scheme:
                token_value = os.getenv("API_BEARER_TOKEN", security_scheme.get("bearerFormat", "dummy_token"))
                auth = {"headers": {"Authorization": f"Bearer {token_value}"}}

        # Build endpoints
        endpoints = []
        for path, operations in spec.get("paths", {}).items():
            for method, operation in operations.items():
                if method.lower() not in ["get", "post", "put", "delete"]:  # Exclude patch
                    continue

                endpoint = {
                    "method": method.upper(),
                    "path": path.lstrip("/"),
                    "expected_status": 200,
                    "expected_keys": [],
                    "params": {},
                    "payload": None
                }

                # Expected status
                for code in operation.get("responses", {}).keys():
                    if code.isdigit() and int(code) < 400:
                        endpoint["expected_status"] = int(code)
                        break

                # Parameters (query and path)
                if "parameters" in operation:
                    for param in operation["parameters"]:
                        if param.get("in") in ["query", "path"] and "schema" in param:
                            endpoint["params"][param["name"]] = param["schema"].get("example")

                # Payload
                if "requestBody" in operation:
                    schema = operation["requestBody"].get("content", {}).get("application/json", {}).get("schema", {})
                    if "$ref" in schema:
                        schema_ref = schema["$ref"].split("/")[-1]
                        schema_def = spec["components"].get("schemas", {}).get(schema_ref, {})
                    else:
                        # Handle resolved schema
                        schema_def = schema
                    payload = {
                        prop: schema_def["properties"][prop].get("example")
                        for prop in schema_def.get("properties", {})
                        if "example" in schema_def["properties"][prop]
                    }
                    if method.lower() == "put" and "id" in payload:
                        del payload["id"]
                    endpoint["payload"] = payload if payload else None

                # Expected keys
                response = operation.get("responses", {}).get(str(endpoint["expected_status"]), {})
                schema = response.get("content", {}).get("application/json", {}).get("schema", {})
                if schema.get("type") == "object":
                    endpoint["expected_keys"] = schema.get("required", [])
                elif schema.get("type") == "array":
                    item_schema = schema.get("items", {})
                    if "$ref" in item_schema:
                        if method.lower == "get": print(item_schema)
                        schema_ref = item_schema["$ref"].split("/")[-1]
                        endpoint["expected_keys"] = spec["components"]["schemas"].get(schema_ref, {}).get("required", [])
                    else:
                        endpoint["expected_keys"] = item_schema.get("required", [])
                elif schema.get("$ref") == "#/components/schemas/EmptyResponse":
                    endpoint["expected_keys"] = []

                endpoints.append(endpoint)

        return {
            "base_url": base_url,
            "auth": auth,
            "endpoints": endpoints
        }
