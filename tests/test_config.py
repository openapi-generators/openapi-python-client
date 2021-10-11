import json
import pathlib

import pytest
import yaml

from openapi_python_client.config import Config


def test_load_from_path(mocker):
    from openapi_python_client import utils

    override1 = {"class_name": "ExampleClass", "module_name": "example_module"}
    override2 = {"class_name": "DifferentClass", "module_name": "different_module"}
    safe_load = mocker.patch(
        "yaml.safe_load",
        return_value={
            "field_prefix": "blah",
            "class_overrides": {"Class1": override1, "Class2": override2},
            "project_name_override": "project-name",
            "package_name_override": "package_name",
            "package_version_override": "package_version",
        },
    )
    fake_path = mocker.MagicMock(autospec=pathlib.Path)

    config = Config.load_from_path(fake_path)
    safe_load.assert_called()
    assert config.field_prefix == "blah"
    assert config.class_overrides["Class1"] == override1
    assert config.class_overrides["Class2"] == override2
    assert config.project_name_override == "project-name"
    assert config.package_name_override == "package_name"
    assert config.package_version_override == "package_version"


DATA = {"class_overrides": {"Class1": {"class_name": "ExampleClass", "module_name": "example_module"}}}


def json_with_tabs(d):
    return json.dumps(d, indent=4).replace("    ", "\t")


@pytest.mark.parametrize(
    "filename,dump",
    [
        ("example.yml", yaml.dump),
        ("example.json", json.dumps),
        ("example.yaml", yaml.dump),
        ("example.json", json_with_tabs),
    ],
)
def test_load_filenames(tmp_path, filename, dump):
    yml_file = tmp_path.joinpath(filename)
    with open(yml_file, "w") as f:
        f.write(dump(DATA))

    config = Config.load_from_path(yml_file)
    assert config.class_overrides == DATA["class_overrides"]
