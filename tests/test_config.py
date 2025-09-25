import json
import os
from io import StringIO
from pathlib import Path
from typing import Any

import pytest
from ruamel.yaml import YAML as _YAML

from openapi_python_client.config import ConfigFile


class YAML(_YAML):
    def dump_to_string(self, data: Any, **kwargs: Any) -> str:
        stream = StringIO()
        self.dump(data=data, stream=stream, **kwargs)
        return stream.getvalue()


yaml = YAML(typ=["safe", "string"])


def json_with_tabs(d: dict) -> str:
    return json.dumps(d, indent=4).replace("    ", "\t")


@pytest.mark.parametrize(
    "filename,dump",
    [
        ("example.yml", yaml.dump_to_string),
        ("example.json", json.dumps),
        ("example.yaml", yaml.dump_to_string),
        ("example.json", json_with_tabs),
    ],
)
@pytest.mark.parametrize("relative", (True, False), ids=("relative", "absolute"))
def test_load_from_path(tmp_path: Path, filename, dump, relative) -> None:
    yml_file = tmp_path.joinpath(filename)
    if relative:
        if not os.getenv("TEST_RELATIVE"):
            pytest.skip("Skipping relative path checks")
            return
        yml_file = yml_file.relative_to(Path.cwd())
    override1 = {"class_name": "ExampleClass", "module_name": "example_module"}
    override2 = {"class_name": "DifferentClass", "module_name": "different_module"}
    data = {
        "field_prefix": "blah",
        "class_overrides": {"Class1": override1, "Class2": override2},
        "project_name_override": "project-name",
        "package_name_override": "package_name",
        "package_version_override": "package_version",
    }
    yml_file.write_text(dump(data))

    config = ConfigFile.load_from_path(yml_file)
    assert config.field_prefix == "blah"
    assert config.class_overrides["Class1"].model_dump() == override1
    assert config.class_overrides["Class2"].model_dump() == override2
    assert config.project_name_override == "project-name"
    assert config.package_name_override == "package_name"
    assert config.package_version_override == "package_version"
