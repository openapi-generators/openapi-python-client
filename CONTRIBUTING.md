# Note: this is the fork of openapi-python-client maintained and used by Benchling.

If you want the official package, go to the upstream repository: https://github.com/openapi-generators/openapi-python-client

For contribution guidelines (including contributing fixes from our fork to the upstream repo), see Benchling internal documentation.

This document mostly contains basic developer instructions.

## Setting up environment

Create a virtualenv with the lowest compatible Python version (currently 3.9).

To install dependencies:

```
pip install poetry
poetry install
```

## Running tests

See the [upstream repo]() for a full description of how the tests in this project are written.

`poetry run task unit` runs only the basic unit tests.

`poetry run task test` runs unit tests plus end-to-end tests.

## Linting/type-checking

The project uses ruff. `poetry run task lint` and `poetry run task format` run `ruff check` and `ruff format`.

`poetry run task mypy` runs `mypy` on only the package module (tests are excluded).

`poetry run task check` runs all of those plus tests.

## Contributing Code

This section is a copy from the upstream repo, with some changes due to Benchling test framework additions that haven't yet been accepted upstream.

### Writing tests

All changes must be tested, I recommend writing the test first, then writing the code to make it pass. 100% code coverage is enforced in CI, a check will fail in GitHub if your code does not have 100% coverage. An HTML report will be added to the test artifacts in this case to help you locate missed lines.

If you think that some of the added code is not testable (or testing it would add little value), mention that in your PR and we can discuss it.

1. If you're adding support for a new OpenAPI feature or covering a new edge case, add [functional tests](#functional-tests), and optionally an [end-to-end snapshot test](#end-to-end-snapshot-tests).
2. If you're modifying the way an existing feature works, make sure functional tests cover this case. Existing end-to-end snapshot tests might also be affected if you have changed what generated model/endpoint code looks like.
3. If you're improving error handling or adding a new error, add [functional tests](#functional-tests).
4. For tests of low-level pieces of code that are fairly self-contained, and not tightly coupled to other internal implementation details, you can use regular [unit tests](#unit-tests).

#### End-to-end snapshot tests

This project aims to have all "happy paths" (types of code which _can_ be generated) covered by end-to-end tests. There are two types of these: snapshot tests, and functional tests.

Snapshot tests verify that the generated code is identical to a previously-committed set of snapshots (called a "golden record" here). They are basically regression tests to catch any unintended changes in the generator output.

In order to check code changes against the previous set of snapshots (called a "golden record" here), you can run `poetry run task e2e`. To regenerate the snapshots, run `poetry run task regen`.

There are 4 types of snapshots generated right now, you may have to update only some or all of these depending on the changes you're making. Within the `end_to_end_tests` directory:

1. `baseline_openapi_3.0.json` creates `golden-record` for testing OpenAPI 3.0 features
2. `baseline_openapi_3.1.yaml` is checked against `golden-record` for testing OpenAPI 3.1 features (and ensuring consistency with 3.0)
3. `test_custom_templates` are used with `baseline_openapi_3.0.json` to generate `custom-templates-golden-record` for testing custom templates
4. `3.1_specific.openapi.yaml` is used to generate `test-3-1-golden-record` and test 3.1-specific features (things which do not have a 3.0 equivalent)

#### Functional tests

These are black-box tests that verify the runtime behavior of generated code, as well as the generator's validation behavior. They are also end-to-end tests, since they run the generator as a shell command.

This can sometimes identify issues with error handling, validation logic, module imports, etc., that might be harder to diagnose via the snapshot tests, especially during development of a new feature. For instance, they can verify that JSON data is correctly decoded into model class attributes, or that the generator will emit an appropriate warning or error for an invalid spec.

See [`end_to_end_tests/functional_tests`](./end_to_end_tests/functional_tests).

#### Unit tests

These include:

* Regular unit tests of basic pieces of fairly self-contained low-level functionality, such as helper functions. These are implemented in the `tests` directory, using the `pytest` framework.
* Older-style unit tests of low-level functions like `property_from_data` that have complex behavior. These are brittle and difficult to maintain, and should not be used going forward. Instead, they should be migrated to functional tests.
