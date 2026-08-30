from __future__ import annotations

import datetime
from typing import Any, ClassVar

from attr import define, field

from ... import schema as oai
from ...strings import PythonCode, PythonIdentifier
from ..errors import PropertyError
from .protocol import PropertyProtocol, Value, convert_example


@define
class DateProperty(PropertyProtocol):
    """A property of type datetime.date"""

    name: oai.UntrustedString
    required: bool
    default: Value | None
    python_name: PythonIdentifier
    description: oai.UntrustedString | None
    example: oai.UntrustedString | None = field(converter=convert_example)

    _type_string: ClassVar[str] = "datetime.date"
    _json_type_string: ClassVar[str] = "str"
    template: ClassVar[str] = "date_property.py.jinja"

    @classmethod
    def build(
        cls,
        name: oai.UntrustedString,
        required: bool,
        default: Any,
        python_name: PythonIdentifier,
        description: oai.UntrustedString | None,
        example: Any,
    ) -> DateProperty | PropertyError:
        checked_default = cls.convert_value(default)
        if isinstance(checked_default, PropertyError):
            return checked_default

        return DateProperty(
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
                datetime.date.fromisoformat(value)  # make sure it's a valid value
            except ValueError as e:
                return PropertyError(f"Invalid date: {e}")
            return Value(python_code=PythonCode(f"datetime.date.fromisoformat({value!r})"), raw_value=value)
        return PropertyError(f"Cannot convert {value} to a date")

    def get_imports(self, *, prefix: str) -> set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = super().get_imports(prefix=prefix)
        imports.update({"import datetime", "from typing import cast"})
        return imports
