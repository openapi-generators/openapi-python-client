__all__ = ["EnumProperty"]

from dataclasses import InitVar, dataclass, field
from typing import Any, ClassVar, Dict, List, Set, Type, Union

from ... import utils
from ..errors import ValidationError
from ..reference import Reference
from .property import Property

ValueType = Union[str, int]


@dataclass
class EnumProperty(Property):
    """ A property that should use an enum """

    values: Dict[str, ValueType]
    reference: Reference = field(init=False)
    value_type: Type[ValueType] = field(init=False)

    title: InitVar[str]
    existing_enums: InitVar[Dict[str, "EnumProperty"]]

    template: ClassVar[str] = "enum_property.pyi"

    def __post_init__(self, title: str, existing_enums: Dict[str, "EnumProperty"]) -> None:  # type: ignore
        reference = Reference.from_ref(title)
        dedup_counter = 0
        while reference.class_name in existing_enums:
            existing = existing_enums[reference.class_name]
            if self.values == existing.values:
                break  # This is the same Enum, we're good
            dedup_counter += 1
            reference = Reference.from_ref(f"{reference.class_name}{dedup_counter}")

        self.reference = reference

        for value in self.values.values():
            self.value_type = type(value)
            break

        super().__post_init__()

    def get_type_string(self, no_optional: bool = False) -> str:
        """ Get a string representation of type that should be used when declaring this property """

        if no_optional or (self.required and not self.nullable):
            return self.reference.class_name
        return f"Optional[{self.reference.class_name}]"

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

    def _validate_default(self, default: Any) -> str:
        inverse_values = {v: k for k, v in self.values.items()}
        try:
            return f"{self.reference.class_name}.{inverse_values[default]}"
        except KeyError as e:
            raise ValidationError() from e
