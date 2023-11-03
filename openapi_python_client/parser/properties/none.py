from __future__ import annotations

from typing import ClassVar

from attr import define

from .protocol import PropertyProtocol, Value
from ..errors import PropertyError
from ... import schema as oai
from ...utils import PythonIdentifier


@define
class NoneProperty(PropertyProtocol):
    """A property that can only be None"""

    name: str
    required: bool
    default: Value | None
    python_name: PythonIdentifier
    description: str | None
    example: str | None

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
        name: str,
        required: bool,
        default: str | None,
        python_name: PythonIdentifier,
        description: str | None,
        example: str | None,
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
    def convert_value(cls, value: str | Value | None) -> Value | None | PropertyError:
        if isinstance(value, str):
            if value != "None":
                return PropertyError(f"Value {value} is not valid, onlly None is allowed")
            return Value(value)
        return value
