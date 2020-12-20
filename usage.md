# `openapi-python-client`

Generate a Python client from an OpenAPI JSON document 

**Usage**:

```console
$ openapi-python-client [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--version`: Print the version and exit  [default: False]
* `--config PATH`: Path to the config file to use
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `generate`: Generate a new OpenAPI Client library
* `update`: Update an existing OpenAPI Client library

## `openapi-python-client generate`

Generate a new OpenAPI Client library 

**Usage**:

```console
$ openapi-python-client generate [OPTIONS]
```

**Options**:

* `--url TEXT`: A URL to read the JSON from
* `--path PATH`: A path to the JSON file
* `--custom-template-path DIRECTORY`: A path to a directory containing custom template(s)
* `--meta [none|poetry|setup]`: The type of metadata you want to generate.  [default: poetry]
* `--help`: Show this message and exit.

## `openapi-python-client update`

Update an existing OpenAPI Client library 

**Usage**:

```console
$ openapi-python-client update [OPTIONS]
```

**Options**:

* `--url TEXT`: A URL to read the JSON from
* `--path PATH`: A path to the JSON file
* `--custom-template-path DIRECTORY`: A path to a directory containing custom template(s)
* `--meta [none|poetry|setup]`: The type of metadata you want to generate.  [default: poetry]
* `--help`: Show this message and exit.

