__all__ = ["EnumProperty"]

from typing import Any, ClassVar, Dict, Optional, Sequence, Set, Type, Union

from attrs import define, field

from ... import schema as oai
from ... import utils
from .property import Property
from .schemas import Class

ValueType = Union[str, int]


@define
class EnumProperty(Property):
    """A property that should use an enum"""

    values: Dict[str, ValueType]
    class_info: Class
    value_type: Type[ValueType]
    default: Optional[Any] = field()

    template: ClassVar[str] = "enum_property.py.jinja"

    _allowed_locations: ClassVar[Set[oai.ParameterLocation]] = {
        oai.ParameterLocation.QUERY,
        oai.ParameterLocation.PATH,
        oai.ParameterLocation.COOKIE,
        oai.ParameterLocation.HEADER,
    }

    def get_base_type_string(self, *, quoted: bool = False) -> str:
        return self.class_info.name

    def get_base_json_type_string(self, *, quoted: bool = False) -> str:
        return self.value_type.__name__

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = super().get_imports(prefix=prefix)
        imports.add(f"from {prefix}models.{self.class_info.module_name} import {self.class_info.name}")
        return imports

    @staticmethod
    def values_from_list(
        values: Union[Sequence[str], Sequence[int]], case_sensitive_enums: bool = False
    ) -> Dict[str, ValueType]:
        """Convert a list of values into dict of {name: value}, where value can sometimes be None"""
        output: Dict[str, ValueType] = {}

        for value in values:
            if isinstance(value, int):
                if value < 0:
                    output[f"VALUE_NEGATIVE_{-value}"] = value
                else:
                    output[f"VALUE_{value}"] = value
                continue

            if case_sensitive_enums:
                sanitized_key = utils.case_insensitive_snake_case(value)
            else:
                sanitized_key = utils.snake_case(value.lower()).upper()
            if not value or not value[0].isalpha():
                sanitized_key = f"LITERAL_{sanitized_key}"

            if sanitized_key in output:
                raise ValueError(f"Duplicate key {sanitized_key} in Enum")

            output[sanitized_key] = utils.remove_string_escapes(value)

        return output
