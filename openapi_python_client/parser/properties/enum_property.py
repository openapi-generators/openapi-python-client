__all__ = ["EnumProperty"]

from typing import Any, ClassVar, Dict, List, Optional, Set, Type, Union

import attr

from ... import utils
from ..reference import Reference
from .property import Property

ValueType = Union[str, int]


@attr.s(auto_attribs=True, frozen=True)
class EnumProperty(Property):
    """ A property that should use an enum """

    values: Dict[str, ValueType]
    reference: Reference
    value_type: Type[ValueType]
    default: Optional[Any] = attr.ib()

    template: ClassVar[str] = "enum_property.pyi"

    def get_type_string(self, no_optional: bool = False) -> str:
        """ Get a string representation of type that should be used when declaring this property """

        type_string = self.reference.class_name
        if no_optional:
            return type_string
        if self.nullable:
            type_string = f"Optional[{type_string}]"
        if not self.required:
            type_string = f"Union[Unset, {type_string}]"
        return type_string

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = super().get_imports(prefix=prefix)
        imports.add(f"from {prefix}models.{self.reference.module_name} import {self.reference.class_name}")
        return imports

    @staticmethod
    def values_from_list(values: List[ValueType]) -> Dict[str, ValueType]:
        """ Convert a list of values into dict of {name: value} """
        output: Dict[str, ValueType] = {}

        for i, value in enumerate(values):
            if isinstance(value, int):
                if value < 0:
                    output[f"VALUE_NEGATIVE_{-value}"] = value
                else:
                    output[f"VALUE_{value}"] = value
                continue
            if value[0].isalpha():
                key = value.upper()
            else:
                key = f"VALUE_{i}"
            if key in output:
                raise ValueError(f"Duplicate key {key} in Enum")
            sanitized_key = utils.snake_case(key).upper()
            output[sanitized_key] = utils.remove_string_escapes(value)
        return output
