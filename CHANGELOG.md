# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Breaking changes to any of the following will cause the **minor** version to be incremented (as long as this project is 0.x). Only these pieces are considered part of the public API:

- The _behavior_ of the generated code. Specifically, the way in which generated endpoints and classes are called and the way in which those calls communicate with an OpenAPI server. Any other property of the generated code is not considered part of the versioned, public API (e.g., code formatting, comments).
- The invocation of the CLI (e.g., commands or arguments).

Programmatic usage of this project (e.g., importing it as a Python module) and the usage of custom templates are not considered part of the public API and therefore may change behavior at any time without notice.

The 0.x prefix used in versions for this project is to indicate that breaking changes are expected frequently (several times a year). Breaking changes will increment the minor number, all other changes will increment the patch number. You can track the progress toward 1.0 [here](https://github.com/openapi-generators/openapi-python-client/projects/2).

## 0.23.0 (2024-12-24)

### Breaking Changes

#### Delete fewer files with `--overwrite`

`--overwrite` will no longer delete the entire output directory before regenerating. Instead, it will only delete 
specific, known directories within that directory. Right now, that is only the generated `models` and `api` directories.

Other generated files, like `README.md`, will be overwritten. Extra files and directories outside of those listed above 
will be left untouched, so you can any extra modules or files around while still updating `pyproject.toml` automatically.

Closes #1105.

### Features

- Support httpx 0.28 (#1172)

#### Add `generate_all_tags` config option

You can now, optionally, generate **duplicate** endpoint functions/modules using _every_ tag for an endpoint,
not just the first one, by setting `generate_all_tags: true` in your configuration file.

### Fixes

- Support Typer 0.14 and 0.15 (#1173)

#### Fix minimum `attrs` version

The minimum `attrs` dependency version was incorrectly set to 21.3.0. This has been corrected to 22.2.0, the minimum 
supported version since `openapi-python-client` 0.19.1.

Closes #1084, thanks @astralblue!

#### Fix compatibility with Pydantic 2.10+

##1176 by @Viicos

Set `defer_build` to models that we know will fail to build, and call `model_rebuild`
in the `__init__.py` file.

## 0.22.0 (2024-11-23)

### Breaking Changes

#### Drop support for Python 3.8

Python 3.8 is no longer supported. "New" 3.9 syntax, like generics on builtin collections, is used both in the generator 
and the generated code.

#### `type` is now a reserved field name

Because `type` is used in type annotations now, it is no longer a valid field name. Fields which were previously named 
`type` will be renamed to `type_`.

### Features

- Support Ruff 0.8 (#1169)

## 0.21.7 (2024-10-28)

### Fixes

- allow required fields list to be specified as empty (#651) (#1149)
- import cast for required const properties, since it's used in the template (#1153)

## 0.21.6 (2024-10-20)

### Features

- update Ruff to >=0.2,<0.8 (#1137)
- Add UUID string format. Thanks @estyrke! (#1140)
- Support OpenAPI 3.1 prefixItems property for arrays. Thanks @estyrke! (#1141)

#### Add `literal_enums` config setting

Instead of the default `Enum` classes for enums, you can now generate `Literal` sets wherever `enum` appears in the OpenAPI spec by setting `literal_enums: true` in your config file.

```yaml
literal_enums: true
```

Thanks to @emosenkis for PR #1114 closes #587, #725, #1076, and probably many more. 
Thanks also to @eli-bl, @expobrain, @theorm, @chrisguillory, and anyone else who helped getting to this design!

### Fixes

- Typo in docstring (#1128)

#### Use literal value instead of `HTTPStatus` enum when checking response statuses

Python 3.13 renamed some of the `HTTPStatus` enum members, which means clients generated with Python 3.13 may not work 
with older versions of Python. This change stops using the `HTTPStatus` enum directly when checking response statuses.

Statuses will still be checked for validity at generation time, and transformed into `HTTPStatus` _after_ being checked 
at runtime.

This may cause some linters to complain.

## 0.21.5 (2024-09-07)

### Features

#### Improved property-merging behavior with `allOf`

When using `allOf` to extend a base object type, `openapi-python-client` is now able to handle some kinds of modifications to an existing property that would have previously caused an error:

- Overriding attributes that do not affect validation, such as `description`.
- Combining properties that this generator ignores, like `maxLength` or `pattern`.
- Combining a generic numeric type with `int` (resulting in `int`).
- Adding a `format` to a string.
- Combining `any` with a specific type (resulting in that specific type).
- Adding or overriding a `default`

> [!NOTE]
> `pattern` and `max_length` are no longer fields on `StringProperty`, which may impact custom templates.

This also fixes a bug where properties of inline objects (as opposed to references) were not using the
merge logic, but were simply overwriting previous definitions of the same property.

### Fixes

- Allow default values for properties of `Any` type

#### Produce valid code for an object that has no properties at all

Fixed by PR #1109. Thanks @eli-bl!

## 0.21.4 (2024-08-25)

### Fixes

#### Allow OpenAPI 3.1-style `exclusiveMinimum` and `exclusiveMaximum`

Fixed by PR #1092. Thanks @mikkelam!

#### Add missing `cast` import when using `const`

Fixed by PR #1072. Thanks @dorcohe!

#### Correctly resolve references to a type that is itself just a single allOf reference

PR #1103 fixed issue #1091. Thanks @eli-bl!

#### Support `const` booleans and floats

Fixed in PR #1086. Thanks @flxdot!

## 0.21.3 (2024-08-18)

### Features

- update Ruff to >=0.2,<0.7 (#1097)

## 0.21.2 (2024-07-20)

### Features

- Update to Ruff 0.5

## 0.21.1 (2024-06-15)

### Features

#### Support request body refs

You can now define and reuse bodies via refs, with a document like this:

```yaml
paths:
  /something:
    post:
      requestBody:
        "$ref": "#/components/requestBodies/SharedBody"
components:
  requestBodies:
    SharedBody:
      content:
        application/json:
          schema:
            type: string
```

Thanks to @kigawas and @supermihi for initial implementations and @RockyMM for the initial request.

Closes #633, closes #664, resolves #595.

### Fixes

- Indent of generated code for non-required lists. Thanks @sfowl! (#1050)
- Parsing requestBody with $ref (#633)

## 0.21.0 (2024-06-08)

### Breaking Changes

#### Removed the `update` command

The `update` command is no more, you can (mostly) replace its usage with some new flags on the `generate` command.

If you had a package named `my-api-client` in the current working directory, the `update` command previously would update the `my_api_client` module within it. You can now _almost_ perfectly replicate this behavior using `openapi-python-client generate --meta=none --output-path=my-api-client/my_api_client --overwrite`.

The only difference is that `my-api-client` would have run `post_hooks` in the `my-api-client` directory, 
but `generate` will run `post_hooks` in the `output-path` directory.

Alternatively, you can now also run `openapi-python-client generate --meta=<your-meta-type> --overwrite` to regenerate 
the entire client, if you don't care about keeping any changes you've made to the generated client.

Please comment on [discussion #824](https://github.com/openapi-generators/openapi-python-client/discussions/824)
(or a new discussion, as appropriate) to aid in designing future features that fill any gaps this leaves for you.

### Features

#### Added an `--output-path` option to `generate`

Rather than changing directories before running `generate` you can now specify an output directory with `--output-path`.
Note that the project name will _not_ be appended to the `--output-path`, whatever path you specify is where the 
generated code will be placed.

#### Added an `--overwrite` flag to `generate`

You can now tell `openapi-python-client` to overwrite an existing directory, rather than deleting it yourself before 
running `generate`.

## 0.20.0 (2024-05-18)

### Breaking Changes

#### `const` values in responses are now validated at runtime

Prior to this version, `const` values returned from servers were assumed to always be correct. Now, if a server returns 
an unexpected value, the client will raise a `ValueError`. This should enable better usage with `oneOf`.

PR #1024. Thanks @peter-greenatlas!

#### Switch YAML parsing to 1.2

This change switches the YAML parsing library to `ruamel.yaml` which follows the YAML 1.2 specification. 
[There are breaking changes](https://yaml.readthedocs.io/en/latest/pyyaml/#defaulting-to-yaml-12-support) from YAML 1.1 to 1.2,
though they will not affect most use cases.

PR #1042 fixes #1041. Thanks @rtaycher!

### Features

- allow Ruff 0.4 (#1031)

### Fixes

#### Fix nullable and required properties in multipart bodies

Fixes #926.

> [!WARNING]
> This change is likely to break custom templates. Multipart body handling has been completely split from JSON bodies.

## 0.19.1 (2024-03-27)

### Features

#### Add config option to override content types

You can now define a `content_type_overrides` field in your `config.yml`:

```yaml
content_type_overrides:
  application/zip: application/octet-stream
```

This allows `openapi-python-client` to generate code for content types it doesn't recognize.

PR #1010 closes #810. Thanks @gaarutyunov!

### Fixes

#### Add aliases to `Client` for pyright

This should resolve incompatibilities between the generated `Client` class and the pyright type checker.

PR #1009 closes #909. Thanks @patrick91!

## 0.19.0 (2024-03-06)

### Breaking Changes

#### Update PDM metadata syntax

Metadata generated for PDM will now use the new `distribution = true` syntax instead of `package-type = "library"`. 
New packages generated with `--meta pdm` will require PDM `2.12.0` or later to build. 

### Features

#### Add response content to `UnexpectedStatus` exception

The error message for `UnexpectedStatus` exceptions will now include the UTF-8 decoded (ignoring errors) body of the response.

PR #989 implements #840. Thanks @harabat!

### Fixes

#### Allow hyphens in path parameters

Before now, path parameters which were invalid Python identifiers were not allowed, and would fail generation with an
"Incorrect path templating" error. In particular, this meant that path parameters with hyphens were not allowed.
This has now been fixed!

PR #986 fixed issue #976. Thanks @harabat!

> [!WARNING]
> This change may break custom templates, see [this diff](https://github.com/openapi-generators/openapi-python-client/pull/986/files#diff-0de8437b26075d8fe8454cf47d8d95d4835c7f827fa87328e03f690412be803e)
> if you have trouble upgrading.

## 0.18.0 (2024-02-22)

### Breaking Changes

#### For custom templates, changed type of endpoint parameters

**This does not affect projects that are not using `--custom-template-path`**

The type of these properties on `Endpoint` has been changed from `Dict[str, Property]` to `List[Property]`:

- `path_parameters`
- `query_parameters`
- `header_parameters`
- `cookie_parameters`

If your templates are very close to the default templates, you can probably just remove `.values()` anywhere it appears.

The type of `iter_all_parameters()` is also different, you probably want `list_all_parameters()` instead.

#### Updated generated config for Ruff v0.2

This only affects projects using the `generate` command, not the `update` command. The `pyproject.toml` file generated which configures Ruff for linting and formatting has been updated to the 0.2 syntax, which means it will no longer work with Ruff 0.1.

#### Updated naming strategy for conflicting properties

While fixing #922, some naming strategies were updated. These should mostly be backwards compatible, but there may be 
some small differences in generated code. Make sure to check your diffs before pushing updates to consumers!

### Features

#### support httpx 0.27 (#974)

### Fixes

#### Allow parameters with names differing only by case

If you have two parameters to an endpoint named `mixedCase` and `mixed_case`, previously, this was a conflict and the endpoint would not be generated.
Now, the generator will skip snake-casing the parameters and use the names as-is. Note that this means if neither of the parameters _was_ snake case, neither _will be_ in the generated code.

Fixes #922 reported by @macmoritz & @benedikt-bartscher.

#### Fix naming conflicts with properties in models with mixed casing

If you had an object with two properties, where the names differed only by case, conflicting properties would be generated in the model, which then failed the linting step (when using default config). For example, this:

```yaml
type: "object"
properties:
  MixedCase:
    type: "string"
  mixedCase:
    type: "string"
```

Would generate a class like this:

```python
class MyModel:
    mixed_case: str
    mixed_case: str
```

Now, neither of the properties will be forced into snake case, and the generated code will look like this:

```python
class MyModel:
    MixedCase: str
    mixedCase: str
```

## 0.17.3 (2024-02-20)

### Fixes

#### Remove spurious field_dict.update({}) for types without properties (#969)

#### Fix invalid type check for nested unions

Nested union types (unions of unions) were generating `isinstance()` checks that were not valid (at least for Python 3.9).

Thanks to @codebutler for PR #959 which fixes #958 and #967.

## 0.17.2 (2024-01-15)

### Features

#### Add `--meta=pdm` option for generating PEP621 + PDM metadata

The default metadata is still `--meta=poetry`, which generates a `pyproject.toml` file with Poetry-specific metadata.
This change adds the `--meta=pdm` option which includes [PDM](https://pdm-project.org/latest/)-specific metadata, but also 
standard [PEP621](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#writing-pyproject-toml)
metadata. This may be useful as a starting point for other dependency managers & build tools (like Hatch).

#### Add original OpenAPI `data` attribute to `Response` object

PR #767

In custom templates, you can now access a `response.data` attribute that contains the original OpenAPI definition of the
response (Response Object or Reference Object).

#### Include the `UP` rule for generated Ruff config

This enables [pyupgrade-like improvements](https://docs.astral.sh/ruff/rules/#pyupgrade-up) which should replace some 
`.format()` calls with f-strings.

### Fixes

#### Fix Ruff formatting for `--meta=none`

PR #940 fixes issue #939. Thanks @satwell!

Due to the lack of `pyproject.toml`, Ruff was not getting configured properly when `--meta=none`.
As a result, it didn't clean up common generation issues like duplicate imports, which would then cause errors from 
linters.

This is now fixed by changing the default `post_hook` to `ruff check . --fix --extend-select=I` when `--meta=none`.
Using `generate --meta=none` should now be almost identical to the code generated by `update`.

## 0.17.1 (2024-01-04)

### Features

#### Export `Unset` types from generated `types.py` (#927)

#### Generate properties for some boolean enums

If a schema has both `type = "boolean"` and `enum` defined, a normal boolean property will now be created. 
Previously, the generator would error. 

Note that the generate code _will not_ correctly limit the values to the enum values. To work around this, use the 
OpenAPI 3.1 `const` instead of `enum` to generate Python `Literal` types.

Thanks for reporting #922 @macmoritz!

### Fixes

#### Do not stop generation for invalid enum values

This generator only supports `enum` values that are strings or integers. 
Previously, this was handled at the parsing level, which would cause the generator to fail if there were any unsupported values in the document.
Now, the generator will correctly keep going, skipping only endpoints which contained unsupported values.

Thanks for reporting #922 @macmoritz!

#### Fix lists within unions

Fixes #756 and #928. Arrays within unions (which, as of 0.17 includes nullable arrays) would generate invalid code.

Thanks @kgutwin and @diesieben07!

#### Simplify type checks for non-required unions

## 0.17.0 (2023-12-31)

### Breaking Changes

#### Removed query parameter nullable/required special case

In previous versions, setting _either_ `nullable: true` or `required: false` on a query parameter would act like both were set, resulting in a type signature like `Union[None, Unset, YourType]`. This special case has been removed, query parameters will now act like all other types of parameters.

#### Renamed body types and parameters

PR #900 addresses #822.

Where previously there would be one body parameter per supported content type, now there is a single `body` parameter which takes a union of all the possible inputs. This correctly models the fact that only one body can be sent (and ever would be sent) in a request.

For example, when calling a generated endpoint, code which used to look like this:

```python
post_body_multipart.sync_detailed(
    client=client,
    multipart_data=PostBodyMultipartMultipartData(),
)
```

Will now look like this:

```python
post_body_multipart.sync_detailed(
    client=client,
    body=PostBodyMultipartBody(),
)
```

Note that both the input parameter name _and_ the class name have changed. This should result in simpler code when there is only a single body type and now produces correct code when there are multiple body types.

### Features

#### OpenAPI 3.1 support

The generator will now attempt to generate code for OpenAPI documents with versions 3.1.x (previously, it would exit immediately on seeing a version other than 3.0.x). The following specific OpenAPI 3.1 features are now supported:

- `null` as a type
- Arrays of types (e.g., `type: [string, null]`)
- `const` (defines `Literal` types)

The generator does not currently validate that the OpenAPI document is valid for a specific version of OpenAPI, so it may be possible to generate code for documents that include both removed 3.0 syntax (e.g., `nullable`) and new 3.1 syntax (e.g., `null` as a type).

Thanks to everyone who helped make this possible with discussions and testing, including:

- @frco9
- @vogre
- @naddeoa
- @staticdev
- @philsturgeon
- @johnthagen

#### Support multiple possible `requestBody`

PR #900 addresses #822.

It is now possible in some circumstances to generate valid code for OpenAPI documents which have multiple possible `requestBody` values. Previously, invalid code could have been generated with no warning (only one body could actually be sent).

Only one content type per "category" is currently supported at a time. The categories are:

- JSON, like `application/json`
- Binary data, like `application/octet-stream`
- Encoded form data, like `application/x-www-form-urlencoded`
- Files, like `multipart/form-data`

### Fixes

#### Always use correct content type for requests

In previous versions, a request body that was similar to a known content type would use that content type in the request. For example `application/json` would be used for `application/vnd.api+json`. This was incorrect and could result in invalid requests being sent.

Now, the content type defined in the OpenAPI document will always be used.

## 0.16.1 (2023-12-23)

### Features

#### Support httpx 0.26 (#913)

## 0.16.0 (2023-12-07)

### Breaking Changes

#### Switch from Black to Ruff for formatting

`black` is no longer a runtime dependency, so if you have them set in custom `post_hooks` in a config file, you'll need to make sure they're being installed manually. [`ruff`](https://docs.astral.sh/ruff) is now installed and used by default instead.

#### Use Ruff instead of isort + autoflake at runtime

`isort` and `autoflake` are no longer runtime dependencies, so if you have them set in custom `post_hooks` in a config file, you'll need to make sure they're being installed manually. [`ruff`](https://docs.astral.sh/ruff) is now installed and used by default instead.

### Features

#### Support all `text/*` content types in responses

Within an API response, any content type which starts with `text/` will now be treated the same as `text/html` already was—they will return the `response.text` attribute from the [httpx Response](https://www.python-httpx.org/api/#response).

Thanks to @fdintino for the initial implementation, and thanks for the discussions from @kairntech, @rubenfiszel, and @antoneladestito.

Closes #797 and #821.

#### Support `application/octet-stream` request bodies

Endpoints that accept `application/octet-stream` request bodies are now supported using the same `File` type as octet-stream responses.

Thanks to @kgutwin for the implementation and @rtaycher for the discussion!

PR #899 closes #588

### Fixes

#### Remove useless `pass` statements from generated code

## 0.15.2 (2023-09-16)

### Features

#### support httpx 0.25 (#854)

#### Support content-type with attributes (#655, #809, #858). Thanks @sherbang!

## 0.15.1 (2023-08-12)

### Features

#### Upgrade internal Pydantic use to v2. Thanks @KristinnVikar! (#779)

### Fixes

#### Naming conflicts when properties are named "field" or "define" (#781, #793). Thanks @david-dotorigin

## 0.15.0 (2023-07-23)

### Breaking Changes

#### Minimum httpx version raised to 0.20

Some features of generated clients already failed at runtime when using httpx < 0.20, but now the minimum version is enforced at generation time.

#### Connections from clients no longer automatically close (PR [#775](https://github.com/openapi-generators/openapi-python-client/pull/775))

`Client` and `AuthenticatedClient` now reuse an internal [`httpx.Client`](https://www.python-httpx.org/advanced/#client-instances) (or `AsyncClient`)—keeping connections open between requests. This will improve performance overall, but may cause resource leaking if clients are not closed properly. The new clients are intended to be used via context managers—though for compatibility they don't _have_ to be used with context managers. If not using a context manager, connections will probably leak. Note that once a client is closed (by leaving the context manager), it can no longer be used—and attempting to do so will raise an exception.

APIs should now be called like:

```python
with client as client:
    my_api.sync(client)
    another_api.sync(client)
# client is closed here and can no longer be used
```

Generated READMEs reflect the new syntax, but READMEs for existing generated clients should be updated manually. See [this diff](https://github.com/openapi-generators/openapi-python-client/pull/775/files#diff-62b50316369f84439d58f4981c37538f5b619d344393cb659080dadbda328547) for inspiration.

#### Generated clients and models now use the newer attrs `@define` and `field` APIs

See [the attrs docs](https://www.attrs.org/en/stable/names.html#attrs-tng) for more information on how these may affect you.

#### Removed public attributes for `Client` and `AuthenticatedClient`

The following attributes have been removed from `Client` and `AuthenticatedClient`:

- `base_url`—this can now only be set via the initializer
- `cookies`—set at initialization or use `.with_cookies()`
- `headers`—set at initialization or use `.with_headers()`
- `timeout`—set at initialization or use `.with_timeout()`
- `verify_ssl`—this can now only be set via the initializer
- `follow_redirects`—this can now only be set via the initializer

#### The `timeout` param and `with_timeout` now take an `httpx.Timeout` instead of a float

#### `AuthenticatedClient` no longer inherits from `Client`

The API of `AuthenticatedClient` is still a superset of `Client`, but the two classes no longer share a common base class.

### Features

#### Allow customizing the underlying `httpx` clients

There are many use-cases where customizing the underlying `httpx` client directly is necessary. Some examples are:

- [Event hooks](https://www.python-httpx.org/advanced/#event-hooks)
- [Proxies](https://www.python-httpx.org/advanced/#http-proxying)
- [Custom authentication](https://www.python-httpx.org/advanced/#customizing-authentication)
- [Retries](https://www.python-httpx.org/advanced/#usage_1)

The new `Client` and `AuthenticatedClient` classes come with several methods to customize underlying clients. You can pass arbitrary arguments to `httpx.Client` or `httpx.AsyncClient` when they are constructed:

```python
client = Client(base_url="https://api.example.com", httpx_args={"proxies": {"https://": "https://proxy.example.com"}})
```

**The underlying clients are constructed lazily, only when needed. `httpx_args` are stored internally in a dictionary until the first request is made.**

You can force immediate construction of an underlying client in order to edit it directly:

```python
import httpx
from my_api import Client

client = Client(base_url="https://api.example.com")
sync_client: httpx.Client = client.get_httpx_client()
sync_client.timeout = 10
async_client = client.get_async_httpx_client()
async_client.timeout = 15
```

You can also completely override the underlying clients:

```python
import httpx
from my_api import Client

client = Client(base_url="https://api.example.com")
# The params you put in here ^ are discarded when you call set_httpx_client or set_async_httpx_client
sync_client = httpx.Client(base_url="https://api.example.com", timeout=10)
client.set_httpx_client(sync_client)
async_client = httpx.AsyncClient(base_url="https://api.example.com", timeout=15)
client.set_async_httpx_client(async_client)
```

#### Clients now reuse connections between requests

This happens every time you use the same `Client` or `AuthenticatedClient` instance for multiple requests, however it is best to use a context manager (e.g., `with client as client:`) to ensure the client is closed properly.

### Fixes

#### Stop showing Poetry instructions in generated READMEs when not appropriate

## 0.14.1

### Fixes

- Allow parameters named "client" and "url" [#758, #762, #765]. Thanks @truenicoco & @juanber84!

## 0.14.0

### Breaking Changes

- Drop support for Python 3.7, put minimum version limit on Black (#754)

### Features

- Better typing (mypy) support for `Unset` (e.g., using if statements to check type) [#714, #752]. Thanks @taasan & @mcclurem! (#752)

### Fixes

- pyproject_no_poetry.toml.jinja template can be used to configure black and isort (closes #750) (#751)

## 0.13.4

### Features

- support httpx 0.24 (#746)

## 0.13.3

### Features

- Extend the UnexpectedStatus exception to include the response's content (#729)
- Added support of follow HTTP redirects (#724). Thanks @expobrain & @emann!

### Fixes

- Parsing endpoint content types with semicolon separator (#727). Thanks @expobrain!
- Remove Response[] from docstring of non-detailed functions (#741). Thanks @robertschweizer!

## 0.13.2

### Features

- Always generate enums with sorted members (#728)

### Fixes

- Prevent backslashes in descriptions from breaking docstrings [#735]. Thanks @robertschweizer & @bryan-hunt! (#735)
- Respect `required` field in parameters included with `$ref` (#737)

## 0.13.1

### Features

- Add `http_timeout` config to set timeout getting document via `--url` [#718]. Thanks @Kircheneer!

## 0.13.0

### Breaking Changes

- run `post_hooks` in package directory instead of current directory if meta=none [#696, #697]. Thanks @brenmous and @wallagib!
- Treat leading underscore as a sign of invalid identifier [#703]. Thanks @maxkomarychev!

### Fixes

- generated docstring for `Client.get_headers` function [#713]. Thanks @rtaycher!

## 0.12.3

### Features

- Add `raise_on_unexpected_status` flag to generated `Client` [#593]. Thanks @JamesHinshelwood, @ramnes, @gwenshap, @theFong!
- add `use_path_prefixes_for_title_model_names` config option for simpler model names [#559, #560]. Thanks @rtaycher!
- Support any content type ending in `+json` [#706, #709]. Thanks @XioNoX and @mtovt!

## 0.12.2

### Fixes

- Support Python 3.11.0 (#701)

## 0.12.1

### Fixes

- Version bump due to PyPI error

## 0.12.0

### Breaking Changes

- Change the `Response.status_code` type to the `HTTPStatus` enum [#665]

### Features

- Add `endpoint_collections_by_tag` and `openapi` to the templating globals [#689]. Thanks @paulo-raca!
- Support for recursive and circular references using lazy imports [#670, #338, #466]. Thanks @maz808 & @mtovt!
- Include `__all__` in generated `__init__.py` files [#676, #631, #540, #675]. Thanks @EltonChou!

### Fixes

- If data.type is None but has data.properties, assume type is object [#691, #674]. Thanks @ahuang11!

## 0.11.6

### Features

- improve the error message when parsing a response fails [#659]. Thanks @supermihi!
- Authorization header can now be customized in AuthenticatedClient [#660]. Thanks @supermihi!
- Support inlined form data schema in requestBody [#656, #662]. Thanks @supermihi!
- Allow enums in headers [#663, #667]. Thanks @supermihi!

### Fixes

- Exception when parsing documents which contain callbacks [#661]. Thanks @dachucky!

## 0.11.5

### Features

- support `#/components/parameters` references [#288, #615, #653]. Thanks @jsanchez7SC!

### Fixes

- Keep trailing newlines in generated files [#646, #654]. Thanks @eliask!

## 0.11.4

### Fixes

- Invalid code generation with some `oneOf` and `anyOf` combinations [#603, #642]. Thanks @jselig-rigetti!
- Allow relative references in all URLs [#630]. Thanks @jtv8!

## 0.11.3

### Fixes

- Allow tokenUrl to be relative [#618]. Thanks @Fokko!

## 0.11.2

### Features

- Allow httpx 0.23.x (#617)

### Fixes

- typos in generated README (#586). Thanks @adelevie!

## 0.11.1

### Features

- Allow httpx 0.22.\* (#577)

### Fixes

- Type annotations for optional dates and datetimes in multipart/form (#580)
- Error generating clients with dates or datetimes in multipart/form [#579]. Thanks @lsaavedr!
- Include nested packages in generated setup.py [#575, #576]. Thanks @tedo-benchling!

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
