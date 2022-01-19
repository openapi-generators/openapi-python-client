# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Breaking changes to any of the following will cause the **minor** version to be incremented (as long as this project is 0.x). Only these pieces are considered part of the public API:

- The _behavior_ of the generated code. Specifically, the way in which generated endpoints and classes are called and the way in which those calls communicate with an OpenAPI server. Any other property of the generated code is not considered part of the versioned, public API (e.g., code formatting, comments).
- The invocation of the CLI (e.g., commands or arguments).

Programmatic usage of this project (e.g., importing it as a Python module) and the usage of custom templates are not considered part of the public API and therefore may change behavior at any time without notice.

The 0.x prefix used in versions for this project is to indicate that breaking changes are expected frequently (several times a year). Breaking changes will increment the minor number, all other changes will increment the patch number. You can track the progress toward 1.0 [here](https://github.com/openapi-generators/openapi-python-client/projects/2).

## 0.11.0

### Breaking Changes

- Minimum required `attrs` version in generated clients is now 21.3.0.
- Python 3.6 is officially not supported. The minimum version has been updated to reflect this.
- Validation of OpenAPI documents is now more strict.
- Model names generated from OpenAPI names with periods (`.`) in them will be different.
- Header values will be explicitly transformed or omitted instead of blindly passed to httpx as-is.
- `datetime` is now considered a reserved word everywhere, so any properties which were named `datetime` will now be named `datetime_`.
- `File` uploads can now only accept binary payloads (`BinaryIO`).

### Features

- Don't set a cap on allowed `attrs` version.
- use poetry-core as build backend in generated clients [#565]. Thanks @fabaff!
- Use httpx.request to allow bodies for all type of requests [#545, #547]. Thanks @MalteBecker!

### Fixes

- OpenAPI schema validation issues (#426, #568). Thanks @p1-ra!
- treat period as a delimiter in names (#546). Thanks @alexifm!
- Non-string header values [#552, #553, #566]. Thanks @John98Zakaria!
- Generate valid code when a property of a model is named "datetime" [#557 & #558]. Thanks @kmray!
- Multipart uploads for httpx >= 0.19.0 [#508, #548]. Thanks @skuo1-ilmn & @kairntech!

## 0.10.8

### Features

- New and improved docstrings in generated functions and classes [#503, #505, #551]. Thanks @rtaycher!
- Support httpx 0.21.\* (#537)

### Fixes

- Basic types as JSON bodies and responses [#487 & #550]. Thanks @Gelbpunkt!
- Relative paths to config files [#538 & #544]. Thanks to @motybz, @MalteBecker, & @abhinav-cashify!

## 0.10.7

### Fixes

- SSL verify argument to async clients [#533 & #510]. Thanks @fsvenson and @mvaught02!
- Remove unused CHANGELOG from generated setup.py [#529]. Thanks @johnthagen!

## 0.10.6

### Features

- Improve error messages related to invalid arrays and circular or recursive references [#519].
- Add httpx 0.20.\* support [#514].

### Fixes

- Use isort "black" profile in generated clients [#523]. Thanks @johnthagen!
- setup.py should generate importable packages named <project>\_client [#492, #520, #521]. Thanks @tedo-benchling & @Leem0sh!
- Allow None in enum properties [#504, #512, #516]. Thanks @juspence!
- properly support JSON OpenAPI documents and config files [#488, #509, #515]. Thanks @tardyp and @Gelbpunkt!

## 0.10.5

### Features

- Add verify_ssl option to generated Client, allowing users to ignore or customize ssl verification (#497). Thanks @rtaycher!

### Fixes

- Properly label a path template issue as a warning (#494). Thanks @chamini2!
- Don't allow mixed types in enums.
- Don't crash when a null is in an enum (#500). Thanks @juspence!

## 0.10.4

### Features

- Allow customization of post-generation steps with the `post_hooks` config option.
- Allow httpx 0.19.\* (#481)

### Fixes

- Don't crash the generator when one of the post-generation hooks is missing [fixes #479]. Thanks @chamini2 and @karolzlot!

## 0.10.3

### Features

- Expose `python_identifier` and `class_name` functions to custom templates to rename with the same behavior as the parser.

### Fixes

- Treat `true` and `false` as reserved words.
- Prevent generating Python files named the same as reserved / key words.
- Properly replace reserved words in class and module names [#475, #476]. Thanks @mtovts!

## 0.10.2

### Features

- Allow path parameters to be positional args [#429 & #464]. Thanks @tsotnikov!
- Include both `UNSET` and `None` static types for nullable or optional query params [#421, #380, #462]. Thanks @forest-benchling!
- Allow allOf enums to be subsets of one another or their base types [#379, #423, #461]. Thanks @forest-benchling! (#461)

### Fixes

- Parameters from `PathItem` can now be overriden in `Operation` [#458 & #457]. Thanks @mtovts!

## 0.10.1

### Fixes

- Support multipart requests with type: array [#452 & #451]. Thanks @csymeonides-mf @slamora and @dpursehouse

## 0.10.0

### Breaking Changes

- Normalize generated module names to allow more tags [#428 & #448]. Thanks @iamnoah & @forest-benchling!
- Improved the consistency of snake_cased identifiers which will cause some to be renamed [#413 & #432]. Thanks @ramnes!
- Allow more types in multipart payloads by defaulting to JSON for complex types [#372]. Thanks @csymeonides-mf!

### Features

- Allow custom templates for API and endpoint `__init__` files. [#442] Thanks @p1-ra!

### Fixes

- Treat empty schemas like `Any` instead of `None`. Thanks @forest-benchling! [#417 & #445]

## 0.9.2

### Features

- Add option to fail on warning [#427]. Thanks @forest-benchling!

### Fixes

- Properly strip out `UNSET` values from form data [#430]. Thanks @p1-ra!

## 0.9.1

### Features

- Allow references to non-object, non-enum types [#371][#418][#425]. Thanks @p1-ra!
- Allow for attrs 21.x in generated clients [#412]
- Allow for using any version of Black [#416] [#411]. Thanks @christhekeele!

### Fixes

- Prevent crash when providing a non-string default to a string attribute. [#414] [#415]
- Deserialization of optional nullable properties when no value is returned from the API [#420] [#381]. Thanks @forest-benchling!

## 0.9.0 - 2021-05-04

### Breaking Changes

- Some generated names will be different, solving some inconsistencies. (closes #369) (#375) Thanks @ramnes!
- Change reference resolution to use reference path instead of class name (fixes #342) (#366)
- If a schema references exactly one other schema in `allOf`, `oneOf`, or `anyOf` that referenced generated model will be used directly instead of generating a copy with another name. (#361)
- Attributes shadowing any builtin except `id` and `type` will now be renamed in generated clients (#360, #378, #407). Thanks @dblanchette and @forest-benchling!

### Features

- Allow httpx 0.18.x in generated clients (#400)
- Add summary attribute to Endpoint for use in custom templates (#404)
- Support common parameters for paths (#376). Thanks @ramnes!
- Add allOf support for model definitions (#98) (#321)

### Fixes

- Attempt to deduplicate endpoint parameters based on name and location (fixes #305) (#406)
- Names of classes without titles will no longer include ref path (fixes #397) (#405). Thanks @ramnes!
- Problems with enum defaults in allOf (#363). Thanks @csymeonides-mf
- Prevent duplicate return types in generated api functions (#365)
- Support empty strings in enums (closes #357) (#358). Thanks @ramnes!
- Allow passing data with files in multipart. (Fixes #351) (#355)
- Deserialization of unions (#332). Thanks @forest-benchling!

## 0.8.0 - 2021-02-19

### Breaking Changes

- Generated clients will no longer pass through `None` to query parameters. Previously, any query params set to `None` would surface as empty strings (per the default behavior of `httpx`). This is contrary to the defaults indicated by the OpenAPI 3.0.3 spec. Ommitting these parameters makes us more compliant. If you require a style of `null` to be passed to your query parameters, please request support for the OpenAPI "style" attribute. Thank you to @forest-benchling and @bowenwr for a ton of input on this.

### Additions

- New `--meta` command line option for specifying what type of metadata should be generated:

  - `poetry` is the default value, same behavior you're used to in previous versions
  - `setup` will generate a pyproject.toml with no Poetry information, and instead create a `setup.py` with the project info.
  - `none` will not create a project folder at all, only the inner package folder (which won't be inner anymore)

- Attempt to detect and alert users if they are using an unsupported version of OpenAPI (#281).

- The media type application/vnd.api+json will now be handled just like application/json (#307). Thanks @jrversteegh!

- Support passing models into query parameters (#316). Thanks @forest-benchling!

- Add support for cookie parameters (#326).

- New `--file-encoding` command line option (#330). Sets the encoding used when writing generated files (defaults to utf-8). Thanks @dongfangtianyu!

### Changes

- Lowered the minimum version of `python-dateutil` to 2.8.0 for improved compatibility (#298 & #299). Thanks @bowenwr!
- The `from_dict` method on generated models is now a `@classmethod` instead of `@staticmethod` (#215 & #292). Thanks @forest-benchling!
- Renamed all templates to end in `.jinja`, and all python-templates to end in `.py.jinja` to fix confusion with the latest version of mypy. Note **this will break existing custom templates until you update your template file names**.

### Fixes

- Endpoint tags are now sanitized during parsing to fix an issue where `My Tag` and `MyTag` are seen as two different tags but are then later unified, causing errors when creating directories. Thanks @p1-ra! (#328)
- Parser will softly ignore value error during schema responses' status code convertion from string to integer (not a number). Errors will be reported to the end user and parsing will continue to proceed (#327).
- The generated `from_dict` and `to_dict` methods of models will now properly handle `nullable` and `not required` properties that are themselves generated models (#315). Thanks @forest-benchling!
- Fixed a typo in the async example in generated README.md files (#337). Thanks @synchronizing!
- Fix deserialization of `None` and `Unset` properties for all types by unifying the checks (#334). Thanks @forest-benchling!
- If duplicate model names are detected during generation, you'll now get an error message instead of broken code (#336). Thanks @forest-benchling!
- Fixes `Enum` deserialization when the value is `UNSET` (#306). Thanks @bowenwr!

## 0.7.3 - 2020-12-21

### Fixes

- Spacing and extra returns for Union types of `additionalProperties` (#266 & #268). Thanks @joshzana & @packyg!
- Title of inline schemas will no longer be missing characters (#271 & #274). Thanks @kalzoo!
- Handling of nulls (Nones) when parsing or constructing dates (#267). Thanks @fyhertz!

## 0.7.2 - 2020-12-08

### Fixes

- A bug in handling optional properties that are themselves models (introduced in 0.7.1) (#262). Thanks @packyg!

## 0.7.1 - 2020-12-08

### Additions

- Support for additionalProperties attribute in OpenAPI schemas and "free-form" objects by adding an `additional_properties` attribute to generated models. **COMPATIBILITY NOTE**: this will prevent any model property with a name that would be coerced to "additional_properties" in the generated client from generating properly (#218 & #252). Thanks @packyg!

### Fixes

- Enums will once again work with query parameters (#259). Thanks @packyg!
- Generated Poetry metadata in pyproject.toml will properly indicate Python 3.6 compatibility (#258). Thanks @bowenwr!

## 0.7.0 - 2020-11-25

### Breaking Changes

- Any request/response field that is not `required` and wasn't specified is now set to `UNSET` instead of `None`.

- Values that are `UNSET` will not be sent along in API calls

- Schemas defined with `type=object` will now be converted into classes, just like if they were created as ref components. The previous behavior was a combination of skipping and using generic Dicts for these schemas.

- Response schema handling was unified with input schema handling, meaning that responses will behave differently than before. Specifically, instead of the content-type deciding what the generated Python type is, the schema itself will.

  - As a result of this, endpoints that used to return `bytes` when content-type was application/octet-stream will now return a `File` object if the type of the data is "binary", just like if you were submitting that type instead of receiving it.

- Instead of skipping input properties with no type, enum, anyOf, or oneOf declared, the property will be declared as `None`.

- Class (models and Enums) names will now contain the name of their parent element (if any). For example, a property declared in an endpoint will be named like {endpoint*name}*{previous*class*name}. Classes will no longer be deduplicated by appending a number to the end of the generated name, so if two names conflict with this new naming scheme, there will be an error instead.

### Additions

- Added a `--custom-template-path` option for providing custom jinja2 templates (#231 - Thanks @erichulburd!).
- Better compatibility for "required" (whether or not the field must be included) and "nullable" (whether or not the field can be null) (#205 & #208). Thanks @bowenwr & @emannguitar!
- Support for all the same schemas in responses as are supported in parameters.
- In template macros: added `declare_type` param to `transform` and `initial_value` param to `construct` to improve flexibility (#241 - Thanks @packyg!).

### Fixes

- Fixed spacing and generation of properties of type `Union` in generated models (#241 - Thanks @packyg!).
- Fixed usage instructions in generated README.md (#247 - Thanks @theFong!).

## 0.6.2 - 2020-11-03

### Fixes

- Prefix generated identifiers to allow leading digits in field names (#206 - @kalzoo).
- Prevent autoflake from removing `__init__.py` imports during generation. (#223 - Thanks @fyhertz!)
- Update minimum Pydantic version to support Python 3.9

### Additions

- Allow specifying the generated client's version using `package_version_override` in a config file. (#225 - Thanks @fyhertz!)

## 0.6.1 - 2020-09-26

### Changes

- Use httpx ^0.15.0 in generated clients

### Fixes

- Properly remove spaces from generated Enum keys (#198). Thanks @bowenwr!

### Additions

- Endpoints without operationIds will have a name generated from their method and path (#92). Thanks @Kerybas & @dtkav!
- autoflake will be run on generated clients to clean up unused imports / variables (#138). Thanks @pawamoy!
- Note to README about supported OpenAPI versions (#176). Thanks @filippog!

## 0.6.0 - 2020-09-21

### Breaking Changes

- Reorganized api calls in generated clients. `async_api` will no longer be generated. Each path operation will now have it's own module under its tag. For example, if there was a generated function `api.my_tag.my_function()` it is replaced with `api.my_tag.my_function.sync()`. The async version can be called with `asyncio()` instead of `sync()`. (#167)
- Removed support for mutable default values (e.g. dicts, lists). They may be added back in a future version given enough demand, but the existing implementation was not up to this project's standards. (#170)
- Removed generated `errors` module (and the `ApiResponseError` therein). Instead of raising an exception on failure, the `sync()` and `asyncio()` functions for a path operation will return `None`. This means all return types are now `Optional`, so mypy will require you to handle potential errors (or explicitly ignore them).
- Moved `models.types` generated module up a level, so just `types`.
- All generated classes that were `dataclass` now use the `attrs` package instead

### Additions

- Every generated API module will have a `sync_detailed()` and `asyncio_detailed()` function which work like their non-detailed counterparts, but return a `types.Response[T]` instead of an `Optional[T]` (where T is the parsed body type). `types.Response` contains `status_code`, `content` (bytes of returned content), `headers`, and `parsed` (the parsed return type you would get from the non-detailed function). (#115)
- It's now possible to include custom headers and cookies in requests, as well as set a custom timeout. This can be done either by directly setting those parameters on a `Client` (e.g. `my_client.headers = {"Header": "Value"}`) or using a fluid api (e.g. `my_endpoint.sync(my_client.with_cookies({"MyCookie": "cookie"}).with_timeout(10.0))`).
- Unsupported content types or no responses at all will no longer result in an endpoint being completely skipped. Instead, only the `detailed` versions of the endpoint will be generated, where the resulting `Response.parsed` is always `None`. (#141)
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

- When encountering a problem, the generator will now differentiate between warnings (things it was able to skip past) and errors (things which halt generation altogether).

### Additions

- The generator can now handle many more errors gracefully, skipping the things it can't generate and continuing with the pieces it can.
- Support for Enums declared in "components/schemas" and references to them (#102).
- Generated clients can now be installed via pip (#120).
- Support for YAML OpenAPI documents (#111)

### Internal Changes

- Switched OpenAPI document parsing to use Pydantic based on a vendored version of [openapi-schema-pydantic](https://github.com/kuimono/openapi-schema-pydantic/) (#103).
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

- Classes generated to be included within lists will now be named like <ListName>Item. For example, if a property named "statuses" is an array of enum values, previously the `Enum` class declared would be called "Statuses". Now it will be called "StatusesItem". If a "title" attribute was used in the OpenAPI document, that should still be respected and used instead of the generated name. You can restore previous names by adding "StatusesItem" to the `class_overrides` section of a config file.
- Clients now require httpx ^0.13.0 (up from ^0.12.1). See [httpx release notes](https://github.com/encode/httpx/releases/tag/0.13.0) for details.

### Additions

- Support for binary format strings (file payloads)
- Support for multipart/form bodies
- Support for any supported property within a list (array), including other lists.
- Support for Union types ("anyOf" in OpenAPI document)
- Support for more basic response types (integer, number, boolean)
- Support for duplicate enums. Instead of erroring, enums with the same name (title) but differing values will have a number appended to the end. So if you have two conflicting enums named `MyEnum`, one of them will now be named `MyEnum1`. Note that the order in which these are processed and therefore named is entirely dependent on the order they are read from the OpenAPI document, so changes to the document could result in swapping the names of conflicting Enums.

### Changes

- The way most imports are handled was changed which _should_ lead to fewer unused imports in generated files.

- Better error messages

  - Most error messages will contain some useful information about why it failed instead of a stack trace
  - Client will still be generated if there are recoverable errors, excluding endpoints that had those errors

- Output from isort and black when generating will now be suppressed

### Fixes

- Defaults within models dataclasses for `Dict` or `List` properties will now be properly declared as a `field` with the `default_factory` parameter to prevent errors related to mutable defaults.

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
