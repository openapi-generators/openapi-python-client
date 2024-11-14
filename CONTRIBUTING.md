# Ways you can Contribute

- Report bugs via [issues](https://github.com/openapi-generators/openapi-python-client/issues)
- Request features via [discussions](https://github.com/openapi-generators/openapi-python-client/discussions)
- Contribute code via [pull request](https://github.com/openapi-generators/openapi-python-client/pulls)

## Reporting a bug

A bug is one of:

1. You get an exception when running the generator
2. The generated code is invalid or incorrect
3. An error message is unclear or incorrect
4. Something which used to work no longer works, except:
   1. Intentional breaking changes, which are documented in the [changelog](https://github.com/openapi-generators/openapi-python-client/blob/main/CHANGELOG.md)
   2. Breaking changes to unstable features, like custom templates

If your issue does not fall under one of the above, it is not a bug; check out "[Requesting a feature](#requesting-a-feature).

### Report requirements

A bug report **must** have an OpenAPI document that can be used to replicate the bug. Reports without a valid document will be closed.

## Requesting a feature

A feature is usually:

1. An improvement to the way the generated code works
2. A feature of the generator itself which makes its use easier (e.g., a new config option)
3. **Support for part of the OpenAPI spec**; this generator _does not yet_ support every OpenAPI feature, these missing features **are not bugs**.

To request a feature:

1. Search through [discussions](https://github.com/openapi-generators/openapi-python-client/discussions/categories/feature-request) to see if the feature you want has already been requested. If it has:
   1. Upvote it with the little arrow on the original post. This enables code contributors to prioritize the most-demanded features.
   2. Optionally leave a comment describing why _you_ want the feature, if no existing thread already covers your use-case
2. If a relevant discussion does not already exist, create a new one. If you are not requesting support for part of the OpenAPI spec, **you must** describe _why_ you want the feature. What real-world use-case does it improve? For example, "raise exceptions for invalid responses" might have a description of "it's not worth the effort to check every error case by hand for the one-off scripts I'm writing".

## Contributing Code

### Setting up a Dev Environment

1. Make sure you have [PDM](https://pdm-project.org) installed and up to date.
2. Make sure you have a supported Python version (e.g. 3.8) installed.
3. Use `pdm install` in the project directory to create a virtual environment with the relevant dependencies.

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

In order to check code changes against the previous set of snapshots (called a "golden record" here), you can run `pdm e2e`. To regenerate the snapshots, run `pdm regen`.

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

### Creating a Pull Request

Once you've written the tests and code and run the checks, the next step is to create a pull request against the `main` branch of this repository. This repository uses [Knope] to auto-generate release notes and version numbers. This can either be done by setting the title of the PR to a [conventional commit] (for simple changes) or by adding [changesets]. If the changes are not documented yet, a check will fail on GitHub. The details of this check will have suggestions for documenting the change (including an example change file for changesets).

### Wait for Review

As soon as possible, your PR will be reviewed. If there are any changes requested there will likely be a bit of back and forth. Once this process is done, your changes will be merged into main and included in the next release. If you need your changes available on PyPI by a certain time, please mention it in the PR, and we'll do our best to accommodate.

[Knope]: https://knope.tech
[changesets]: https://knope.tech/reference/concepts/changeset/
[Conventional Commits]: https://knope.tech/reference/concepts/conventional-commits/
