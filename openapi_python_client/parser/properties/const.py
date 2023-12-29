from __future__ import annotations

from typing import Any

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
    value: Value
    default: Value | None
    python_name: PythonIdentifier
    description: str | None
    example: None

    @classmethod
    def build(
        cls,
        *,
        const: str | int,
        default: Any,
        name: str,
        python_name: PythonIdentifier,
        required: bool,
        description: str | None,
    ) -> ConstProperty | PropertyError:
        """
        Create a `ConstProperty` the right way.

        Args:
            const: The `const` value of the schema, indicating the literal value this represents
            default: The default value of this property, if any. Must be equal to `const` if set.
            name: The name of the property where it appears in the OpenAPI document.
            required: Whether this property is required where it's being used.
            python_name: The name used to represent this variable/property in generated Python code
            description: The description of this property, used for docstrings
        """
        value = cls._convert_value(const)
        if isinstance(value, PropertyError):
            return value

        prop = cls(
            value=value,
            python_name=python_name,
            name=name,
            required=required,
            default=None,
            description=description,
            example=None,
        )
        converted_default = prop.convert_value(default)
        if isinstance(converted_default, PropertyError):
            return converted_default
        prop.default = converted_default
        return prop

    def convert_value(self, value: Any) -> Value | None | PropertyError:
        value = self._convert_value(value)
        if value != self.value:
            return PropertyError(detail=f"Invalid value for const {self.name}; {value} != {self.value}")
        return value

    @staticmethod
    def _convert_value(value: Any) -> Value:
        if isinstance(value, Value):
            return value
        if isinstance(value, str):
            return StringProperty.convert_value(value)
        return Value(str(value))

    def get_type_string(
        self,
        no_optional: bool = False,
        json: bool = False,
        *,
        multipart: bool = False,
        quoted: bool = False,
    ) -> str:
        lit = f"Literal[{self.value}]"
        if not no_optional and not self.required:
            return f"Union[{lit}, Unset]"
        return lit

    def get_imports(self, *, prefix: str) -> set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        if self.required:
            return {"from typing import Literal"}
        return {
            "from typing import Literal, Union",
            f"from {prefix}types import UNSET, Unset",
        }
