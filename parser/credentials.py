from typing import List, Optional, Set

from dataclasses import dataclass

import openapi_schema_pydantic as osp

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

    def get_imports(self) -> Set[str]:
        ret: Set[str] = set()
        if len(self.schemes) > 1:
            ret.add("from typing import Union")
        for item in self.schemes:
            ret.add(f"from .credentials import {item.class_name}")
        return ret

    @classmethod
    def from_requirements(
        cls, requirements: List[osp.SecurityRequirement], context: OpenapiContext
    ) -> "CredentialsProperty":
        """Build property from endpoint security requirements"""
        schemes: List[SecurityScheme] = []
        for item in requirements:
            key = next(iter(item.keys()))
            scheme = context.get_security_scheme(key)
            schemes.append(scheme)

        return cls(schemes)

    @classmethod
    def from_context(cls, context: OpenapiContext) -> Optional["CredentialsProperty"]:
        """Create property from all credentials. To be used in source"""
        schemes = list(context.security_schemes.values())
        if not schemes:
            return None
        return cls(schemes)
