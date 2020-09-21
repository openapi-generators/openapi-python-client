# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.6.0 - Unreleased

### Breaking Changes

- Reorganized api calls in generated clients. `async_api` will no longer be generated. Each path operation will now
  have it's own module under its tag. For example, if there was a generated function `api.my_tag.my_function()` it is
  replaced with `api.my_tag.my_function.sync()`. The async version can be called with `asyncio()` instead of `sync()`.
  (#167)
- Removed support for mutable default values (e.g. dicts, lists). They may be added back in a future version given enough
  demand, but the existing implementation was not up to this project's standards. (#170)
- Removed generated `errors` module (and the `ApiResponseError` therein). Instead of raising an exception on failure,
  the `sync()` and `asyncio()` functions for a path operation will return `None`. This means all return types are now
  `Optional`, so mypy will require you to handle potential errors (or explicitly ignore them).
- Moved `models.types` generated module up a level, so just `types`.
- All generated classes that were `dataclass` now use the `attrs` package instead

### Additions

- Every generated API module will have a `sync_detailed()` and `asyncio_detailed()` function which work like their
  non-detailed counterparts, but return a `types.Response[T]` instead of an `Optional[T]` (where T is the parsed body type).
  `types.Response` contains `status_code`, `content` (bytes of returned content), `headers`, and `parsed` (the
  parsed return type you would get from the non-detailed function). (#115)
- It's now possible to include custom headers and cookies in requests, as well as set a custom timeout. This can be done
  either by directly setting those parameters on a `Client` (e.g. `my_client.headers = {"Header": "Value"}`) or using
  a fluid api (e.g. `my_endpoint.sync(my_client.with_cookies({"MyCookie": "cookie"}).with_timeout(10.0))`).
- Unsupported content types or no responses at all will no longer result in an endpoint being completely skipped. Instead, 
  only the `detailed` versions of the endpoint will be generated, where the resulting `Response.parsed` is always `None`.
  (#141)
- Support for Python 3.6 (#137 & #154)
- Support for enums with integer values
  
### Changes

- The format of any errors/warnings has been spaced out a bit.

## 0.5.5 - 2020-09-04
### Fixes
- Improved trailing comma handling in endpoint generation (#178 & #179). Thanks @dtkav!
- `Optional` is now properly imported for `nullable` fields (#177 & #180). Thanks @dtkav!


## 0.5.4 - 2020-08-29

### Additions

- Support for octet-stream content type (#116)
- Support for [nullable](https://swagger.io/docs/specification/data-models/data-types/#null) (#99)
- Union properties can be defined using oneOf (#98)
- Support for lists of strings, integers, floats and booleans as responses (#165). Thanks @Maistho!

## 0.5.3 - 2020-08-13

### Security

- All values that become file/directory names are sanitized to address path traversal vulnerabilities (CVE-2020-15141)
- All values that get placed into python files (everything from enum names, to endpoint descriptions, to default values) are validated and/or saniziatied to address arbitrary code execution vulnerabilities (CVE-2020-15142)

### Changes

- Due to security concerns/implementation complexities, default values are temporarily unsupported for any `RefProperty` that doesn't refer to an enum.
- Defaults for properties must now be valid values for their respective type (e.g. "example string" is an invalid default for an `integer` type property, and the function for an endpoint using it would fail to generate and be skipped).

### Additions

- Added support for header parameters (#117)

### Fixes

- JSON bodies will now be assigned correctly in generated clients(#139 & #147). Thanks @pawamoy!

## 0.5.2 - 2020-08-06

### Additions

- Added `project_name_override` and `package_name_override` config options to override the name of the generated project/package (#123)
- The generated library's version is now the same as the OpenAPI doc's version (#134)

## 0.5.1 - 2020-08-05

### Fixes

- Relative paths are now allowed in securitySchemes/OAuthFlow/tokenUrl (#130).
- Schema validation errors will no longer print a stack trace (#131).
- Invalid YAML/URL will no longer print stack trace (#128)

## 0.5.0 - 2020-08-05

### Changes

- When encountering a problem, the generator will now differentiate between warnings (things it was able to skip past)
  and errors (things which halt generation altogether).

### Additions

- The generator can now handle many more errors gracefully, skipping the things it can't generate and continuing
  with the pieces it can.
- Support for Enums declared in "components/schemas" and references to them (#102).
- Generated clients can now be installed via pip (#120).
- Support for YAML OpenAPI documents (#111)

### Internal Changes

- Switched OpenAPI document parsing to use Pydantic based on a vendored version of
  [openapi-schema-pydantic](https://github.com/kuimono/openapi-schema-pydantic/) (#103).
- Tests can now be run on Windows.

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

- The way most imports are handled was changed which _should_ lead to fewer unused imports in generated files.
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
