from importlib.metadata import version
from typing import Optional

import click

from . import main


@click.group()
@click.version_option(version(__package__), prog_name="OpenAPI Python Client")
def cli() -> None:
    """ Entrypoint into CLI """
    pass


@cli.command()
@click.option("--url", help="The URL to the openapi.json file")
@click.option("--path", help="The path to the openapi.json file")
def generate(url: Optional[str], path: Optional[str]) -> None:
    """ Generate a new OpenAPI Client library """
    if not url and not path:
        click.secho("You must either provide --url or --path", fg="red")
        exit(1)
    elif url and path:
        click.secho("Provide either --url or --path, not both", fg="red")
        exit(1)
    main(url=url, path=path)
