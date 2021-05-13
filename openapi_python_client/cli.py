import codecs
import pathlib
from pprint import pformat
from typing import Optional, Sequence

import typer

from openapi_python_client import MetaType
from openapi_python_client.config import Config
from openapi_python_client.parser.errors import ErrorLevel, GeneratorError, ParseError

app = typer.Typer()


def _version_callback(value: bool) -> None:
    from openapi_python_client import __version__

    if value:
        typer.echo(f"openapi-python-client version: {__version__}")
        raise typer.Exit()


def _process_config(path: Optional[pathlib.Path]) -> Config:

    if not path:
        return Config()

    try:
        return Config.load_from_path(path=path)
    except:  # noqa
        raise typer.BadParameter("Unable to parse config")


# noinspection PyUnusedLocal
@app.callback(name="openapi-python-client")
def cli(
    version: bool = typer.Option(False, "--version", callback=_version_callback, help="Print the version and exit"),
) -> None:
    """Generate a Python client from an OpenAPI JSON document"""
    pass


def _print_parser_error(e: GeneratorError, color: str) -> None:
    typer.secho(e.header, bold=True, fg=color, err=True)
    typer.echo()
    if e.detail:
        typer.secho(e.detail, fg=color, err=True)
        typer.echo()

    if isinstance(e, ParseError) and e.data is not None:
        formatted_data = pformat(e.data)
        typer.secho(formatted_data, fg=color, err=True)

    typer.echo()


def handle_errors(errors: Sequence[GeneratorError], fail_on_warning: bool = False) -> None:
    """Turn custom errors into formatted error messages"""
    if len(errors) == 0:
        return
    error_level = ErrorLevel.WARNING
    message = "Warning(s) encountered while generating. Client was generated, but some pieces may be missing"
    header_color = typer.colors.BRIGHT_YELLOW
    color = typer.colors.YELLOW
    for error in errors:
        if error.level == ErrorLevel.ERROR:
            error_level = ErrorLevel.ERROR
            message = "Error(s) encountered while generating, client was not created"
            color = typer.colors.RED
            header_color = typer.colors.BRIGHT_RED
            break
    typer.secho(
        message,
        underline=True,
        bold=True,
        fg=header_color,
        err=True,
    )
    typer.echo()

    for err in errors:
        _print_parser_error(err, color)

    gh_link = typer.style(
        "https://github.com/triaxtec/openapi-python-client/issues/new/choose", fg=typer.colors.BRIGHT_BLUE
    )
    typer.secho(
        f"If you believe this was a mistake or this tool is missing a feature you need, "
        f"please open an issue at {gh_link}",
        fg=typer.colors.BLUE,
        err=True,
    )

    if error_level == ErrorLevel.ERROR or fail_on_warning:
        raise typer.Exit(code=1)


custom_template_path_options = {
    "help": "A path to a directory containing custom template(s)",
    "file_okay": False,
    "dir_okay": True,
    "readable": True,
    "resolve_path": True,
}

_meta_option = typer.Option(
    MetaType.POETRY,
    help="The type of metadata you want to generate.",
)

CONFIG_OPTION = typer.Option(None, "--config", help="Path to the config file to use")


@app.command()
def generate(
    url: Optional[str] = typer.Option(None, help="A URL to read the JSON from"),
    path: Optional[pathlib.Path] = typer.Option(None, help="A path to the JSON file"),
    custom_template_path: Optional[pathlib.Path] = typer.Option(None, **custom_template_path_options),  # type: ignore
    meta: MetaType = _meta_option,
    file_encoding: str = typer.Option("utf-8", help="Encoding used when writing generated"),
    config_path: Optional[pathlib.Path] = CONFIG_OPTION,
    fail_on_warning: bool = False,
) -> None:
    """Generate a new OpenAPI Client library"""
    from . import create_new_client

    if not url and not path:
        typer.secho("You must either provide --url or --path", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    if url and path:
        typer.secho("Provide either --url or --path, not both", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    try:
        codecs.getencoder(file_encoding)
    except LookupError:
        typer.secho("Unknown encoding : {}".format(file_encoding), fg=typer.colors.RED)
        raise typer.Exit(code=1)

    config = _process_config(config_path)
    errors = create_new_client(
        url=url,
        path=path,
        meta=meta,
        custom_template_path=custom_template_path,
        file_encoding=file_encoding,
        config=config,
    )
    handle_errors(errors, fail_on_warning)


@app.command()
def update(
    url: Optional[str] = typer.Option(None, help="A URL to read the JSON from"),
    path: Optional[pathlib.Path] = typer.Option(None, help="A path to the JSON file"),
    custom_template_path: Optional[pathlib.Path] = typer.Option(None, **custom_template_path_options),  # type: ignore
    meta: MetaType = _meta_option,
    file_encoding: str = typer.Option("utf-8", help="Encoding used when writing generated"),
    config_path: Optional[pathlib.Path] = CONFIG_OPTION,
    fail_on_warning: bool = False,
) -> None:
    """Update an existing OpenAPI Client library"""
    from . import update_existing_client

    if not url and not path:
        typer.secho("You must either provide --url or --path", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    if url and path:
        typer.secho("Provide either --url or --path, not both", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    try:
        codecs.getencoder(file_encoding)
    except LookupError:
        typer.secho("Unknown encoding : {}".format(file_encoding), fg=typer.colors.RED)
        raise typer.Exit(code=1)

    config = _process_config(config_path)
    errors = update_existing_client(
        url=url,
        path=path,
        meta=meta,
        custom_template_path=custom_template_path,
        file_encoding=file_encoding,
        config=config,
    )
    handle_errors(errors, fail_on_warning)
