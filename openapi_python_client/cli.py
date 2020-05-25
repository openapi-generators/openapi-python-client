import pathlib
from contextlib import contextmanager
from pprint import pformat
from typing import Generator, Optional

import typer

from openapi_python_client.openapi_parser.errors import MultipleParseError, ParseError

app = typer.Typer()


def _version_callback(value: bool) -> None:
    from openapi_python_client import __version__

    if value:
        typer.echo(f"openapi-python-client version: {__version__}")
        raise typer.Exit()


def _process_config(path: Optional[pathlib.Path]) -> None:
    from openapi_python_client import load_config

    if not path:
        return

    try:
        load_config(path=path)
    except:
        raise typer.BadParameter("Unable to parse config")


# noinspection PyUnusedLocal
@app.callback(name="openapi-python-client")
def cli(
    version: bool = typer.Option(False, "--version", callback=_version_callback, help="Print the version and exit"),
    config: Optional[pathlib.Path] = typer.Option(
        None, callback=_process_config, help="Path to the config file to use"
    ),
) -> None:
    """ Generate a Python client from an OpenAPI JSON document """
    pass


def _print_parser_error(e: ParseError) -> None:
    formatted_data = pformat(e.data)
    typer.secho(e.header, bold=True, fg=typer.colors.BRIGHT_RED, err=True)
    typer.secho(formatted_data, fg=typer.colors.RED, err=True)
    if e.message:
        typer.secho(e.message, fg=typer.colors.BRIGHT_RED, err=True)
    gh_link = typer.style(
        "https://github.com/triaxtec/openapi-python-client/issues/new/choose", fg=typer.colors.BRIGHT_BLUE
    )
    typer.secho(f"Please open an issue at {gh_link}", fg=typer.colors.RED, err=True)
    typer.secho()


@contextmanager
def handle_errors() -> Generator[None, None, None]:
    """ Turn custom errors into formatted error messages """
    try:
        yield
    except ParseError as e:
        _print_parser_error(e)
        raise typer.Exit(code=1)
    except MultipleParseError as e:
        typer.secho("MULTIPLE ERRORS WHILE PARSING:", underline=True, bold=True, fg=typer.colors.BRIGHT_RED, err=True)
        for err in e.parse_errors:
            _print_parser_error(err)
        raise typer.Exit(code=1)
    except FileExistsError:
        typer.secho("Directory already exists. Delete it or use the update command.", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)


@app.command()
def generate(
    url: Optional[str] = typer.Option(None, help="A URL to read the JSON from"),
    path: Optional[pathlib.Path] = typer.Option(None, help="A path to the JSON file"),
) -> None:
    """ Generate a new OpenAPI Client library """
    from . import create_new_client

    if not url and not path:
        typer.secho("You must either provide --url or --path", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    elif url and path:
        typer.secho("Provide either --url or --path, not both", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    with handle_errors():
        create_new_client(url=url, path=path)


@app.command()
def update(
    url: Optional[str] = typer.Option(None, help="A URL to read the JSON from"),
    path: Optional[pathlib.Path] = typer.Option(None, help="A path to the JSON file"),
) -> None:
    """ Update an existing OpenAPI Client library """
    from . import update_existing_client

    if not url and not path:
        typer.secho("You must either provide --url or --path", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    elif url and path:
        typer.secho("Provide either --url or --path, not both", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    with handle_errors():
        update_existing_client(url=url, path=path)
