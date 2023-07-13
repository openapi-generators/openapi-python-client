import codecs
import pathlib
from typing import Optional

import typer

from openapi_python_client import MetaType
from openapi_python_client.config import Config

from openapi_python_client.cli_endpoint_selection import questionary_endpoint_selection

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
    except Exception as err:
        raise typer.BadParameter("Unable to parse config") from err


# noinspection PyUnusedLocal
# pylint: disable=unused-argument
@app.callback(name="openapi-python-client")
def cli(
    version: bool = typer.Option(False, "--version", callback=_version_callback, help="Print the version and exit"),
) -> None:
    """Generate a Python client from an OpenAPI JSON document"""


custom_template_path_options = {
    "help": "A path to a directory containing custom template(s)",
    "file_okay": False,
    "dir_okay": True,
    "readable": True,
    "resolve_path": True,
}

_meta_option = typer.Option(
    MetaType.NONE,
    help="The type of metadata you want to generate.",
)

CONFIG_OPTION = typer.Option(None, "--config", help="Path to the config file to use")


# pylint: disable=too-many-arguments
@app.command()
def init(
    source: str = typer.Argument(None, help="A name of data source for which to generate a pipeline"),
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
    except LookupError as err:
        typer.secho(f"Unknown encoding : {file_encoding}", fg=typer.colors.RED)
        raise typer.Exit(code=1) from err

    config = _process_config(config_path)
    config.project_name_override = source
    config.package_name_override = source
    create_new_client(
        url=url,
        path=path,
        meta=meta,
        custom_template_path=custom_template_path,
        file_encoding=file_encoding,
        config=config,
        endpoint_filter=questionary_endpoint_selection,
    )
