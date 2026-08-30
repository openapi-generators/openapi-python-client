from __future__ import annotations

from typing import Any, ClassVar
from uuid import UUID

from attr import define, field

from ... import schema as oai
from ...strings import PythonCode, PythonIdentifier
from ..errors import PropertyError
from .protocol import PropertyProtocol, Value, convert_example


@define
class UuidProperty(PropertyProtocol):
    """A property of type uuid.UUID"""

    name: oai.UntrustedString
    required: bool
    default: Value | None
    python_name: PythonIdentifier
    description: oai.UntrustedString | None
    example: oai.UntrustedString | None = field(converter=convert_example)

    _type_string: ClassVar[str] = "UUID"
    _json_type_string: ClassVar[str] = "str"
    _allowed_locations: ClassVar[set[oai.ParameterLocation]] = {
        oai.ParameterLocation.QUERY,
        oai.ParameterLocation.PATH,
        oai.ParameterLocation.COOKIE,
        oai.ParameterLocation.HEADER,
    }
    template: ClassVar[str] = "uuid_property.py.jinja"

    @classmethod
    def build(
        cls,
        name: oai.UntrustedString,
        required: bool,
        default: Any,
        python_name: PythonIdentifier,
        description: oai.UntrustedString | None,
        example: Any,
    ) -> UuidProperty | PropertyError:
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
        )

    @classmethod
    def convert_value(cls, value: Any) -> Value | PropertyError | None:
        if value is None or isinstance(value, Value):
            return value
        if isinstance(value, str):
            try:
                UUID(value)
            except ValueError:
                return PropertyError(f"Invalid UUID value: {value}")
            return Value(python_code=PythonCode(f"UUID('{value}')"), raw_value=value)
        return PropertyError(f"Invalid UUID value: {value}")

    def get_imports(self, *, prefix: str) -> set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = super().get_imports(prefix=prefix)
        imports.update({"from uuid import UUID"})
        return imports
