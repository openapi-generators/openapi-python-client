""" Generate modern Python clients from OpenAPI """
import sys
from pathlib import Path
from typing import Dict

import orjson
import requests
from jinja2 import Environment, PackageLoader

from .models import OpenAPI, import_string_from_reference


def main():
    """ Generate the client library """
    url = sys.argv[1]
    json = _get_json(url)
    data_dict = _parse_json(json)
    openapi = OpenAPI.from_dict(data_dict)
    _build_project(openapi)


def _get_json(url) -> bytes:
    response = requests.get(url)
    return response.content


def _parse_json(json: bytes) -> Dict:
    return orjson.loads(json)


def _build_project(openapi: OpenAPI):
    env = Environment(loader=PackageLoader(__package__), trim_blocks=True, lstrip_blocks=True)

    # Create output directories
    project_name = f"{openapi.title.replace(' ', '-').lower()}-client"
    package_name = f"{openapi.title.replace(' ', '_').lower()}_client"
    project_dir = Path.cwd() / project_name
    project_dir.mkdir()
    package_dir = project_dir / package_name
    package_dir.mkdir()
    package_init = package_dir / "__init__.py"
    package_description = f"A client library for accessing {openapi.title}"
    package_init_template = env.get_template("package_init.pyi")
    package_init.write_text(package_init_template.render(description=package_description))

    # Create a pyproject.toml file
    pyproject_template = env.get_template("pyproject.toml")
    pyproject_path = project_dir / "pyproject.toml"
    pyproject_path.write_text(pyproject_template.render(project_name=project_name, package_name=package_name, description=package_description))

    readme = project_dir / "README.md"
    readme_template = env.get_template("README.md")
    readme.write_text(readme_template.render(description=package_description))

    # Generate models
    models_dir = package_dir / "models"
    models_dir.mkdir()
    models_init = models_dir / "__init__.py"
    imports = []

    model_template = env.get_template("model.pyi")
    for schema in openapi.schemas.values():
        module_path = models_dir / f"{schema.reference.module_name}.py"
        module_path.write_text(model_template.render(schema=schema))
        imports.append(import_string_from_reference(schema.reference))

    # Generate enums
    enum_template = env.get_template("enum.pyi")
    for enum in openapi.enums.values():
        module_path = models_dir / f"{enum.name}.py"
        module_path.write_text(enum_template.render(enum=enum))
        imports.append(import_string_from_reference(enum.reference))

    models_init_template = env.get_template("models_init.pyi")
    models_init.write_text(models_init_template.render(imports=imports))

    # Generate Client
    client_path = package_dir / "client.py"
    client_template = env.get_template("client.pyi")
    client_path.write_text(client_template.render())

    # Generate endpoints
    api_dir = package_dir / "api"
    api_dir.mkdir()
    api_init = api_dir / "__init__.py"
    api_init.write_text('""" Contains all methods for accessing the API """')
    endpoint_template = env.get_template("endpoint_module.pyi")
    for tag, collection in openapi.endpoint_collections_by_tag.items():
        module_path = api_dir / f"{tag}.py"
        module_path.write_text(endpoint_template.render(collection=collection))


