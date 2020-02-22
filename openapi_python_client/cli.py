from typing import Optional

import click

from . import main


@click.group()
def cli():
    """ Entrypoint into CLI """
    pass


@cli.command()
@click.option("--url", help="The URL to the openapi.json file")
@click.option("--path", help="The path to the openapi.json file")
def generate(url: Optional[str], path: Optional[str]):
    """ Generate a new OpenAPI Client library """
    if not url and not path:
        print("You must either provide --url or --path")
        exit(1)
    main(url=url, path=path)
