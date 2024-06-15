import codecs
from pathlib import Path
from pprint import pformat
from typing import Optional, Sequence, Union

import typer

from openapi_python_client import MetaType
from openapi_python_client.config import Config, ConfigFile
from openapi_python_client.parser.errors import ErrorLevel, GeneratorError, ParseError

app = typer.Typer()


def _version_callback(value: bool) -> None:
    from openapi_python_client import __version__

    if value:
        typer.echo(f"openapi-python-client version: {__version__}")
        raise typer.Exit()


def _process_config(
    *,
    url: Optional[str],
    path: Optional[Path],
    config_path: Optional[Path],
    meta_type: MetaType,
    file_encoding: str,
    overwrite: bool,
    output_path: Optional[Path],
) -> Config:
    source: Union[Path, str]
    if url and not path:
        source = url
    elif path and not url:
        source = path
    elif url and path:
        typer.secho("Provide either --url or --path, not both", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    else:
        typer.secho("You must either provide --url or --path", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    try:
        codecs.getencoder(file_encoding)
    except LookupError as err:
        typer.secho(f"Unknown encoding : {file_encoding}", fg=typer.colors.RED)
        raise typer.Exit(code=1) from err

    if not config_path:
        config_file = ConfigFile()
    else:
        try:
            config_file = ConfigFile.load_from_path(path=config_path)
        except Exception as err:
            raise typer.BadParameter("Unable to parse config") from err

    return Config.from_sources(config_file, meta_type, source, file_encoding, overwrite, output_path=output_path)


# noinspection PyUnusedLocal


@app.callback(name="openapi-python-client")
def cli(
    version: bool = typer.Option(False, "--version", callback=_version_callback, help="Print the version and exit"),
) -> None:
    """Generate a Python client from an OpenAPI document"""


def _print_parser_error(err: GeneratorError, color: str) -> None:
    typer.secho(err.header, bold=True, fg=color, err=True)
    typer.echo()
    if err.detail:
        typer.secho(err.detail, fg=color, err=True)
        typer.echo()

    if isinstance(err, ParseError) and err.data is not None:
        formatted_data = pformat(err.data)
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
        "https://github.com/openapi-generators/openapi-python-client/issues/new/choose", fg=typer.colors.BRIGHT_BLUE
    )
    typer.secho(
        f"If you believe this was a mistake or this tool is missing a feature you need, "
        f"please open an issue at {gh_link}",
        fg=typer.colors.BLUE,
        err=True,
    )

    if error_level == ErrorLevel.ERROR or fail_on_warning:
        raise typer.Exit(code=1)


@app.command()
def generate(
    url: Optional[str] = typer.Option(None, help="A URL to read the OpenAPI document from"),
    path: Optional[Path] = typer.Option(None, help="A path to the OpenAPI document"),
    custom_template_path: Optional[Path] = typer.Option(
        None,
        help="A path to a directory containing custom template(s)",
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    ),  # type: ignore
    meta: MetaType = typer.Option(
        MetaType.POETRY,
        help="The type of metadata you want to generate.",
    ),
    file_encoding: str = typer.Option("utf-8", help="Encoding used when writing generated"),
    config_path: Optional[Path] = typer.Option(None, "--config", help="Path to the config file to use"),
    fail_on_warning: bool = False,
    overwrite: bool = typer.Option(False, help="Overwrite the existing client if it exists"),
    output_path: Optional[Path] = typer.Option(
        None,
        help="Path to write the generated code to. "
        "Defaults to the OpenAPI document title converted to kebab or snake case (depending on meta type). "
        "Can also be overridden with `project_name_override` or `package_name_override` in config.",
    ),
) -> None:
    """Generate a new OpenAPI Client library"""
    from . import generate

    config = _process_config(
        url=url,
        path=path,
        config_path=config_path,
        meta_type=meta,
        file_encoding=file_encoding,
        overwrite=overwrite,
        output_path=output_path,
    )
    errors = generate(
        custom_template_path=custom_template_path,
        config=config,
    )
    handle_errors(errors, fail_on_warning)
