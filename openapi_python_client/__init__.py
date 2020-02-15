""" Generate modern Python clients from OpenAPI """
import sys
from pathlib import Path
from typing import Dict

import orjson
import requests
import stringcase
from jinja2 import Environment, PackageLoader

from .models import OpenAPI


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

    # Create a pyproject.toml file
    pyproject_template = env.get_template("pyproject.toml")
    pyproject_path = project_dir / "pyproject.toml"
    pyproject_path.write_text(pyproject_template.render(project_name=project_name, package_name=package_name))

    # Generate models
    models_dir = package_dir / "models"
    models_dir.mkdir()
    model_template = env.get_template("model.pyi")
    for schema in openapi.schemas.values():
        module_path = models_dir / f"{stringcase.snakecase(schema.title)}.py"
        module_path.write_text(model_template.render(schema=schema))

    # Generate enums
    enum_template = env.get_template("enum.pyi")
    for enum in openapi.enums.values():
        module_path = models_dir / f"{enum.name}.py"
        module_path.write_text(enum_template.render(enum=enum))

