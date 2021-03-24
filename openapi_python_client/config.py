from pathlib import Path
from typing import Dict, Optional

import yaml
from pydantic import BaseModel

from openapi_python_client.parser.properties import Class


class Config(BaseModel):
    class_overrides: Dict[str, Class] = {}
    project_name_override: Optional[str]
    package_name_override: Optional[str]
    package_version_override: Optional[str]
    field_prefix: str = "field_"

    @staticmethod
    def load_from_path(path: Path) -> "Config":
        """ Creates a Config from provided JSON or YAML file and sets a bunch of globals from it """
        config_data = yaml.safe_load(path.read_text())
        return Config(**config_data)
