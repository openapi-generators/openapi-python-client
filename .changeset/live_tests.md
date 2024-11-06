---
default: minor
---

# New category of end-to-end tests

There is a new set of tests that generate client code from an API document and then actually import and execute that code. See [`end_to_end_tests/generated_code_live_tests`](./end_to_end_tests/generated_code_live_tests) for more details.

This does not affect any runtime functionality of openapi-python-client.
