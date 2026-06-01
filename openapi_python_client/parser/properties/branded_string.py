from __future__ import annotations

from typing import Any, ClassVar

from attr import define

from ... import schema as oai
from ...utils import PythonIdentifier
from ..errors import PropertyError
from .protocol import PropertyProtocol, Value
from .string import StringProperty

BRAND_PREFIX = "brand::"


@define
class BrandedStringProperty(PropertyProtocol):
    """A string whose runtime type is a custom, branded Python type.

    Produced when a string schema's ``format`` is of the form
    ``brand::<namespace>::<TypeName>``. The generated field is typed as
    ``<TypeName>`` and imported from a module mapped from ``<namespace>``.
    """

    name: str
    required: bool
    default: Value | None
    python_name: PythonIdentifier
    description: str | None
    example: str | None
    brand_module: str
    brand_type: str

    _json_type_string: ClassVar[str] = "str"
    _allowed_locations: ClassVar[set[oai.ParameterLocation]] = {
        oai.ParameterLocation.QUERY,
        oai.ParameterLocation.PATH,
        oai.ParameterLocation.COOKIE,
        oai.ParameterLocation.HEADER,
    }

    @classmethod
    def build(
        cls,
        name: str,
        required: bool,
        default: Any,
        python_name: PythonIdentifier,
        description: str | None,
        example: str | None,
        brand_module: str,
        brand_type: str,
    ) -> BrandedStringProperty | PropertyError:
        checked_default = cls.convert_value(default)
        if isinstance(checked_default, PropertyError):
            return checked_default
        return cls(
            name=name,
            required=required,
            default=checked_default,
            python_name=python_name,
            description=description,
            example=example,
            brand_module=brand_module,
            brand_type=brand_type,
        )

    @classmethod
    def convert_value(cls, value: Any) -> Value | None | PropertyError:
        return StringProperty.convert_value(value)

    def get_base_type_string(self) -> str:
        return self.brand_type

    def get_imports(self, *, prefix: str) -> set[str]:
        imports = super().get_imports(prefix=prefix)
        imports.add(f"from {self.brand_module} import {self.brand_type}")
        return imports


_BRAND_MODULES: dict[str, str] = {
    "protected": "tandem_platform.schema.protected",
}


def parse_brand_format(schema_format: str | None) -> tuple[str, str] | None:
    """Parse a branded ``format`` value into (module, type_name).

    Returns None if the format is not a recognized brand.
    """
    if not schema_format or not schema_format.startswith(BRAND_PREFIX):
        return None
    parts = schema_format.split("::")
    if len(parts) != 3 or parts[0] != "brand":
        return None
    _, namespace, type_name = parts
    module = _BRAND_MODULES.get(namespace)
    if module is None or not type_name:
        return None
    return module, type_name
