---
default: minor
---

# Functional tests

Automated tests have been extended to include a new category of "functional" tests, in [`end_to_end_tests/functional_tests`](./end_to_end_tests/functional_tests). These are of two kinds:

1. Happy-path tests that run the generator from an inline API document and then actually import and execute the generated code.
2. Warning/error condition tests that run the generator from an inline API document that contains something invalid, and make assertions about the generator's output.

These provide more efficient and granular test coverage than the "golden record"-based end-to-end tests. Also, the low-level unit tests in `tests`, which are dependent on internal implementation details, can now in many cases be replaced by functional tests.

This does not affect any runtime functionality of openapi-python-client.
