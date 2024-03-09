import json
import mimetypes
from pathlib import Path
from typing import Dict, List, Optional
import os

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
    project_name_override: Optional[str] = None
    package_name_override: Optional[str] = None
    package_version_override: Optional[str] = None
    use_path_prefixes_for_title_model_names: bool = True
    post_hooks: List[str] = [
        "autoflake -i -r --remove-all-unused-imports --remove-unused-variables .",
        "isort --float-to-top .",
        "black .",
    ]
    field_prefix: str = "field_"
    http_timeout: int = 5
    # include_methods: List[str] = ["get", "put", "post", "delete", "options", "head", "patch", "trace"]
    include_methods: List[str] = ["get"]
    default_openapi_title: str = "openapi"  # Fallback title when openapi info.title is missing or empty
    project_name_suffix: str = "-pipeline"
    dataset_name_suffix: str = "_data"

    openai_api_key: Optional[str] = os.environ.get("OPENAI_API_KEY")

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
