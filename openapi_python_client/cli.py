import pathlib
from typing import Optional

import typer

app = typer.Typer()


def _version_callback(value: bool) -> None:
    from openapi_python_client import __version__

    if value:
        typer.echo(f"openapi-python-client version: {__version__}")
        raise typer.Exit()


# noinspection PyUnusedLocal
@app.callback(name="openapi-python-client")
def cli(
    version: bool = typer.Option(False, "--version", callback=_version_callback, help="Print the version and exit"),
) -> None:
    """ Generate a Python client from an OpenAPI JSON document """
    pass


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
    update_existing_client(url=url, path=path)
