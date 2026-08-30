from __future__ import annotations

from typing import Any, ClassVar, overload

from attr import define, field

from ... import schema as oai
from ...strings import PythonCode, PythonIdentifier, remove_string_escapes
from ..errors import PropertyError
from .protocol import PropertyProtocol, Value, convert_example


@define
class StringProperty(PropertyProtocol):
    """A property of type str"""

    name: oai.UntrustedString
    required: bool
    default: Value | None
    python_name: PythonIdentifier
    description: oai.UntrustedString | None
    example: oai.UntrustedString | None = field(converter=convert_example)
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
        name: oai.UntrustedString,
        required: bool,
        default: Any,
        python_name: PythonIdentifier,
        description: oai.UntrustedString | None,
        example: Any,
    ) -> StringProperty | PropertyError:
        checked_default = cls.convert_value(default)
        return cls(
            name=name,
            required=required,
            default=checked_default,
            python_name=python_name,
            description=description,
            example=example,
        )

    @classmethod
    @overload
    def convert_value(cls, value: None) -> None:  # type: ignore[misc]
        ...  # pragma: no cover

    @classmethod
    @overload
    def convert_value(cls, value: Any) -> Value: ...  # pragma: no cover

    @classmethod
    def convert_value(cls, value: Any) -> Value | None:
        if value is None or isinstance(value, Value):
            return value
        if not isinstance(value, str):
            value = str(value)
        return Value(python_code=PythonCode(repr(remove_string_escapes(value))), raw_value=value)
