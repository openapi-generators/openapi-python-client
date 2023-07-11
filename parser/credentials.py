from typing import List

from dataclasses import dataclass

import openapi_schema_pydantic as osp
from openapi_python_client.utils import ClassName

from parser.context import OpenapiContext, SecurityScheme


@dataclass
class CredentialsProperty:
    schemes: List[SecurityScheme]

    @property
    def type_hint(self) -> str:
        if len(self.schemes) > 1:
            tmpl = "Union[{}]"
        else:
            tmpl = "{}"
        return tmpl.format(", ".join(scheme.class_name for scheme in self.schemes))

    def get_imports(self) -> List[str]:
        if len(self.schemes) > 1:
            return ["from typing import Union"]
        return []

    @classmethod
    def from_requirements(
        cls, requirements: List[osp.SecurityRequirement], context: OpenapiContext
    ) -> "CredentialsProperty":
        """Build property from endpoint security requirements"""
        schemes: List[SecurityScheme] = []
        for item in requirements:
            key = next(iter(item.keys()))
            scheme = context.get_security_scheme(key)
            schemes.append(SecurityScheme(scheme, ClassName(key + "Credentials", context.config.field_prefix)))

        return cls(schemes)
