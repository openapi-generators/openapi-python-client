import json
import mimetypes
from pathlib import Path
from typing import Dict, List, Optional

import yaml
from pydantic import BaseModel


class ClassOverride(BaseModel):
    """An override of a single generated class.

    See https://github.com/openapi-generators/openapi-python-client#class_overrides
    """

    class_name: Optional[str] = None
    module_name: Optional[str] = None


class Config(BaseModel):
    """Contains any configurable values passed by the user.

    See https://github.com/openapi-generators/openapi-python-client#configuration
    """

    class_overrides: Dict[str, ClassOverride] = {}
    project_name_override: Optional[str]
    package_name_override: Optional[str]
    package_version_override: Optional[str]
    post_hooks: List[str] = [
        "autoflake -i -r --remove-all-unused-imports --remove-unused-variables --ignore-init-module-imports .",
        "isort .",
        "black .",
    ]
    field_prefix: str = "field_"

    @staticmethod
    def load_from_path(path: Path) -> "Config":
        """Creates a Config from provided JSON or YAML file and sets a bunch of globals from it"""
        mime = mimetypes.guess_type(path.absolute().as_uri(), strict=True)[0]
        if mime == "application/json":
            config_data = json.loads(path.read_text())
        else:
            config_data = yaml.safe_load(path.read_text())
        config = Config(**config_data)
        return config
