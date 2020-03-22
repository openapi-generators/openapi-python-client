# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.2.1 - 2020-03-22
### Fixes
- Fixed import of errors.py in generated api modules

### Additions
- Support for lists of Enums
- Add config for black to generated pyproject.toml

## 0.2.0 - 2020-03-22
### Changes
- Update Typer dependency to 0.1.0 and remove click-completion dependency (#19)
- Switched to httpx from requests for both this tool and generated clients (#15)

### Additions
- `--version` option to print the version of openapi-python-client and exit
- `--config` option for passing a config.yml file to override generated class names (#9)
- Generated clients will now have some basic Poetry usage in their README.md (#13)
- Generated clients will now have an async_api module for async versions of every function in the api module (#16)
- Generated clients will be auto-formatted with isort and black (#12)
- Generated clients will have a .gitignore covering some basics (#14)
- A number of additions to the README including recommending pipx (#20)

## 0.1.2 - 2020-03-16
- Improve handling of optional properties in generated `to_dict` function for models
- Add PEP 561 marker file (py.typed) to generated packages

## 0.1.1 - 2020-03-06
- Fix mypy issue in generated models `from_dict` with datetime or reference properties
- Generated clients now raise an `ApiResponseError` if they receive a response that was not declared
- Stop including optional query parameters when value is set to None
- Added an `update` command to update a previously generated client
- Added click-completion for installable tab completion in most shells

## 0.1.0 - 2020-02-28
- Initial Release
