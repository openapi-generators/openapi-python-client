from __future__ import annotations

from itertools import chain
from typing import Any, List, Set

import attr

from ... import Config, utils
from .property import Property
from .security_property import SecurityProperty


@attr.s(auto_attribs=True, frozen=True)
class CredentialsProperty(Property):
    """A property which refers to another Schema"""

    description: str
    security_properties: List[SecurityProperty]

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = super().get_imports(prefix=prefix)
        if len(self.security_properties) > 1:
            imports.update({"from typing import Union"})
        return imports

    def get_lazy_imports(self, *, prefix: str) -> Set[str]:
        """Get a set of lazy import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        return set(chain.from_iterable(t.get_lazy_imports(prefix=prefix) for t in self.security_properties))

    def get_type_string(
        self,
        no_optional: bool = False,
        json: bool = False,
        *,
        quoted: bool = False,
    ) -> str:
        """
        Get a string representation of type that should be used when declaring this property

        Args:
            no_optional: Do not include Optional or Unset even if the value is optional (needed for isinstance checks)
            json: True if the type refers to the property after JSON serialization
        """
        props = self.security_properties
        if len(props) == 1:
            return props[0].get_type_string()
        type_strings = ", ".join(p.get_type_string() for p in props)
        return f"Union[{type_strings}]"

    @property
    def is_populated(self) -> bool:
        return bool(self.security_properties)

    def to_string(self, default: Any = None, keyword: bool = True) -> str:
        pref = f"{self.python_name}: {self.get_type_string(quoted=True)}"
        if not keyword:
            return pref

        default = default or self.default
        return pref + f" = {default}"


def build_credentials_property(
    name: str, security_properties: List[SecurityProperty], config: Config
) -> CredentialsProperty:
    return CredentialsProperty(
        name=name,
        security_properties=security_properties,
        required=True,
        nullable=False,
        description="",
        python_name=utils.PythonIdentifier(name, prefix=config.field_prefix),
        default=None,
        example=None,
    )
