import codecs
from collections.abc import Sequence
from pathlib import Path
from pprint import pformat

import typer

from openapi_python_client import MetaType, __version__
from openapi_python_client.config import Config, ConfigFile
from openapi_python_client.parser.errors import ErrorLevel, GeneratorError, ParseError

app = typer.Typer(name="openapi-python-client")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"openapi-python-client version: {__version__}")
        raise typer.Exit()


def _split_comma_separated(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _load_config_file(
    *,
    config_path: Path | None,
) -> ConfigFile:
    if not config_path:
        config_file = ConfigFile()
    else:
        try:
            config_file = ConfigFile.load_from_path(path=config_path)
        except Exception as err:
            raise typer.BadParameter("Unable to parse config") from err

    return config_file


def _process_config(
    *,
    url: str | None,
    path: Path | None,
    config_path: Path | None,
    meta_type: MetaType,
    file_encoding: str,
    overwrite: bool,
    output_path: Path | None,
    include_tags: str | None = None,
    exclude_tags: str | None = None,
) -> Config:
    source: Path | str
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

    config_file = _load_config_file(config_path=config_path)

    if include_tags is not None:
        config_file.include_tags = _split_comma_separated(include_tags)
    if exclude_tags is not None:
        config_file.exclude_tags = _split_comma_separated(exclude_tags)

    if config_file.include_tags and config_file.exclude_tags:
        typer.secho("Provide either include_tags or exclude_tags, not both", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    return Config.from_sources(config_file, meta_type, source, file_encoding, overwrite, output_path=output_path)


# noinspection PyUnusedLocal


@app.callback()
def cli(
    version: bool = typer.Option(False, "--version", callback=_version_callback, help="Print the version and exit"),
) -> None:
    """Generate a Python client from an OpenAPI document"""


def _print_parser_error(err: GeneratorError, color: str) -> None:
    typer.secho(err.header, bold=True, fg=color, err=True)
    typer.echo(err=True)
    if err.detail:
        typer.secho(err.detail, fg=color, err=True)
        typer.echo(err=True)

    if isinstance(err, ParseError) and err.data is not None:
        formatted_data = pformat(err.data)
        typer.secho(formatted_data, fg=color, err=True)

    typer.echo(err=True)


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
    url: str | None = typer.Option(None, help="A URL to read the OpenAPI document from"),
    path: Path | None = typer.Option(None, help="A path to the OpenAPI document"),
    custom_template_path: Path | None = typer.Option(
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
    config_path: Path | None = typer.Option(None, "--config", help="Path to the config file to use"),
    fail_on_warning: bool = False,
    overwrite: bool = typer.Option(False, help="Overwrite the existing client if it exists"),
    output_path: Path | None = typer.Option(
        None,
        help="Path to write the generated code to. "
        "Defaults to the OpenAPI document title converted to kebab or snake case (depending on meta type). "
        "Can also be overridden with `project_name_override` or `package_name_override` in config.",
    ),
    include_tags: str | None = typer.Option(
        None,
        "--include-tags",
        help="Comma-separated tags to generate. "
        "Keeps matching endpoints, drops the rest, prunes unused schemas. "
        "Case-sensitive. Overrides config. Can't combine with --exclude-tags.",
    ),
    exclude_tags: str | None = typer.Option(
        None,
        "--exclude-tags",
        help="Comma-separated tags to skip. "
        "Drops matching endpoints, keeps the rest, prunes unused schemas. "
        "Case-sensitive. Overrides config. Can't combine with --include-tags.",
    ),
) -> None:
    """Generate a new OpenAPI Client library"""
    from . import generate  # noqa: PLC0415

    config = _process_config(
        url=url,
        path=path,
        config_path=config_path,
        meta_type=meta,
        file_encoding=file_encoding,
        overwrite=overwrite,
        output_path=output_path,
        include_tags=include_tags,
        exclude_tags=exclude_tags,
    )
    errors = generate(
        custom_template_path=custom_template_path,
        config=config,
    )
    handle_errors(errors, fail_on_warning)
