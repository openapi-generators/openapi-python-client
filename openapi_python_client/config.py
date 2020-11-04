from pathlib import Path
from typing import Dict, Optional

import yaml
from pydantic import BaseModel


class ClassOverride(BaseModel):
    class_name: str
    module_name: str


class Config(BaseModel):
    class_overrides: Optional[Dict[str, ClassOverride]]
    project_name_override: Optional[str]
    package_name_override: Optional[str]
    package_version_override: Optional[str]
    field_prefix: Optional[str]

    def load_config(self) -> None:
        """ Sets globals based on Config """
        from openapi_python_client import Project

        from . import utils
        from .parser import reference

        if self.class_overrides is not None:
            for class_name, class_data in self.class_overrides.items():
                reference.class_overrides[class_name] = reference.Reference(**dict(class_data))

        Project.project_name_override = self.project_name_override
        Project.package_name_override = self.package_name_override
        Project.package_version_override = self.package_version_override

        if self.field_prefix is not None:
            utils.FIELD_PREFIX = self.field_prefix

    @staticmethod
    def load_from_path(path: Path) -> None:
        """ Creates a Config from provided JSON or YAML file and sets a bunch of globals from it """
        config_data = yaml.safe_load(path.read_text())
        Config(**config_data).load_config()
