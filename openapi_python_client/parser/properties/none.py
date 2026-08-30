from __future__ import annotations

from typing import Any, ClassVar

from attr import define, field

from ... import schema as oai
from ...strings import PythonCode, PythonIdentifier
from ..errors import PropertyError
from .protocol import PropertyProtocol, Value, convert_example


@define
class NoneProperty(PropertyProtocol):
    """A property that can only be None"""

    name: oai.UntrustedString
    required: bool
    default: Value | None
    python_name: PythonIdentifier
    description: oai.UntrustedString | None
    example: oai.UntrustedString | None = field(converter=convert_example)

    _allowed_locations: ClassVar[set[oai.ParameterLocation]] = {
        oai.ParameterLocation.QUERY,
        oai.ParameterLocation.COOKIE,
        oai.ParameterLocation.HEADER,
    }
    _type_string: ClassVar[str] = "None"
    _json_type_string: ClassVar[str] = "None"

    @classmethod
    def build(
        cls,
        name: oai.UntrustedString,
        required: bool,
        default: Any,
        python_name: PythonIdentifier,
        description: oai.UntrustedString | None,
        example: Any,
    ) -> NoneProperty | PropertyError:
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
            if value == "None":
                return Value(python_code=PythonCode(value), raw_value=value)
        return PropertyError(f"Value {value} is not valid, only None is allowed")
