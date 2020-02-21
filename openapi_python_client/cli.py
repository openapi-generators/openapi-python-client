import click

from . import main


@click.group()
def cli():
    """ Entrypoint into CLI """
    pass


@cli.command()
@click.option("--url", required=True, help="The URL to the openapi.json file")
def generate(url: str):
    """ Generate a new OpenAPI Client library """
    main(url=url)
