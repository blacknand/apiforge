# APIForge

APIForge is a Python-based automated testing framework for RESTful APIs, designed for simplicity and extensibility. It supports test generation, detailed reporting, and CI/CD integration, making API testing fast and reliable. It sends HTTP requests to an API (e.g. a `GET` request) and evaluates the response via paralelle test execution while logging the tests.

## Features
- Automatic test generation from OpenAPI specs
- Support for multiple HTTP methods and authentication
- Detailed test reports and logging
- CI/CD-ready with GitHub Actions
- Easy configuration of RESTful APIs using `yaml` configuration files
- Paralelle test execution
- Setup within seconds

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
forge = APIForge("https://jsonplaceholder.typicode.com")
result = forge.run_test("GET", "posts", expected_status=200, params: dict)
```

## Example OAS spec configuration
```json
"openapi": "3.0.3",
"info": {
    "title": "example test config API",
    "description": "Example simple test config",
    "version": "1.0.0"
},
"servers": [{"url": "https://jsonplaceholder.typicode.com"}],
"paths": {
    "/posts": {
        "get": {
            "responses": {
                "200": {
                    "description": "List of posts",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["id", "title", "body", "userId"],
                                    "properties": {
                                        "id": {"type": "integer"},
                                        "title": {"type": "string"},
                                        "body": {"type": "string"},
                                        "userId": {"type": "integer"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
```

## Example API custom YAML configuration
> NOTE: a starting point configuration file is provieded: `configs/api_config.yaml`. The best thing to do is to create a new `yaml` file for each configuration for each API.

> NOTE: it is better to follow the [OAS spec](https://swagger.io/specification/), even if `APIForge` supports custom `yaml` configs


Configure your RESTful API using a `yaml` configuration file inside of the `configs` directory:
```bash
base_url: https://jsonplaceholder.typicode.com
environments:
  prod: https://jsonplaceholder.typicode.com
  staging: https://staging.example.com
auth:
  headers:
    Authorization: Bearer dummy_token
endpoints:
  - method: GET
    path: posts
    expected_status: 200
  - method: POST
    path: posts
    payload: { "title": "foo", "body": "bar", "userId": 1 }
    expected_status: 201
```