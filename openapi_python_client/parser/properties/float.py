from __future__ import annotations

from typing import ClassVar

from attr import define

from ... import schema as oai
from ...utils import PythonIdentifier
from ..errors import PropertyError
from .protocol import PropertyProtocol, Value


@define
class FloatProperty(PropertyProtocol):
    """A property of type float"""

    name: str
    required: bool
    default: Value | None
    python_name: PythonIdentifier
    description: str | None
    example: str | None

    _type_string: ClassVar[str] = "float"
    _json_type_string: ClassVar[str] = "float"
    _allowed_locations: ClassVar[set[oai.ParameterLocation]] = {
        oai.ParameterLocation.QUERY,
        oai.ParameterLocation.PATH,
        oai.ParameterLocation.COOKIE,
        oai.ParameterLocation.HEADER,
    }
    template: ClassVar[str] = "float_property.py.jinja"

    @classmethod
    def build(
        cls,
        name: str,
        required: bool,
        default: str | None | Value,
        python_name: PythonIdentifier,
        description: str | None,
        example: str | None,
    ) -> FloatProperty | PropertyError:
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
    def convert_value(cls, value: str | Value | None) -> Value | None | PropertyError:
        if isinstance(value, str):
            try:
                float(value)
            except ValueError:
                return PropertyError(f"Invalid float value: {value}")
            return Value(value)
        return value
