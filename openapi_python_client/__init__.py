""" Generate modern Python clients from OpenAPI """

import logging
import json
import mimetypes
import shutil
import subprocess
from enum import Enum
from importlib.metadata import version
from pathlib import Path
from subprocess import CalledProcessError
from typing import Any, Dict, List, Optional, Sequence, Union

import httpcore
import httpx
import yaml
from jinja2 import BaseLoader, ChoiceLoader, Environment, FileSystemLoader, PackageLoader

from openapi_python_client import utils

from .config import Config

# from .parser import GeneratorData, import_string_from_class
# from .parser.errors import ErrorLevel, GeneratorError
from parser.openapi_parser import OpenapiParser

# from .typing import TEndpointFilter

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
        # endpoint_filter: Optional[TEndpointFilter] = None,
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
        # self.endpoint_filter = endpoint_filter

    def build(self) -> None:
        """Create the project from templates"""
        # if self.endpoint_filter:
        #     endpoint_names = self.endpoint_filter(self.openapi.endpoints)
        #     self.openapi.endpoints.set_names_to_render(endpoint_names)
        if self.meta == MetaType.NONE:
            print(f"Generating {self.package_name}")
        else:
            print(f"Generating {self.project_name}")
            self.project_dir.mkdir()
        self._create_package()
        self._build_metadata()
        # TODO: Config with servers
        # self._build_dlt_config()
        # self._build_models()
        # TODO: Security in parser
        # self._build_security()
        self._build_api()
        # self._build_source()
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
        api_helpers_path = self.package_dir / "utils.py"
        api_helpers_path.write_text(api_helpers_template.render(), encoding=self.file_encoding)

    def _build_dlt_config(self) -> None:
        config_dir = self.project_dir / ".dlt"
        config_dir.mkdir()

        first_server = self.openapi.openapi.servers[0]
        other_servers = self.openapi.openapi.servers[1:]

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

    def _build_api(self) -> None:
        # Generate Client
        # client_path = self.package_dir / "client.py"
        # client_template = self.env.get_template("client.py.jinja")
        # client_path.write_text(client_template.render(), encoding=self.file_encoding)

        # Generate included Errors
        errors_path = self.package_dir / "errors.py"
        errors_template = self.env.get_template("errors.py.jinja")
        errors_path.write_text(errors_template.render(), encoding=self.file_encoding)

        # Generate endpoints
        api_dir = self.package_dir / "api"
        api_dir.mkdir()

        endpoint_template = self.env.get_template(
            "endpoint_module.py.jinja", globals={"isbool": lambda obj: obj.get_base_type_string() == "bool"}
        )
        for endpoint in self.openapi.endpoints.all_endpoints_to_render:
            module_path = api_dir / f"{endpoint.python_name}.py"
            module_path.write_text(
                endpoint_template.render(endpoint=endpoint),
                encoding=self.file_encoding,
            )

        # Generate API init
        api_init_path = api_dir / "__init__.py"
        api_init_template = self.env.get_template("api_init.py.jinja")
        api_init_path.write_text(
            api_init_template.render(endpoints=self.openapi.endpoints.all_endpoints_to_render),
            encoding=self.file_encoding,
        )

    def _build_security(self) -> None:
        schemes_dir = self.package_dir / "security"
        schemes_dir.mkdir()
        schemes_init = schemes_dir / "__init__.py"
        schemes_base = schemes_dir / "_base.py"
        imports = []
        alls = []

        scheme_template = self.env.get_template("security_scheme.py.jinja")
        for scheme in self.openapi.security_schemes.values():
            module_path = schemes_dir / f"{scheme.class_info.module_name}.py"
            module_path.write_text(scheme_template.render(scheme=scheme), encoding=self.file_encoding)
            imports.append(import_string_from_class(scheme.class_info))
            alls.append(scheme.class_info.name)

        schemes_init_template = self.env.get_template("security_schemes_init.py.jinja")
        schemes_init.write_text(schemes_init_template.render(imports=imports, alls=alls), encoding=self.file_encoding)

        schemes_base_template = self.env.get_template("security_schemes_base.py.jinja")
        schemes_base.write_text(schemes_base_template.render(), encoding=self.file_encoding)

    def _build_source(self) -> None:
        module_path = self.package_dir / "__init__.py"

        template = self.env.get_template("source.py.jinja")
        # TODO: Credentials in new parser
        # imports = self.openapi.credentials.get_imports(prefix=".") | self.openapi.credentials.get_lazy_imports(
        #     prefix="."
        # )
        module_path.write_text(
            template.render(
                source_name=self.source_name,
                endpoint_collections=self.openapi.endpoints.all_endpoints_to_render,
                imports=[],  # TODO: Credentials imports
                # credentials=self.openapi.credentials if self.openapi.credentials.is_populated else None,
                credentials=None,
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
    # endpoint_filter: Optional[TEndpointFilter] = None,
) -> Project:
    # data_dict = _get_document(url=url, path=path, timeout=config.http_timeout)
    # if isinstance(data_dict, GeneratorError):
    #     return data_dict
    openapi = OpenapiParser(url or path, config=config)
    openapi.parse()
    # openapi = GeneratorData.from_dict(data_dict, config=config)
    # if isinstance(openapi, GeneratorError):
    #     return openapi
    return Project(
        openapi=openapi,
        custom_template_path=custom_template_path,
        meta=meta,
        file_encoding=file_encoding,
        config=config,
        # endpoint_filter=endpoint_filter,
    )


def create_new_client(
    *,
    url: Optional[str] = None,
    path: Optional[Path] = None,
    meta: MetaType = MetaType.POETRY,
    config: Config = Config(),
    custom_template_path: Optional[Path] = None,
    file_encoding: str = "utf-8",
    # endpoint_filter: Optional[TEndpointFilter] = None,
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
        # endpoint_filter=endpoint_filter,
    )
    project.build()
    return project


# def update_existing_client(
#     *,
#     url: Optional[str],
#     path: Optional[Path],
#     meta: MetaType,
#     config: Config,
#     custom_template_path: Optional[Path] = None,
#     file_encoding: str = "utf-8",
# ) -> None:
#     """
#     Update an existing client library

#     Returns:
#          A list containing any errors encountered when generating.
#     """
#     project = _get_project_for_url_or_path(
#         url=url,
#         path=path,
#         custom_template_path=custom_template_path,
#         meta=meta,
#         file_encoding=file_encoding,
#         config=config,
#     )
#     if isinstance(project, GeneratorError):
#         return [project]
#     return project.update()


# def _load_yaml_or_json(data: bytes, content_type: Optional[str]) -> Union[Dict[str, Any], GeneratorError]:
#     if content_type == "application/json":
#         try:
#             return json.loads(data.decode())
#         except ValueError as err:
#             return GeneratorError(header=f"Invalid JSON from provided source: {err}")
#     else:
#         try:
#             return yaml.safe_load(data)
#         except yaml.YAMLError as err:
#             return GeneratorError(header=f"Invalid YAML from provided source: {err}")


# def _get_document(*, url: Optional[str], path: Optional[Path], timeout: int) -> Union[Dict[str, Any], GeneratorError]:
#     yaml_bytes: bytes
#     content_type: Optional[str]
#     if url is not None and path is not None:
#         return GeneratorError(header="Provide URL or Path, not both.")
#     if url is not None:
#         try:
#             response = httpx.get(url, timeout=timeout)
#             yaml_bytes = response.content
#             if "content-type" in response.headers:
#                 content_type = response.headers["content-type"].split(";")[0]
#             else:
#                 content_type = mimetypes.guess_type(url, strict=True)[0]

#         except (httpx.HTTPError, httpcore.NetworkError):
#             return GeneratorError(header="Could not get OpenAPI document from provided URL")
#     elif path is not None:
#         yaml_bytes = path.read_bytes()
#         content_type = mimetypes.guess_type(path.absolute().as_uri(), strict=True)[0]

#     else:
#         return GeneratorError(header="No URL or Path provided")

#     return _load_yaml_or_json(yaml_bytes, content_type)
