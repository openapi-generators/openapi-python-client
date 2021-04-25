from pathlib import Path
from typing import Dict, Optional

import yaml
from pydantic import BaseModel


class ClassOverride(BaseModel):
    class_name: Optional[str] = None
    module_name: Optional[str] = None


class Config(BaseModel):
    class_overrides: Dict[str, ClassOverride] = {}
    project_name_override: Optional[str]
    package_name_override: Optional[str]
    package_version_override: Optional[str]
    field_prefix: str = "field_"

    @staticmethod
    def load_from_path(path: Path) -> "Config":
        """Creates a Config from provided JSON or YAML file and sets a bunch of globals from it"""
        from . import utils

        config_data = yaml.safe_load(path.read_text())
        config = Config(**config_data)
        utils.FIELD_PREFIX = config.field_prefix
        return config
