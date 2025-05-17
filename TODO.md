APIForge Week 2 Roadmap
Overview
APIForge is a Python-based API testing framework designed to automate testing of RESTful APIs. Week 1 established a core framework with HTTP request support (GET, POST, PUT, DELETE), response validation, and YAML-based configuration. Week 2 enhances APIForge with professional-grade features to demonstrate advanced testing capabilities for a MAANG internship portfolio.
Objective: Extend APIForge to support query parameters, enhance response validation, improve error handling, and upgrade reporting, ensuring robustness and portfolio readiness.
Duration: May 15–May 22, 2025 (1 week)
Prerequisites:

Week 1 completed: Functional run_test, validate_response, test_core.py, test_utils.py, test_config.py, and api_config.yaml.
Test API: jsonplaceholder.typicode.com.
Tools: Python, Pytest, YAML.

Week 2 Goals

Query Parameter Support: Enable run_test to handle query parameters (e.g., GET /posts?userId=1).
Enhanced Response Validation: Validate response key types and values (e.g., id is an integer, title is "foo").
Improved Error Handling: Add retry logic for network failures and handle invalid endpoints.
Enhanced Reporting: Log detailed test results (e.g., response time, payload).
Documentation: Update README.md to reflect new features.

Daily Tasks and Deliverables
Day 1: Query Parameter Support (May 15, 2025)

Tasks:
Update run_test in core.py to accept a params argument and pass it to requests.request.
Add params to the GET endpoint in api_config.yaml (e.g., userId: 1).
Add test_query_params in test_core.py to test GET /posts?userId=1.


Deliverable: Updated core.py, api_config.yaml, and test_core.py with passing tests.
Estimated Time: 2 hours.

Day 2: Enhanced Response Validation (May 16, 2025)

Tasks:
Modify validate_response in utils.py to accept expected_keys as tuples (e.g., ("id", int), ("title", str, "foo")).
Update run_test to support the new format.
Add tests in test_utils.py for type and value validation.
Add test_response_val_types in test_core.py for GET /posts/1.


Deliverable: Updated utils.py, core.py, test_utils.py, and test_core.py with passing tests.
Estimated Time: 3 hours.

Day 3: Error Handling (May 17, 2025)

Tasks:
Add retry logic to run_test for network failures (e.g., ConnectionError).
Handle 404 errors for invalid endpoints.
Add test_network_failure and test_invalid_endpoint in test_core.py.


Deliverable: Updated core.py and test_core.py with passing tests.
Estimated Time: 2.5 hours.

Day 4: Reporting Improvements (May 18, 2025)

Tasks:
Enhance Reporter in reporter.py to log response time, payload, status, and response data.
Update run_test to measure and pass response time to Reporter.
Add test_reporter_output in test_core.py to verify log content.


Deliverable: Updated reporter.py, core.py, and test_core.py with passing tests.
Estimated Time: 2 hours.

Day 5: Documentation and Testing (May 19, 2025)

Tasks:
Update README.md to document query parameters, validation, error handling, and reporting.
Run all tests (test_core.py, test_utils.py, test_config.py) and fix issues.


Deliverable: Polished README.md and passing test suite.
Estimated Time: 1.5 hours.

Day 6: Polish and Review (May 20, 2025)

Tasks:
Review code for PEP 8 compliance and add comments.
Add edge case tests (e.g., empty params, invalid expected_keys).
Create a demo script or notebook for portfolio presentation.


Deliverable: Clean code, additional tests, and demo script.
Estimated Time: 2 hours.

Day 7: Final Testing and Submission (May 21, 2025)

Tasks:
Run full test suite and fix any failures.
Commit changes to GitHub with clear messages.
Plan Week 3 goals (e.g., authentication, parallel testing).


Deliverable: Fully tested codebase on GitHub, Week 3 outline.
Estimated Time: 1 hour.

Expected Deliverables

Code: Updated core.py, utils.py, reporter.py, test_core.py, test_utils.py, api_config.yaml, and README.md.
Tests: Passing tests for query parameters, validation, errors, and reporting.
Documentation: Comprehensive README.md and demo script.
Repository: Clean GitHub repo with Week 2 commits.

Tips for Success

Test Incrementally: Run pytest -v after each task.
Leverage API: Use jsonplaceholder.typicode.com endpoints like GET /posts?userId=1 or GET /invalid.
Document Learning: Highlight challenges and solutions in README.md for portfolio impact.
Ask for Help: Share test failures or questions to stay on track.

Next Steps

Start with Day 1: Implement query parameter support.
Run pytest test_core.py -v to verify progress.
Share updates or issues for guidance.

Let’s make Week 2 shine for your portfolio!
