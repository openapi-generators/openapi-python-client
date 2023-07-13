""" Generate modern Python clients from OpenAPI """

import logging
import shutil
import subprocess
from enum import Enum
from importlib.metadata import version
from pathlib import Path
from subprocess import CalledProcessError
from typing import Optional

from jinja2 import BaseLoader, ChoiceLoader, Environment, FileSystemLoader, PackageLoader

from openapi_python_client import utils
from .config import Config
from .parser.openapi_parser import OpenapiParser
from .typing import TEndpointFilter


log = logging.getLogger(__name__)

__version__ = version(__package__)


class MetaType(str, Enum):
    """The types of metadata supported for project generation."""

    NONE = "none"
    POETRY = "poetry"
    SETUP = "setup"


TEMPLATE_FILTERS = {
    "snakecase": utils.snake_case,
    "kebabcase": utils.kebab_case,
    "pascalcase": utils.pascal_case,
    "any": any,
}


class Project:  # pylint: disable=too-many-instance-attributes
    """Represents a Python project (the top level file-tree) to generate"""

    openapi: OpenapiParser

    def __init__(
        self,
        *,
        openapi: OpenapiParser,
        meta: MetaType,
        config: Config,
        custom_template_path: Optional[Path] = None,
        file_encoding: str = "utf-8",
        endpoint_filter: Optional[TEndpointFilter] = None,
    ) -> None:
        self.openapi = openapi
        self.meta: MetaType = meta
        self.file_encoding = file_encoding
        self.config = config

        package_loader = PackageLoader(__package__)
        loader: BaseLoader
        if custom_template_path is not None:
            loader = ChoiceLoader(
                [
                    FileSystemLoader(str(custom_template_path)),
                    package_loader,
                ]
            )
        else:
            loader = package_loader
        self.env: Environment = Environment(
            loader=loader,
            trim_blocks=True,
            lstrip_blocks=True,
            extensions=["jinja2.ext.loopcontrols"],
            keep_trailing_newline=True,
        )

        project_name_base: str = config.project_name_override or f"{utils.kebab_case(openapi.info.title).lower()}"
        self.project_name = project_name_base + config.project_name_suffix
        self.package_name: str = config.package_name_override or self.project_name

        self.package_name = self.package_name.replace("-", "_")
        self.source_name: str = self.package_name + "_source"
        self.dataset_name: str = self.package_name + config.dataset_name_suffix
        self.project_dir: Path = Path.cwd()
        # if meta != MetaType.NONE:
        self.project_dir /= self.project_name

        self.package_dir: Path = self.project_dir / self.package_name
        self.package_description: str = utils.remove_string_escapes(
            f"A pipeline to load data from {self.openapi.info.title}"
        )
        self.version: str = config.package_version_override or openapi.info.version

        self.env.filters.update(TEMPLATE_FILTERS)
        self.env.globals.update(
            utils=utils,
            python_identifier=lambda x: utils.PythonIdentifier(x, config.field_prefix),
            class_name=lambda x: utils.ClassName(x, config.field_prefix),
            package_name=self.package_name,
            package_dir=self.package_dir,
            package_description=self.package_description,
            package_version=self.version,
            project_name=self.project_name,
            project_dir=self.project_dir,
            openapi=self.openapi,
            endpoints=self.openapi.endpoints,
        )
        # self.errors: List[GeneratorError] = []
        self.endpoint_filter = endpoint_filter

    def build(self) -> None:
        """Create the project from templates"""
        if self.endpoint_filter:
            endpoint_names = self.endpoint_filter(self.openapi.endpoints)
            self.openapi.endpoints.set_names_to_render(endpoint_names)
        if self.meta == MetaType.NONE:
            print(f"Generating {self.package_name}")
        else:
            print(f"Generating {self.project_name}")
            self.project_dir.mkdir()
        self._create_package()
        self._build_metadata()
        self._build_dlt_config()
        self._build_security()
        self._build_source()
        self._build_pipeline()
        self._run_post_hooks()

    def _run_post_hooks(self) -> None:
        for command in self.config.post_hooks:
            self._run_command(command)

    def _run_command(self, cmd: str) -> None:
        cmd_name = cmd.split(" ")[0]
        command_exists = shutil.which(cmd_name)
        if not command_exists:
            log.warning("Skipping integration: %s is not in PATH", cmd_name)
            return
        cwd = self.package_dir if self.meta == MetaType.NONE else self.project_dir
        try:
            subprocess.run(cmd, cwd=cwd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except CalledProcessError as err:
            raise RuntimeError("{}failed\n{}".format(cmd_name, err.stderr.decode() or err.output.decode())) from err

    def _create_package(self) -> None:
        self.project_dir.mkdir(exist_ok=True)
        self.package_dir.mkdir()

        if self.meta != MetaType.NONE:
            pytyped = self.package_dir / "py.typed"
            pytyped.write_text("# Marker file for PEP 561", encoding=self.file_encoding)

        types_template = self.env.get_template("types.py.jinja")
        types_path = self.package_dir / "types.py"
        types_path.write_text(types_template.render(), encoding=self.file_encoding)

        utils_template = self.env.get_template("utils.py.jinja")
        utils_path = self.package_dir / "utils.py"
        utils_path.write_text(utils_template.render(), encoding=self.file_encoding)

        api_helpers_template = self.env.get_template("api_helpers.py.jinja")
        api_helpers_path = self.package_dir / "api_helpers.py"
        api_helpers_path.write_text(api_helpers_template.render(), encoding=self.file_encoding)

    def _build_dlt_config(self) -> None:
        config_dir = self.project_dir / ".dlt"
        config_dir.mkdir()

        servers = self.openapi.info.servers
        first_server = servers[0] if servers else None
        other_servers = servers[1:]
        if first_server and first_server.url == "/" and not first_server.description:
            # Remove default server
            first_server = None

        config_template = self.env.get_template("dlt_config.toml.jinja")
        config_path = config_dir / "config.toml"
        config_path.write_text(
            config_template.render(
                first_server=first_server, other_servers=other_servers, source_name=self.source_name
            ),
            encoding=self.file_encoding,
        )

    def _build_metadata(self) -> None:
        if self.meta == MetaType.NONE:
            return

        self._build_pyproject_toml(use_poetry=self.meta == MetaType.POETRY)
        if self.meta == MetaType.SETUP:
            self._build_setup_py()

        # README.md
        readme = self.project_dir / "README.md"
        readme_template = self.env.get_template("README.md.jinja")
        readme.write_text(
            readme_template.render(),
            encoding=self.file_encoding,
        )

        # .gitignore
        git_ignore_path = self.project_dir / ".gitignore"
        git_ignore_template = self.env.get_template(".gitignore.jinja")
        git_ignore_path.write_text(git_ignore_template.render(), encoding=self.file_encoding)

        # requirements.txt
        requirements_path = self.project_dir / "requirements.txt"
        requirements_template = self.env.get_template("requirements.txt.jinja")
        requirements_path.write_text(requirements_template.render(), encoding=self.file_encoding)

    def _build_pyproject_toml(self, *, use_poetry: bool) -> None:
        template = "pyproject.toml.jinja"
        pyproject_template = self.env.get_template(template)
        pyproject_path = self.project_dir / "pyproject.toml"
        pyproject_path.write_text(
            pyproject_template.render(use_poetry=use_poetry),
            encoding=self.file_encoding,
        )

    def _build_setup_py(self) -> None:
        template = self.env.get_template("setup.py.jinja")
        path = self.project_dir / "setup.py"
        path.write_text(
            template.render(),
            encoding=self.file_encoding,
        )

    def _build_security(self) -> None:
        schemes_base = self.package_dir / "_base.py"

        scheme_template = self.env.get_template("security_schemes.py.jinja")
        module_path = self.package_dir / "credentials.py"
        module_path.write_text(
            scheme_template.render(security_schemes=self.openapi.context.security_schemes.values()),
            encoding=self.file_encoding,
        )

        schemes_base_template = self.env.get_template("security_schemes_base.py.jinja")
        schemes_base.write_text(schemes_base_template.render(), encoding=self.file_encoding)

    def _build_source(self) -> None:
        module_path = self.package_dir / "__init__.py"

        template = self.env.get_template("source.py.jinja")
        module_path.write_text(
            template.render(
                source_name=self.source_name,
                endpoint_collection=self.openapi.endpoints,
                imports=self.openapi.credentials.get_imports() if self.openapi.credentials else [],
                credentials=self.openapi.credentials,
            ),
            encoding=self.file_encoding,
        )

    def _build_pipeline(self) -> None:
        module_path = self.project_dir / "pipeline.py"

        template = self.env.get_template("pipeline.py.jinja")
        module_path.write_text(
            template.render(
                package_name=self.package_name, source_name=self.source_name, dataset_name=self.dataset_name
            ),
            encoding=self.file_encoding,
        )


def _get_project_for_url_or_path(  # pylint: disable=too-many-arguments
    url: Optional[str],
    path: Optional[Path],
    meta: MetaType,
    config: Config,
    custom_template_path: Optional[Path] = None,
    file_encoding: str = "utf-8",
    endpoint_filter: Optional[TEndpointFilter] = None,
) -> Project:
    openapi = OpenapiParser(url or path, config=config)
    openapi.parse()
    return Project(
        openapi=openapi,
        custom_template_path=custom_template_path,
        meta=meta,
        file_encoding=file_encoding,
        config=config,
        endpoint_filter=endpoint_filter,
    )


def create_new_client(
    *,
    url: Optional[str] = None,
    path: Optional[Path] = None,
    meta: MetaType = MetaType.POETRY,
    config: Config = Config(),
    custom_template_path: Optional[Path] = None,
    file_encoding: str = "utf-8",
    endpoint_filter: Optional[TEndpointFilter] = None,
) -> Project:
    """
    Generate the client library

    Returns:
         A list containing any errors encountered when generating.
    """
    project = _get_project_for_url_or_path(
        url=url,
        path=path,
        custom_template_path=custom_template_path,
        meta=meta,
        file_encoding=file_encoding,
        config=config,
        endpoint_filter=endpoint_filter,
    )
    project.build()
    return project
