""" Generate modern Python clients from OpenAPI """

import shutil
import subprocess
import sys
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Union

import httpcore
import httpx
import yaml
from jinja2 import BaseLoader, ChoiceLoader, Environment, FileSystemLoader, PackageLoader

from openapi_python_client import utils

from .config import Config
from .parser import GeneratorData, import_string_from_class
from .parser.errors import GeneratorError
from .utils import snake_case

if sys.version_info.minor < 8:  # version did not exist before 3.8, need to use a backport
    from importlib_metadata import version
else:
    from importlib.metadata import version  # type: ignore

__version__ = version(__package__)


class MetaType(str, Enum):
    NONE = "none"
    POETRY = "poetry"
    SETUP = "setup"


TEMPLATE_FILTERS = {
    "snakecase": utils.snake_case,
    "kebabcase": utils.kebab_case,
    "pascalcase": utils.pascal_case,
    "any": any,
}


class Project:
    def __init__(
        self,
        *,
        openapi: GeneratorData,
        meta: MetaType,
        config: Config,
        custom_template_path: Optional[Path] = None,
        file_encoding: str = "utf-8",
    ) -> None:
        self.openapi: GeneratorData = openapi
        self.meta: MetaType = meta
        self.file_encoding = file_encoding

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
        self.env: Environment = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

        self.project_name: str = config.project_name_override or f"{utils.kebab_case(openapi.title).lower()}-client"
        self.project_dir: Path = Path.cwd()
        if meta != MetaType.NONE:
            self.project_dir /= self.project_name

        self.package_name: str = config.package_name_override or self.project_name.replace("-", "_")
        self.package_dir: Path = self.project_dir / self.package_name
        self.package_description: str = utils.remove_string_escapes(
            f"A client library for accessing {self.openapi.title}"
        )
        self.version: str = config.package_version_override or openapi.version

        self.env.filters.update(TEMPLATE_FILTERS)

    def build(self) -> Sequence[GeneratorError]:
        """Create the project from templates"""

        if self.meta == MetaType.NONE:
            print(f"Generating {self.package_name}")
        else:
            print(f"Generating {self.project_name}")
            try:
                self.project_dir.mkdir()
            except FileExistsError:
                return [GeneratorError(detail="Directory already exists. Delete it or use the update command.")]
        self._create_package()
        self._build_metadata()
        self._build_models()
        self._build_api()
        self._reformat()
        return self._get_errors()

    def update(self) -> Sequence[GeneratorError]:
        """Update an existing project"""

        if not self.package_dir.is_dir():
            raise FileNotFoundError()
        print(f"Updating {self.package_name}")
        shutil.rmtree(self.package_dir)
        self._create_package()
        self._build_models()
        self._build_api()
        self._reformat()
        return self._get_errors()

    def _reformat(self) -> None:
        subprocess.run(
            "autoflake -i -r --remove-all-unused-imports --remove-unused-variables --ignore-init-module-imports .",
            cwd=self.package_dir,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        subprocess.run(
            "isort .",
            cwd=self.project_dir,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        subprocess.run("black .", cwd=self.project_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def _get_errors(self) -> Sequence[GeneratorError]:
        errors = []
        for collection in self.openapi.endpoint_collections_by_tag.values():
            errors.extend(collection.parse_errors)
        errors.extend(self.openapi.errors)
        return errors

    def _create_package(self) -> None:
        self.package_dir.mkdir()
        # Package __init__.py
        package_init = self.package_dir / "__init__.py"

        package_init_template = self.env.get_template("package_init.py.jinja")
        package_init.write_text(
            package_init_template.render(description=self.package_description), encoding=self.file_encoding
        )

        if self.meta != MetaType.NONE:
            pytyped = self.package_dir / "py.typed"
            pytyped.write_text("# Marker file for PEP 561", encoding=self.file_encoding)

        types_template = self.env.get_template("types.py.jinja")
        types_path = self.package_dir / "types.py"
        types_path.write_text(types_template.render(), encoding=self.file_encoding)

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
            readme_template.render(
                project_name=self.project_name, description=self.package_description, package_name=self.package_name
            ),
            encoding=self.file_encoding,
        )

        # .gitignore
        git_ignore_path = self.project_dir / ".gitignore"
        git_ignore_template = self.env.get_template(".gitignore.jinja")
        git_ignore_path.write_text(git_ignore_template.render(), encoding=self.file_encoding)

    def _build_pyproject_toml(self, *, use_poetry: bool) -> None:
        template = "pyproject.toml.jinja" if use_poetry else "pyproject_no_poetry.toml.jinja"
        pyproject_template = self.env.get_template(template)
        pyproject_path = self.project_dir / "pyproject.toml"
        pyproject_path.write_text(
            pyproject_template.render(
                project_name=self.project_name,
                package_name=self.package_name,
                version=self.version,
                description=self.package_description,
            ),
            encoding=self.file_encoding,
        )

    def _build_setup_py(self) -> None:
        template = self.env.get_template("setup.py.jinja")
        path = self.project_dir / "setup.py"
        path.write_text(
            template.render(
                project_name=self.project_name,
                package_name=self.package_name,
                version=self.version,
                description=self.package_description,
            ),
            encoding=self.file_encoding,
        )

    def _build_models(self) -> None:
        # Generate models
        models_dir = self.package_dir / "models"
        models_dir.mkdir()
        models_init = models_dir / "__init__.py"
        imports = []

        model_template = self.env.get_template("model.py.jinja")
        for model in self.openapi.models:
            module_path = models_dir / f"{model.class_info.module_name}.py"
            module_path.write_text(model_template.render(model=model), encoding=self.file_encoding)
            imports.append(import_string_from_class(model.class_info))

        # Generate enums
        str_enum_template = self.env.get_template("str_enum.py.jinja")
        int_enum_template = self.env.get_template("int_enum.py.jinja")
        for enum in self.openapi.enums:
            module_path = models_dir / f"{enum.class_info.module_name}.py"
            if enum.value_type is int:
                module_path.write_text(int_enum_template.render(enum=enum), encoding=self.file_encoding)
            else:
                module_path.write_text(str_enum_template.render(enum=enum), encoding=self.file_encoding)
            imports.append(import_string_from_class(enum.class_info))

        models_init_template = self.env.get_template("models_init.py.jinja")
        models_init.write_text(models_init_template.render(imports=imports), encoding=self.file_encoding)

    def _build_api(self) -> None:
        # Generate Client
        client_path = self.package_dir / "client.py"
        client_template = self.env.get_template("client.py.jinja")
        client_path.write_text(client_template.render(), encoding=self.file_encoding)

        # Generate endpoints
        api_dir = self.package_dir / "api"
        api_dir.mkdir()
        api_init = api_dir / "__init__.py"
        api_init.write_text('""" Contains methods for accessing the API """', encoding=self.file_encoding)

        endpoint_template = self.env.get_template("endpoint_module.py.jinja")
        for tag, collection in self.openapi.endpoint_collections_by_tag.items():
            tag_dir = api_dir / tag
            tag_dir.mkdir()
            (tag_dir / "__init__.py").touch()

            for endpoint in collection.endpoints:
                module_path = tag_dir / f"{snake_case(endpoint.name)}.py"
                module_path.write_text(endpoint_template.render(endpoint=endpoint), encoding=self.file_encoding)


def _get_project_for_url_or_path(
    url: Optional[str],
    path: Optional[Path],
    meta: MetaType,
    config: Config,
    custom_template_path: Optional[Path] = None,
    file_encoding: str = "utf-8",
) -> Union[Project, GeneratorError]:
    data_dict = _get_document(url=url, path=path)
    if isinstance(data_dict, GeneratorError):
        return data_dict
    openapi = GeneratorData.from_dict(data_dict, config=config)
    if isinstance(openapi, GeneratorError):
        return openapi
    return Project(
        openapi=openapi,
        custom_template_path=custom_template_path,
        meta=meta,
        file_encoding=file_encoding,
        config=config,
    )


def create_new_client(
    *,
    url: Optional[str],
    path: Optional[Path],
    meta: MetaType,
    config: Config,
    custom_template_path: Optional[Path] = None,
    file_encoding: str = "utf-8",
) -> Sequence[GeneratorError]:
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
    )
    if isinstance(project, GeneratorError):
        return [project]
    return project.build()


def update_existing_client(
    *,
    url: Optional[str],
    path: Optional[Path],
    meta: MetaType,
    config: Config,
    custom_template_path: Optional[Path] = None,
    file_encoding: str = "utf-8",
) -> Sequence[GeneratorError]:
    """
    Update an existing client library

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
    )
    if isinstance(project, GeneratorError):
        return [project]
    return project.update()


def _get_document(*, url: Optional[str], path: Optional[Path]) -> Union[Dict[str, Any], GeneratorError]:
    yaml_bytes: bytes
    if url is not None and path is not None:
        return GeneratorError(header="Provide URL or Path, not both.")
    if url is not None:
        try:
            response = httpx.get(url)
            yaml_bytes = response.content
        except (httpx.HTTPError, httpcore.NetworkError):
            return GeneratorError(header="Could not get OpenAPI document from provided URL")
    elif path is not None:
        yaml_bytes = path.read_bytes()
    else:
        return GeneratorError(header="No URL or Path provided")
    try:
        return yaml.safe_load(yaml_bytes)
    except yaml.YAMLError:
        return GeneratorError(header="Invalid YAML from provided source")
