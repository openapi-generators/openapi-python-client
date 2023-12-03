from __future__ import annotations

from typing import ClassVar

from attr import define

from ...utils import PythonIdentifier
from ..errors import PropertyError
from .protocol import PropertyProtocol, Value
from .string import StringProperty


@define
class ConstProperty(PropertyProtocol):
    """A property representing a Union (anyOf) of other properties"""

    name: str
    required: bool
    default: Value
    python_name: PythonIdentifier
    description: str | None
    example: None
    template: ClassVar[str] = "const_property.py.jinja"

    @classmethod
    def build(
        cls,
        *,
        const: None | str | int,
        name: str,
        python_name: PythonIdentifier,
        required: bool,
        description: str | None,
    ) -> ConstProperty | PropertyError:
        """
        Create a `ConstProperty` the right way.

        Args:
            const: The `const` value of the schema, indicating the literal value this represents
            name: The name of the property where it appears in the OpenAPI document.
            required: Whether this property is required where it's being used.
            python_name: The name used to represent this variable/property in generated Python code
            description: The description of this property, used for docstrings
        """
        default: Value | PropertyError = PropertyError(
            detail="Invalid const value, only null, strings, and ints are supported."
        )
        if const is None:
            default = Value("None")
        elif isinstance(const, str):
            # this can't ever be None, but the Python type system can't represent that
            default = StringProperty.convert_value(const)  # type: ignore
        elif isinstance(const, int):
            default = Value(repr(const))

        if isinstance(default, PropertyError):
            return default

        return cls(
            python_name=python_name,
            name=name,
            required=required,
            default=default,
            description=description,
            example=None,
        )

    def convert_value(self, value: str | Value | None | int) -> Value | PropertyError:
        value_or_error: Value | PropertyError
        if isinstance(value, str):
            # this can't ever be None, but the Python type system can't represent that
            value_or_error = StringProperty.convert_value(value)  # type: ignore
        elif isinstance(value, int):
            value_or_error = Value(repr(value))
        elif value is None:
            value_or_error = Value("None")
        elif isinstance(value, Value):
            value_or_error = value
        if isinstance(value, PropertyError):
            return value
        if value_or_error != self.default:
            return PropertyError(detail=f"Invalid value for const {self.name}")
        return value_or_error

    def get_type_string(
        self,
        no_optional: bool = False,
        json: bool = False,
        *,
        multipart: bool = False,
        quoted: bool = False,
    ) -> str:
        return f"Literal[{self.default}]"

    def get_imports(self, *, prefix: str) -> set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        return {"from typing import Literal"}
