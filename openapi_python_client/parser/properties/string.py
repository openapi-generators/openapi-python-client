from __future__ import annotations

from typing import ClassVar

from attr import define

from ... import schema as oai
from ... import utils
from ...utils import PythonIdentifier
from ..errors import PropertyError
from .protocol import PropertyProtocol, Value


@define
class StringProperty(PropertyProtocol):
    """A property of type str"""

    name: str
    required: bool
    default: Value | None
    python_name: PythonIdentifier
    description: str | None
    example: str | None
    max_length: int | None = None
    pattern: str | None = None
    _type_string: ClassVar[str] = "str"
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
        default: str | None | Value,
        python_name: PythonIdentifier,
        description: str | None,
        example: str | None,
        pattern: str | None = None,
    ) -> StringProperty | PropertyError:
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
            pattern=pattern,
        )

    @classmethod
    def convert_value(cls, value: str | Value | None) -> Value | None | PropertyError:
        if isinstance(value, str):
            return Value(repr(utils.remove_string_escapes(value)))
        return value
