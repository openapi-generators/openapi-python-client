from __future__ import annotations

from typing import ClassVar

from attr import define

from ...utils import PythonIdentifier
from .protocol import PropertyProtocol, Value


@define
class AnyProperty(PropertyProtocol):
    """A property that can be any type (used for empty schemas)"""

    @classmethod
    def build(
        cls,
        name: str,
        required: bool,
        default: str | None,
        python_name: PythonIdentifier,
        description: str | None,
        example: str | None,
    ) -> AnyProperty:
        return cls(
            name=name,
            required=required,
            default=Value(default) if default is not None else None,
            python_name=python_name,
            description=description,
            example=example,
        )

    @classmethod
    def convert_value(cls, value: str | Value | None) -> Value | None:
        if isinstance(value, str):
            return Value(value)
        return value

    name: str
    required: bool
    default: Value | None
    python_name: PythonIdentifier
    description: str | None
    example: str | None
    _type_string: ClassVar[str] = "Any"
    _json_type_string: ClassVar[str] = "Any"
