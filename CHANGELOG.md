# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.4.2 - 2020-06-13
### Additions
- Support for responses with no content (#63 & #66). Thanks @acgray!
- Support for custom string formats (#64 & #65). Thanks @acgray!


## 0.4.1 - 2020-06-02
### Additions
- Support for Python 3.7 (#58)


## 0.4.0 - 2020-05-30
### Breaking Changes
- Classes generated to be included within lists will now be named like <ListName>Item. For example, if a property 
    named "statuses" is an array of enum values, previously the `Enum` class declared would be called "Statuses". Now it 
    will be called "StatusesItem". If a "title" attribute was used in the OpenAPI document, that should still be respected
    and used instead of the generated name. You can restore previous names by adding "StatusesItem" to the `class_overrides`
    section of a config file.
- Clients now require httpx ^0.13.0 (up from ^0.12.1). See [httpx release notes](https://github.com/encode/httpx/releases/tag/0.13.0)
    for details.

### Additions
- Support for binary format strings (file payloads)
- Support for multipart/form bodies
- Support for any supported property within a list (array), including other lists.
- Support for Union types ("anyOf" in OpenAPI document)
- Support for more basic response types (integer, number, boolean)
- Support for duplicate enums. Instead of erroring, enums with the same name (title) but differing values 
    will have a number appended to the end. So if you have two conflicting enums named `MyEnum`, one of them
    will now be named `MyEnum1`. Note that the order in which these are processed and therefore named is entirely
    dependent on the order they are read from the OpenAPI document, so changes to the document could result 
    in swapping the names of conflicting Enums.

### Changes
- The way most imports are handled was changed which *should* lead to fewer unused imports in generated files.
- Better error messages
    - Most error messages will contain some useful information about why it failed instead of a stack trace
    - Client will still be generated if there are recoverable errors, excluding endpoints that had those errors
- Output from isort and black when generating will now be suppressed

### Fixes
- Defaults within models dataclasses for `Dict` or `List` properties will now be properly declared as a 
    `field` with the `default_factory` parameter to prevent errors related to mutable defaults.

## 0.3.0 - 2020-04-25
### Additions
- Link to the GitHub repository from PyPI (#26). Thanks @theY4Kman!
- Support for date properties (#30, #37). Thanks @acgray!
- Allow naming schemas by property name and Enums by title (#21, #31, #38). Thanks @acgray!

### Fixes
- Fixed some typing issues in generated clients and incorporate mypy into end to end tests (#32). Thanks @acgray!
- Properly handle camelCase endpoint names and properties (#29, #36). Thanks @acgray!

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
