import pathlib
from typing import Optional

import typer

from . import main

app = typer.Typer()


@app.callback()
def cli() -> None:
    """ Generate a Python client from an OpenAPI JSON document """
    pass


@app.command()
def generate(
    url: Optional[str] = typer.Option(None, help="A URL to read the JSON from"),
    path: Optional[pathlib.Path] = typer.Option(None, help="A path to the JSON file"),
) -> None:
    """ Generate a new OpenAPI Client library """
    if not url and not path:
        typer.secho("You must either provide --url or --path", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    elif url and path:
        typer.secho("Provide either --url or --path, not both", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    main(url=url, path=path)
