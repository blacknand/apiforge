# Apifogre Week 3 Roadmap: Advanced Core Features and Scalability

**Goal**: Enhance Apifogre’s core functionality with advanced Python techniques to make it scalable, extensible, and robust, while deepening your expertise in Python and software testing. This week focuses on complex features to showcase technical sophistication.

## TODOs

### 1. Enhance Test Generation with OpenAPI Support
**Description**: Extend the `TestGenerator` class to parse OpenAPI/Swagger specifications and automatically generate test cases for all endpoints, methods, and parameters. This adds a powerful feature that differentiates Apifogre from tools like Postman and demonstrates your ability to handle complex data parsing.

**Implementation Guidance**:
- Install `prance` (`pip install prance`) to parse OpenAPI specs (JSON/YAML).
- Update `generator.py` to read an OpenAPI spec and generate test cases dynamically.
- For each endpoint in the spec’s `paths`, extract the method, path, parameters, and expected response schema.
- Use list comprehensions and dictionary merging to create test configurations efficiently.
- Example code:
  ```python
  from prance import ResolvingParser
  from typing import Dict, Any, List
  class TestGenerator:
      def generate_tests(self, spec: Union[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
          parser = ResolvingParser(specification=spec) if isinstance(spec, str) else ResolvingParser(specification_dict=spec)
          tests = []
          for path, methods in parser.specification["paths"].items():
              for method, details in methods.items():
                  tests.append({
                      "method": method.upper(),
                      "endpoint": path.lstrip("/"),
                      "params": {p["name"]: p.get("default", "") for p in details.get("parameters", []) if p["in"] == "query"},
                      "expected_status": 200,
                      "expected_keys": [prop for prop in details.get("responses", {}).get("200", {}).get("schema", {}).get("properties", {}).keys()]
                  })
          return tests
  ```
- Test with a public OpenAPI spec (e.g., `https://petstore.swagger.io/v2/swagger.json`).
- Handle edge cases like missing schemas or invalid specs with proper error messages.

**Learning Outcome**:
- Master parsing complex JSON/YAML structures.
- Practice advanced Python features like list comprehensions and type hints.
- Understand OpenAPI specifications, a key skill for API development.

**Portfolio Impact**: Showcases your ability to integrate industry-standard API specs, making Apifogre competitive with professional tools.

---

### 2. Implement Parallel Test Execution
**Description**: Add support for running tests concurrently to improve performance, using `concurrent.futures.ThreadPoolExecutor`. This demonstrates advanced Python concurrency skills and makes Apifogre scalable for large test suites.

**Implementation Guidance**:
- Modify `run_config_tests` in `core.py` to execute tests in parallel.
- Use a context manager to ensure thread-safe session handling for `requests.Session`.
- Update `Reporter` to handle concurrent logging safely (e.g., using a lock).
- Example code:
  ```python
  from concurrent.futures import ThreadPoolExecutor
  from contextlib import contextmanager
  from threading import Lock
  class APIForge:
      @contextmanager
      def get_session(self):
          session = requests.Session()
          try:
              yield session
          finally:
              session.close()
      def run_config_tests(self, config_path: str, env: str = "prod", reporter: Optional[Reporter] = None) -> List[Dict[str, Any]]:
          config = ConfigParser.load_config(config_path, env)
          results = []
          with ThreadPoolExecutor(max_workers=4) as executor:
              futures = [executor.submit(self.run_test, **endpoint, reporter=reporter) for endpoint in config["endpoints"]]
              results = [future.result() for future in futures]
          return results
  class Reporter:
      def __init__(self, output_dir: str = "reports"):
          self.logger = logging.getLogger("APIForge")
          self.output_dir = output_dir
          self.results = []
          self.lock = Lock()
      def log_api_result(self, test: Dict[str, Any], result: Any, success: bool):
          with self.lock:
              status = "PASS" if success else "FAIL"
              self.logger.info(f"Test {test['method']} {test['endpoint']}: {status} - Result: {result}")
              self.results.append({"method": test["method"], "endpoint": test["endpoint"], "success": success, "result": result})
  ```
- Test with a large config file to verify performance improvements.
- Handle exceptions from failed futures gracefully.

**Learning Outcome**:
- Gain expertise in Python concurrency with `ThreadPoolExecutor`.
- Learn thread-safe programming with locks and context managers.
- Understand performance optimization for testing frameworks.

**Portfolio Impact**: Demonstrates scalability, a critical concern for MAANG companies handling large-scale systems.

---

### 3. Expand Authentication Support
**Description**: Enhance authentication to support OAuth 2.0 and API keys, using a decorator to apply auth dynamically. This adds flexibility and showcases advanced Python techniques like decorators.

