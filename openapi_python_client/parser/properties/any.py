from __future__ import annotations

from typing import Any, ClassVar

from attr import define, field

from ...schema.untrusted_string import UntrustedString
from ...strings import PythonCode, PythonIdentifier
from .protocol import PropertyProtocol, Value, convert_example


@define
class AnyProperty(PropertyProtocol):
    """A property that can be any type (used for empty schemas)"""

    @classmethod
    def build(
        cls,
        name: UntrustedString,
        required: bool,
        default: Any,
        python_name: PythonIdentifier,
        description: UntrustedString | None,
        example: Any,
    ) -> AnyProperty:
        return cls(
            name=name,
            required=required,
            default=AnyProperty.convert_value(default),
            python_name=python_name,
            description=description,
            example=example,
        )

    @classmethod
    def convert_value(cls, value: Any) -> Value | None:
        from .string import StringProperty  # noqa: PLC0415

        if value is None:
            return value
        if isinstance(value, str):
            return StringProperty.convert_value(value)
        return Value(python_code=PythonCode(str(value)), raw_value=value)

    name: UntrustedString
    required: bool
    default: Value | None
    python_name: PythonIdentifier
    description: UntrustedString | None
    example: UntrustedString | None = field(converter=convert_example)
    _type_string: ClassVar[str] = "Any"
    _json_type_string: ClassVar[str] = "Any"
