""" Generate modern Python clients from OpenAPI """
import json
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from jinja2 import Environment, PackageLoader

from .openapi_parser import OpenAPI, import_string_from_reference


def main(*, url: Optional[str], path: Optional[str]) -> None:
    """ Generate the client library """
    data_dict = _get_json(url=url, path=path)
    openapi = OpenAPI.from_dict(data_dict)
    project = _Project(openapi=openapi)
    project.build()


def _get_json(*, url: Optional[str], path: Optional[str]) -> Dict[str, Any]:
    json_bytes: bytes
    if url is not None and path is not None:
        raise ValueError("Provide URL or Path, not both.")
    elif url is not None:
        response = requests.get(url)
        json_bytes = response.content
    elif path is not None:
        json_bytes = Path(path).read_bytes()
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

    def build(self) -> None:
        """ Create the project from templates """
        print(f"Generating {self.project_name}")
        self.project_dir.mkdir()
        self.package_dir.mkdir()
        self._build_metadata()
        self._build_models()
        self._build_api()

    def _build_metadata(self) -> None:
        # Package __init__.py
        package_init = self.package_dir / "__init__.py"
        package_description = f"A client library for accessing {self.openapi.title}"
        package_init_template = self.env.get_template("package_init.pyi")
        package_init.write_text(package_init_template.render(description=package_description))

        # Create a pyproject.toml file
        pyproject_template = self.env.get_template("pyproject.toml")
        pyproject_path = self.project_dir / "pyproject.toml"
        pyproject_path.write_text(
            pyproject_template.render(
                project_name=self.project_name, package_name=self.package_name, description=package_description
            )
        )

        # README.md
        readme = self.project_dir / "README.md"
        readme_template = self.env.get_template("README.md")
        readme.write_text(readme_template.render(description=package_description))

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
        api_init.write_text('""" Contains all methods for accessing the API """')
        endpoint_template = self.env.get_template("endpoint_module.pyi")
        for tag, collection in self.openapi.endpoint_collections_by_tag.items():
            module_path = api_dir / f"{tag}.py"
            module_path.write_text(endpoint_template.render(collection=collection))
