# openapi-python-client

## Purpose
Generate modern Python clients from OpenAPI

## Contribution Guidelines
 - The project is written to support Python 3.8 and should conform to the [Triax Python Standards](https://triaxtec.atlassian.net/wiki/spaces/EN/pages/499482627/Python+Guidelines).
 - Any changes should be covered with a unit test and documented in [CHANGELOG.md]

## Release Process
1. Start a release with Git Flow
1. Update the version number in `pyproject.toml` with `poetry version <rule>`
1. Ensure all requirements are pointing to released versions
1. Add the release date to the new version in [CHANGELOG.md]
1. Commit and push any changes
1. Create a pull request from the release branch to master
1. Get approval from all stakeholders
1. Ensure all checks pass (e.g. CircleCI)
1. Open and merge the pull request
1. Create a tag on the merge commit with the release number

## Contributors 
 - Dylan Anthony <danthony@triaxtec.com>


[CHANGELOG.md]: CHANGELOG.md
