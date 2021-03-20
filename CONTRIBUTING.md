# Ways you can Contribute

- Document bugs and missing features as issues.
- Find and document the relevant [OpenAPI specification](https://swagger.io/specification/) for open issues.
- Create a pull request addressing an open issue.

# Contributing Code

## Setting up a Dev Environment

1. Make sure you have [Poetry](https://python-poetry.org/) installed and up to date.
2. Make sure you have a supported Python version (e.g. 3.8) installed and accessible to Poetry (e.g. with [pyenv](https://github.com/pyenv/pyenv).
3. Use `poetry install` in the project directory to create a virtual environment with the relevant dependencies.
4. Enter a `poetry shell` to make running commands easier.

## Writing Code

1. Write some code and make sure it's covered by unit tests. All unit tests are in the `tests` directory and the file structure should mirror the structure of the source code in the `openapi_python_client` directory.
2. When in a Poetry shell (`poetry shell`) run `task check` in order to run most of the same checks CI runs. This will auto-reformat the code, check type annotations, run unit tests, check code coverage, and lint the code.
3. If you're writing a new feature, try to add it to the end to end test.
   1. If adding support for a new OpenAPI feature, add it somewhere in `end_to_end_tests/openapi.json`
   2. Regenerate the "golden records" with `task regen`. This client is generated from the OpenAPI document used for end to end testing.
   3. Check the changes to `end_to_end_tests/golden-record` to confirm only what you intended to change did change and that the changes look correct.
4. Run the end to end tests with `task e2e`. This will generate clients against `end_to_end_tests/openapi.json` and compare them with the golden record. The tests will fail if **anything is different**. The end to end tests are not included in `task check` as they take longer to run and don't provide very useful feedback in the event of failure. If an e2e test does fail, the easiest way to check what's wrong is to run `task regen` and check the diffs. You can also use `task re` which will run `regen` and `e2e` in that order.

## Creating a Pull Request

Once you've written the code and run the checks, the next step is to create a pull request against the `main` branch of this repository. This repository uses [conventional commits] squashed on each PR, then uses [Dobby] to auto-generate CHANGELOG.md entries for release. So the title of your PR should be in the format of a conventional commit written in plain english as it will end up in the CHANGELOG. Some example PR titles:

- feat: Support for `allOf` in OpenAPI documents (closes #123).
- refactor!: Removed support for Python 3.5
- fix: Data can now be passed to multipart bodies along with files.

Once your PR is created, a series of automated checks should run. If any of them fail, try your best to fix them.

## Wait for Review

As soon as possible, your PR will be reviewed. If there are any changes requested there will likely be a bit of back and forth. Once this process is done, your changes will be merged into main and included in the next release. If you need your changes available on PyPI by a certain time, please mention it in the PR, and we'll do our best to accommodate.

[Conventional Commits]: https://www.conventionalcommits.org/en/v1.0.0/
[Dobby]: https://triaxtec.github.io/dobby/introduction.html
