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

    def load_config(self) -> None:
        """ Loads config from provided Path """

        if self.class_overrides is not None:
            from .parser import reference

            for class_name, class_data in self.class_overrides.items():
                reference.class_overrides[class_name] = reference.Reference(**dict(class_data))

        from openapi_python_client import Project

        Project.project_name_override = self.project_name_override
        Project.package_name_override = self.package_name_override

    @staticmethod
    def load_from_path(path: Path) -> None:
        config_data = yaml.safe_load(path.read_text())
        Config(**config_data).load_config()
