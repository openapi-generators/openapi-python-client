""" Generate modern Python clients from OpenAPI """
from __future__ import annotations

import json
import shutil
import subprocess
from importlib.metadata import version
from pathlib import Path
from typing import Any, Dict, Optional

import httpx
import yaml
from jinja2 import Environment, PackageLoader

from .openapi_parser import OpenAPI, import_string_from_reference

__version__ = version(__package__)


def _get_project_for_url_or_path(url: Optional[str], path: Optional[Path]) -> _Project:
    data_dict = _get_json(url=url, path=path)
    openapi = OpenAPI.from_dict(data_dict)
    return _Project(openapi=openapi)


def load_config(*, path: Path) -> None:
    """ Loads config from provided Path """
    config_data = yaml.safe_load(path.read_text())

    if "class_overrides" in config_data:
        from .openapi_parser import reference

        for class_name, class_data in config_data["class_overrides"].items():
            reference.class_overrides[class_name] = reference.Reference(**class_data)


def create_new_client(*, url: Optional[str], path: Optional[Path]) -> None:
    """ Generate the client library """
    project = _get_project_for_url_or_path(url=url, path=path)
    project.build()


def update_existing_client(*, url: Optional[str], path: Optional[Path]) -> None:
    """ Update an existing client library """
    project = _get_project_for_url_or_path(url=url, path=path)
    project.update()


def _get_json(*, url: Optional[str], path: Optional[Path]) -> Dict[str, Any]:
    json_bytes: bytes
    if url is not None and path is not None:
        raise ValueError("Provide URL or Path, not both.")
    elif url is not None:
        response = httpx.get(url)
        json_bytes = response.content
    elif path is not None:
        json_bytes = path.read_bytes()
    else:
        raise ValueError("No URL or Path provided")
    return json.loads(json_bytes)


class _Project:
    def __init__(self, *, openapi: OpenAPI) -> None:
        self.openapi: OpenAPI = openapi
        self.env: Environment = Environment(loader=PackageLoader(__package__), trim_blocks=True, lstrip_blocks=True)

        self.project_name: str = f"{openapi.title.replace(' ', '-').lower()}-client"
        self.project_dir: Path = Path.cwd() / self.project_name

        self.package_name: str = self.project_name.replace("-", "_")
        self.package_dir: Path = self.project_dir / self.package_name
        self.package_description = f"A client library for accessing {self.openapi.title}"

    def build(self) -> None:
        """ Create the project from templates """

        print(f"Generating {self.project_name}")
        self.project_dir.mkdir()
        self._create_package()
        self._build_metadata()
        self._build_models()
        self._build_api()
        self._reformat()

    def update(self) -> None:
        """ Update an existing project """

        if not self.package_dir.is_dir():
            raise FileNotFoundError()
        print(f"Updating {self.project_name}")
        shutil.rmtree(self.package_dir)
        self._create_package()
        self._build_models()
        self._build_api()
        self._reformat()

    def _reformat(self) -> None:
        subprocess.run("isort --recursive --apply", cwd=self.project_dir, shell=True)
        subprocess.run("black .", cwd=self.project_dir, shell=True)

    def _create_package(self) -> None:
        self.package_dir.mkdir()
        # Package __init__.py
        package_init = self.package_dir / "__init__.py"

        package_init_template = self.env.get_template("package_init.pyi")
        package_init.write_text(package_init_template.render(description=self.package_description))

        pytyped = self.package_dir / "py.typed"
        pytyped.write_text("# Marker file for PEP 561")

    def _build_metadata(self) -> None:
        # Create a pyproject.toml file
        pyproject_template = self.env.get_template("pyproject.toml")
        pyproject_path = self.project_dir / "pyproject.toml"
        pyproject_path.write_text(
            pyproject_template.render(
                project_name=self.project_name, package_name=self.package_name, description=self.package_description
            )
        )

        # README.md
        readme = self.project_dir / "README.md"
        readme_template = self.env.get_template("README.md")
        readme.write_text(
            readme_template.render(
                project_name=self.project_name, description=self.package_description, package_name=self.package_name
            )
        )

        # .gitignore
        git_ignore_path = self.project_dir / ".gitignore"
        git_ignore_template = self.env.get_template(".gitignore")
        git_ignore_path.write_text(git_ignore_template.render())

    def _build_models(self) -> None:
        # Generate models
        models_dir = self.package_dir / "models"
        models_dir.mkdir()
        models_init = models_dir / "__init__.py"
        imports = []

        model_template = self.env.get_template("model.pyi")
        for schema in self.openapi.schemas.values():
            module_path = models_dir / f"{schema.reference.module_name}.py"
            module_path.write_text(model_template.render(schema=schema))
            imports.append(import_string_from_reference(schema.reference))

        # Generate enums
        enum_template = self.env.get_template("enum.pyi")
        for enum in self.openapi.enums.values():
            module_path = models_dir / f"{enum.name}.py"
            module_path.write_text(enum_template.render(enum=enum))
            imports.append(import_string_from_reference(enum.reference))

        models_init_template = self.env.get_template("models_init.pyi")
        models_init.write_text(models_init_template.render(imports=imports))

    def _build_api(self) -> None:
        # Generate Client
        client_path = self.package_dir / "client.py"
        client_template = self.env.get_template("client.pyi")
        client_path.write_text(client_template.render())

        # Generate endpoints
        api_dir = self.package_dir / "api"
        api_dir.mkdir()
        api_init = api_dir / "__init__.py"
        api_init.write_text('""" Contains synchronous methods for accessing the API """')

        async_api_dir = self.package_dir / "async_api"
        async_api_dir.mkdir()
        async_api_init = async_api_dir / "__init__.py"
        async_api_init.write_text('""" Contains async methods for accessing the API """')

        api_errors = self.package_dir / "errors.py"
        errors_template = self.env.get_template("errors.pyi")
        api_errors.write_text(errors_template.render())

        endpoint_template = self.env.get_template("endpoint_module.pyi")
        async_endpoint_template = self.env.get_template("async_endpoint_module.pyi")
        for tag, collection in self.openapi.endpoint_collections_by_tag.items():
            module_path = api_dir / f"{tag}.py"
            module_path.write_text(endpoint_template.render(collection=collection))
            async_module_path = async_api_dir / f"{tag}.py"
            async_module_path.write_text(async_endpoint_template.render(collection=collection))
