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
3. **Support for part of the OpenAPI spec**; this generate _does not yet_ support every OpenAPI feature, these missing features **are not bugs**.

To request a feature:

1. Search through [discussions](https://github.com/openapi-generators/openapi-python-client/discussions/categories/feature-request) to see if the feature you want has already been requested. If it has:
  1. Upvote it with the little arrow on the original post. This enables code contributors to prioritize the most-demanded features.
  2. Optionally leave a comment describing why _you_ want the feature, if no existing thread already covers your use-case
3. If a relevant discussion does not already exist, create a new one. If you are not requesting support for part of the OpenAPI spec, **you must** describe _why_ you want the feature. What real-world use-case does it improve? For example, "raise exceptions for invalid responses" might have a description of "it's not worth the effort to check every error case by hand for the one-off scripts I'm writing".

## Contributing Code

### Setting up a Dev Environment

1. Make sure you have [Poetry](https://python-poetry.org/) installed and up to date.
2. Make sure you have a supported Python version (e.g. 3.8) installed and accessible to Poetry (e.g. with [pyenv](https://github.com/pyenv/pyenv)).
3. Use `poetry install` in the project directory to create a virtual environment with the relevant dependencies.
4. Enter a `poetry shell` to make running commands easier.

### Writing Code

1. Write some code and make sure it's covered by unit tests. All unit tests are in the `tests` directory and the file structure should mirror the structure of the source code in the `openapi_python_client` directory.

#### Run Checks and Tests

2. When in a Poetry shell (`poetry shell`) run `task check` in order to run most of the same checks CI runs. This will auto-reformat the code, check type annotations, run unit tests, check code coverage, and lint the code.

#### Rework end-to-end tests 

3. If you're writing a new feature, try to add it to the end-to-end test.
   1. If adding support for a new OpenAPI feature, add it somewhere in `end_to_end_tests/openapi.json`
   2. Regenerate the "golden records" with `task regen`. This client is generated from the OpenAPI document used for end-to-end testing.
   3. Check the changes to `end_to_end_tests/golden-record` to confirm only what you intended to change did change and that the changes look correct.
4. **If you added a test above OR modified the templates**: Run the end-to-end tests with `task e2e`. This will generate clients against `end_to_end_tests/openapi.json` and compare them with the golden record. The tests will fail if **anything is different**. The end-to-end tests are not included in `task check` as they take longer to run and don't provide very useful feedback in the event of failure. If an e2e test does fail, the easiest way to check what's wrong is to run `task regen` and check the diffs. You can also use `task re` which will run `regen` and `e2e` in that order.


### Creating a Pull Request

Once you've written the code and run the checks, the next step is to create a pull request against the `main` branch of this repository. This repository uses [conventional commits] squashed on each PR, then uses [Knope] to auto-generate CHANGELOG.md entries for release. So the title of your PR should be in the format of a conventional commit written in plain english as it will end up in the CHANGELOG. Some example PR titles:

- feat: Support for `allOf` in OpenAPI documents (closes #123).
- refactor!: Removed support for Python 3.5
- fix: Data can now be passed to multipart bodies along with files.

Once your PR is created, a series of automated checks should run. If any of them fail, try your best to fix them.

### Wait for Review

As soon as possible, your PR will be reviewed. If there are any changes requested there will likely be a bit of back and forth. Once this process is done, your changes will be merged into main and included in the next release. If you need your changes available on PyPI by a certain time, please mention it in the PR, and we'll do our best to accommodate.

[Conventional Commits]: https://www.conventionalcommits.org/en/v1.0.0/
[Knope]: https://knope-dev.github.io/knope/
