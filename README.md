![Run Checks](https://github.com/openapi-generators/openapi-python-client/workflows/Run%20Checks/badge.svg)
[![codecov](https://codecov.io/gh/openapi-generators/openapi-python-client/branch/main/graph/badge.svg)](https://codecov.io/gh/triaxtec/openapi-python-client)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![Generic badge](https://img.shields.io/badge/type_checked-mypy-informational.svg)](https://mypy.readthedocs.io/en/stable/introduction.html)
[![PyPI version shields.io](https://img.shields.io/pypi/v/openapi-python-client.svg)](https://pypi.python.org/pypi/openapi-python-client/)
[![Downloads](https://static.pepy.tech/personalized-badge/openapi-python-client?period=total&units=international_system&left_color=blue&right_color=green&left_text=Downloads)](https://pepy.tech/project/openapi-python-client)

# openapi-python-client

Generate modern Python clients from OpenAPI 3.0 and 3.1 documents.

_This generator does not support OpenAPI 2.x FKA Swagger. If you need to use an older document, try upgrading it to
version 3 first with one of many available converters._

**This project is still in development and does not support all OpenAPI features**

## Why This?

This tool focuses on creating the best developer experience for Python developers by:

1. Using all the latest and greatest Python features like type annotations and dataclasses.
2. Having documentation and usage instructions specific to this one generator.
3. Being written in Python with Jinja2 templates, making it easier to improve and extend for Python developers. It's also much easier to install and use if you already have Python.

## Installation

I recommend you install with [pipx](https://pipxproject.github.io/pipx/) so you don't conflict with any other packages you might have: `pipx install openapi-python-client --include-deps`.

> Note the `--include-deps` option makes `ruff` available in your path so that `openapi-python-client` can use it to clean up the generated code.

**If you use `pipx run` then the post-generation hooks will not be available unless you install them manually.**

You can also install with normal pip: `pip install openapi-python-client`

Then, if you want tab completion: `openapi-python-client --install-completion`

## Usage

### Create a new client

`openapi-python-client generate --url https://my.api.com/openapi.json`

This will generate a new client library named based on the title in your OpenAPI spec. For example, if the title
of your API is "My API", the expected output will be "my-api-client". If a folder already exists by that name, you'll
get an error.

If you have an `openapi.json` file available on disk, in any CLI invocation you can build off that instead by replacing `--url` with a `--path`:

`openapi-python-client generate --path location/on/disk/openapi.json`

### Update an existing client

`openapi-python-client update --url https://my.api.com/openapi.json`

### Using custom templates

This feature leverages Jinja2's [ChoiceLoader](https://jinja.palletsprojects.com/en/2.11.x/api/#jinja2.ChoiceLoader) and [FileSystemLoader](https://jinja.palletsprojects.com/en/2.11.x/api/#jinja2.FileSystemLoader). This means you do _not_ need to customize every template. Simply copy the template(s) you want to customize from [the default template directory](openapi_python_client/templates) to your own custom template directory (file names _must_ match exactly) and pass the template directory through the `custom-template-path` flag to the `generate` and `update` commands. For instance,

```
openapi-python-client update \
  --url https://my.api.com/openapi.json \
  --custom-template-path=relative/path/to/mytemplates
```

_Be forewarned, this is a beta-level feature in the sense that the API exposed in the templates is undocumented and unstable._

## What You Get

1. A `pyproject.toml` file, optionally with [Poetry] metadata (default), [PDM] (with `--meta=pdm`), or only [Ruff] config.
2. A `README.md` you'll most definitely need to update with your project's details
3. A Python module named just like the auto-generated project name (e.g. "my_api_client") which contains:
   1. A `client` module which will have both a `Client` class and an `AuthenticatedClient` class. You'll need these
      for calling the functions in the `api` module.
   2. An `api` module which will contain one module for each tag in your OpenAPI spec, as well as a `default` module
      for endpoints without a tag. Each of these modules in turn contains one function for calling each endpoint.
   3. A `models` module which has all the classes defined by the various schemas in your OpenAPI spec
4. A `setup.py` file _if_ you use `--meta=setup` (default is `--meta=poetry`)

For a full example you can look at the `end_to_end_tests` directory which has `baseline_openapi_3.0.json` and `baseline_openapi_3.1.yaml` files.
The "golden-record" in that same directory is the generated client from either of those OpenAPI documents.

## Configuration

You can pass a YAML (or JSON) file to openapi-python-client with the `--config` option in order to change some behavior.
The following parameters are supported:

### class_overrides

Used to change the name of generated model classes. This param should be a mapping of existing class name
(usually a key in the "schemas" section of your OpenAPI document) to class_name and module_name. As an example, if the
name of a model in OpenAPI (and therefore the generated class name) was something like "_PrivateInternalLongName"
and you want the generated client's model to be called "ShortName" in a module called "short_name" you could do this:

Example:

```yaml
class_overrides:
  _PrivateInternalLongName:
    class_name: ShortName
    module_name: short_name
```

The easiest way to find what needs to be overridden is probably to generate your client and go look at everything in the `models` folder.

### project_name_override and package_name_override

Used to change the name of generated client library project/package. If the project name is changed but an override for the package name
isn't provided, the package name will be converted from the project name using the standard convention (replacing `-`'s with `_`'s).

Example:

```yaml
project_name_override: my-special-project-name
package_name_override: my_extra_special_package_name
```

### field_prefix

When generating properties, the `name` attribute of the OpenAPI schema will be used. When the `name` is not a valid Python identifier (e.g. begins with a number) this string will be prepended. Defaults to "field\_". It will also be used to prefix fields in schema starting with "_" in order to avoid ambiguous semantics.

Example:

```yaml
field_prefix: attr_
```

### package_version_override

Specify the package version of the generated client. If unset, the client will use the version of the OpenAPI spec.

Example:

```yaml
package_version_override: 1.2.3
```

### post_hooks

In the config file, there's an easy way to tell `openapi-python-client` to run additional commands after generation. Here's an example showing the default commands (using [Ruff]) that will run if you don't override them in config:

```yaml
post_hooks:
   - "ruff check . --fix"
   - "ruff format ."
```

### use_path_prefixes_for_title_model_names

By default, `openapi-python-client` generates class names which include the full path to the schema, including any parent-types. This can result in very long class names like `MyRouteSomeClassAnotherClassResponse`—which is very unique and unlikely to cause conflicts with future API additions, but also super verbose.

If you are carefully curating your `title` properties already to ensure no duplicate class names, you can turn off this prefixing feature by setting `use_path_prefixes_for_title_model_names` to `false` in your config file. This will use the `title` property of any object that has it set _without_ prefixing.

If this option results in conflicts, you will need to manually override class names instead via the `class_overrides` option.

### http_timeout

By default, the timeout for retrieving the schema file via HTTP is 5 seconds. In case there is an error when retrieving the schema, you might try and increase this setting to a higher value.

### content_type_overrides

Normally, `openapi-python-client` will skip any bodies or responses that it doesn't recognize the content type for.
This config tells the generator to treat a given content type like another.

```yaml
content_type_overrides:
  application/zip: application/octet-stream
```

[changelog.md]: CHANGELOG.md
[poetry]: https://python-poetry.org/
[PDM]: https://pdm-project.org/latest/
[Ruff]: https://docs.astral.sh/ruff/
