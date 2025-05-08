# APIForge

APIForge is a Python-based automated testing framework for RESTful APIs, designed for simplicity and extensibility. It supports test generation, detailed reporting, and CI/CD integration, making API testing fast and reliable. It sends HTTP requests to an API (e.g. a `GET` request) and checks if the responses match expectations (e.g. Status code `200` and valid JSON data).

## Features
- Automatic test generation from OpenAPI specs
- Support for multiple HTTP methods and authentication
- Detailed test reports and logging
- CI/CD-ready with GitHub Actions

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
forge = APIForge("https://jsonplaceholder.typicode.com")
result = forge.run_test("GET", "posts", expected_status=200)
```

## Example API configuration
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