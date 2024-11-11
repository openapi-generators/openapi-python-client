---
default: minor
---

# New categories of end-to-end tests

Automated tests have been extended to include two new types of tests:

1. Happy-path tests that run the generator from an inline API document and then actually import and execute the generated code. See [`end_to_end_tests/generated_code_live_tests`](./end_to_end_tests/generated_code_live_tests).
2. Warning/error condition tests that run the generator from an inline API document that contains something invalid, and make assertions about the generator's output.

These provide more efficient and granular test coverage than the "golden record"-based end-to-end tests, and also replace some tests that were previously being done against low-level implementation details in `tests/unit`.

This does not affect any runtime functionality of openapi-python-client.
