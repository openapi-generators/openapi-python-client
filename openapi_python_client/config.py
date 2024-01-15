import json
import mimetypes
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Union

import yaml
from attr import define
from pydantic import BaseModel


class ClassOverride(BaseModel):
    """An override of a single generated class.

    See https://github.com/openapi-generators/openapi-python-client#class_overrides
    """

    class_name: Optional[str] = None
    module_name: Optional[str] = None


class MetaType(str, Enum):
    """The types of metadata supported for project generation."""

    NONE = "none"
    POETRY = "poetry"
    SETUP = "setup"
    PDM = "pdm"


class ConfigFile(BaseModel):
    """Contains any configurable values passed via a config file.

    See https://github.com/openapi-generators/openapi-python-client#configuration
    """

    class_overrides: Optional[Dict[str, ClassOverride]] = None
    project_name_override: Optional[str] = None
    package_name_override: Optional[str] = None
    package_version_override: Optional[str] = None
    use_path_prefixes_for_title_model_names: bool = True
    post_hooks: Optional[List[str]] = None
    field_prefix: str = "field_"
    http_timeout: int = 5

    @staticmethod
    def load_from_path(path: Path) -> "ConfigFile":
        """Creates a Config from provided JSON or YAML file and sets a bunch of globals from it"""
        mime = mimetypes.guess_type(path.absolute().as_uri(), strict=True)[0]
        if mime == "application/json":
            config_data = json.loads(path.read_text())
        else:
            config_data = yaml.safe_load(path.read_text())
        config = ConfigFile(**config_data)
        return config


@define
class Config:
    """Contains all the config values for the generator, from files, defaults, and CLI arguments."""

    meta_type: MetaType
    class_overrides: Dict[str, ClassOverride]
    project_name_override: Optional[str]
    package_name_override: Optional[str]
    package_version_override: Optional[str]
    use_path_prefixes_for_title_model_names: bool
    post_hooks: List[str]
    field_prefix: str
    http_timeout: int
    document_source: Union[Path, str]
    file_encoding: str

    @staticmethod
    def from_sources(
        config_file: ConfigFile, meta_type: MetaType, document_source: Union[Path, str], file_encoding: str
    ) -> "Config":
        if config_file.post_hooks is not None:
            post_hooks = config_file.post_hooks
        elif meta_type == MetaType.NONE:
            post_hooks = [
                "ruff check . --fix --extend-select=I",
                "ruff format .",
            ]
        else:
            post_hooks = [
                "ruff check --fix .",
                "ruff format .",
            ]

        config = Config(
            meta_type=meta_type,
            class_overrides=config_file.class_overrides or {},
            project_name_override=config_file.project_name_override,
            package_name_override=config_file.package_name_override,
            package_version_override=config_file.package_version_override,
            use_path_prefixes_for_title_model_names=config_file.use_path_prefixes_for_title_model_names,
            post_hooks=post_hooks,
            field_prefix=config_file.field_prefix,
            http_timeout=config_file.http_timeout,
            document_source=document_source,
            file_encoding=file_encoding,
        )
        return config
