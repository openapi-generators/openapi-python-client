from __future__ import annotations

from typing import Any, ClassVar

from attr import define, field

from ... import schema as oai
from ...strings import PythonCode, PythonIdentifier
from ..errors import PropertyError
from .protocol import PropertyProtocol, Value, convert_example


@define
class FloatProperty(PropertyProtocol):
    """A property of type float"""

    name: oai.UntrustedString
    required: bool
    default: Value | None
    python_name: PythonIdentifier
    description: oai.UntrustedString | None
    example: oai.UntrustedString | None = field(converter=convert_example)

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
        name: oai.UntrustedString,
        required: bool,
        default: Any,
        python_name: PythonIdentifier,
        description: oai.UntrustedString | None,
        example: Any,
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
    def convert_value(cls, value: Any) -> Value | PropertyError | None:
        if isinstance(value, Value) or value is None:
            return value
        if isinstance(value, str):
            try:
                parsed = float(value)
                return Value(python_code=PythonCode(str(parsed)), raw_value=value)
            except ValueError:
                return PropertyError(f"Invalid float value: {value}")
        if isinstance(value, float):
            return Value(python_code=PythonCode(str(value)), raw_value=value)
        if isinstance(value, int) and not isinstance(value, bool):
            return Value(python_code=PythonCode(str(float(value))), raw_value=value)
        return PropertyError(f"Cannot convert {value} to a float")