**Implementation Guidance**:
- Add OAuth 2.0 support using `requests-oauthlib` (`pip install requests-oauthlib`).
- Update `ConfigParser` to parse auth configurations (e.g., `api_key` or `oauth2` credentials).
- Implement a decorator to inject authentication headers or parameters:
  ```python
  from functools import wraps
  from requests_oauthlib import OAuth2Session
  class APIForge:
      def __init__(self, base_url: str, auth: Optional[Dict[str, Any]] = None):
          self.base_url = base_url.rstrip('/')
          self.auth = auth or {}
          self.session = requests.Session()
          if self.auth.get("type") == "oauth2":
              self.session = OAuth2Session(token=self.auth.get("token"))
      def with_auth(auth_type: str):
          def decorator(func):
              @wraps(func)
              def wrapper(self, *args, **kwargs):
                  if auth_type == "api_key" and self.auth.get("api_key"):
                      kwargs["params"] = {**kwargs.get("params", {}), "api_key": self.auth["api_key"]}
                  return func(self, *args, **kwargs)
              return wrapper
          return decorator
      @with_auth("api_key")
      def send_request(self, url: str, method: str, params: Dict[str, Any] = {}, expected_status: int = 200, **kwargs) -> Dict[str, Any]:
          # Existing implementation
          pass
  ```
- Update `configs/api_config.yaml` to support auth types:
  ```yaml
  auth:
    type: oauth2
    token:
      access_token: your_access_token
  ```
- Test with APIs requiring API keys (e.g., ReqRes) and OAuth 2.0 (e.g., GitHub API).

**Learning Outcome**:
- Master decorators for reusable code.
- Learn OAuth 2.0 flows and secure credential management.
- Practice integrating third-party libraries.

**Portfolio Impact**: Shows familiarity with industry-standard authentication, a key requirement for API testing tools.

---

### 4. Add Advanced Response Validation
**Description**: Enhance `validate_response` to support JSON Schema validation and regex pattern matching, making Apifogre more robust for complex API responses.

**Implementation Guidance**:
- Install `jsonschema` (`pip install jsonschema`) for schema validation.
- Update `utils.py` to handle JSON Schema or regex-based validation:
  ```python
  from jsonschema import validate, ValidationError
  import re
  def validate_response(data: Any, expected_keys: Union[List[expected_key], Dict[str, Any], List[Tuple[str, str]]]) -> bool:
      if isinstance(expected_keys, dict):  # JSON Schema
          try:
              validate(instance=data, schema=expected_keys)
              return True
          except ValidationError:
              return False
      if isinstance(expected_keys, list) and expected_keys and isinstance(expected_keys[0], tuple) and len(expected_keys[0]) == 2 and expected_keys[0][1] == "regex":
          for key, pattern in expected_keys:
              if key not in data or not re.match(pattern, str(data[key])):
                  return False
          return True
      # Existing key-based validation
      return existing_validate_response(data, expected_keys)
  ```
- Update `configs/api_config.yaml` to support schema or regex:
  ```yaml
  endpoints:
    - method: GET
      path: posts
      expected_status: 200
      expected_schema:
        type: array
        items:
          type: object
          properties:
            id: {type: integer}
            title: {type: string}
  ```
- Test with complex responses from public APIs.

**Learning Outcome**:
- Deepen understanding of JSON Schema and regex.
- Practice handling complex validation logic.
- Enhance type hint usage for robust code.

**Portfolio Impact**: Demonstrates advanced validation capabilities, critical for enterprise-grade API testing.

---

### 5. Write Advanced Unit Tests
**Description**: Add tests for new features (OpenAPI generation, parallel execution, advanced validation) to ensure reliability and showcase testing expertise.

**Implementation Guidance**:
- Update `test_core.py` and `test_utils.py` with tests for new features.
- Use `pytest` fixtures and `unittest.mock` to mock OpenAPI specs and API responses.
- Example test for OpenAPI generation:
  ```python
  def test_generate_tests():
      generator = TestGenerator()
      spec = {"paths": {"/posts": {"get": {"responses": {"200": {"schema": {"properties": {"id": {}, "title": {}}}}}}}}
      tests = generator.generate_tests(spec)
      assert tests == [{"method": "GET", "endpoint": "posts", "params": {}, "expected_status": 200, "expected_keys": ["id", "title"]}]
  ```
- Test parallel execution by mocking multiple test runs:
  ```python
  def test_parallel_execution(api_forge, mocker):
      mocker.patch.object(api_forge, "run_test", return_value={"id": 1})
      results = api_forge.run_config_tests("configs/api_config.yaml")
      assert len(results) == 4
  ```
- Cover edge cases like invalid schemas or thread failures.

**Learning Outcome**:
- Master advanced testing with `pytest` and mocking.
- Learn to test concurrent code and edge cases.
- Build confidence in writing robust test suites.

**Portfolio Impact**: Comprehensive tests signal a commitment to quality, a key trait for MAANG roles.