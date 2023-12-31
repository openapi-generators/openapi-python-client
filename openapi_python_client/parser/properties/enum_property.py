from __future__ import annotations

__all__ = ["EnumProperty"]

from typing import Any, ClassVar, Union, cast

from attr import evolve
from attrs import define

from ... import Config, utils
from ... import schema as oai
from ...schema import DataType
from ..errors import PropertyError
from .none import NoneProperty
from .protocol import PropertyProtocol, Value
from .schemas import Class, Schemas
from .union import UnionProperty

ValueType = Union[str, int]


@define
class EnumProperty(PropertyProtocol):
    """A property that should use an enum"""

    name: str
    required: bool
    default: Value | None
    python_name: utils.PythonIdentifier
    description: str | None
    example: str | None
    values: dict[str, ValueType]
    class_info: Class
    value_type: type[ValueType]

    template: ClassVar[str] = "enum_property.py.jinja"

    _allowed_locations: ClassVar[set[oai.ParameterLocation]] = {
        oai.ParameterLocation.QUERY,
        oai.ParameterLocation.PATH,
        oai.ParameterLocation.COOKIE,
        oai.ParameterLocation.HEADER,
    }

    @classmethod
    def build(
        cls,
        *,
        data: oai.Schema,
        name: str,
        required: bool,
        schemas: Schemas,
        enum: list[str | None] | list[int | None],
        parent_name: str,
        config: Config,
    ) -> tuple[EnumProperty | NoneProperty | UnionProperty | PropertyError, Schemas]:
        """
        Create an EnumProperty from schema data.

        Args:
            data: The OpenAPI Schema which defines this enum.
            name: The name to use for variables which receive this Enum's value (e.g. model property name)
            required: Whether or not this Property is required in the calling context
            schemas: The Schemas which have been defined so far (used to prevent naming collisions)
            enum: The enum from the provided data. Required separately here to prevent extra type checking.
            parent_name: The context in which this EnumProperty is defined, used to create more specific class names.
            config: The global config for this run of the generator

        Returns:
            A tuple containing either the created property or a PropertyError AND update schemas.
        """

        if len(enum) == 0:
            return PropertyError(detail="No values provided for Enum", data=data), schemas

        # OpenAPI allows for null as an enum value, but it doesn't make sense with how enums are constructed in Python.
        # So instead, if null is a possible value, make the property nullable.
        # Mypy is not smart enough to know that the type is right though
        value_list: list[str] | list[int] = [value for value in enum if value is not None]  # type: ignore

        # It's legal to have an enum that only contains null as a value, we don't bother constructing an enum for that
        if len(value_list) == 0:
            return (
                NoneProperty.build(
                    name=name,
                    required=required,
                    default="None",
                    python_name=utils.PythonIdentifier(value=name, prefix=config.field_prefix),
                    description=None,
                    example=None,
                ),
                schemas,
            )
        if len(value_list) < len(enum):  # Only one of the values was None, that becomes a union
            data.oneOf = [
                oai.Schema(type=DataType.NULL),
                data.model_copy(update={"enum": value_list, "default": data.default}),
            ]
            data.enum = None
            return UnionProperty.build(
                data=data,
                name=name,
                required=required,
                schemas=schemas,
                parent_name=parent_name,
                config=config,
            )

        class_name = data.title or name
        if parent_name:
            class_name = f"{utils.pascal_case(parent_name)}{utils.pascal_case(class_name)}"
        class_info = Class.from_string(string=class_name, config=config)
        values = EnumProperty.values_from_list(value_list)

        if class_info.name in schemas.classes_by_name:
            existing = schemas.classes_by_name[class_info.name]
            if not isinstance(existing, EnumProperty) or values != existing.values:
                return (
                    PropertyError(
                        detail=f"Found conflicting enums named {class_info.name} with incompatible values.", data=data
                    ),
                    schemas,
                )

        value_type = type(next(iter(values.values())))

        prop = EnumProperty(
            name=name,
            required=required,
            class_info=class_info,
            values=values,
            value_type=value_type,
            default=None,
            python_name=utils.PythonIdentifier(value=name, prefix=config.field_prefix),
            description=data.description,
            example=data.example,
        )
        checked_default = prop.convert_value(data.default)
        if isinstance(checked_default, PropertyError):
            checked_default.data = data
            return checked_default, schemas
        prop = evolve(prop, default=checked_default)

        schemas = evolve(schemas, classes_by_name={**schemas.classes_by_name, class_info.name: prop})
        return prop, schemas

    def convert_value(self, value: Any) -> Value | PropertyError | None:
        if value is None or isinstance(value, Value):
            return value
        if isinstance(value, self.value_type):
            inverse_values = {v: k for k, v in self.values.items()}
            try:
                return Value(f"{self.class_info.name}.{inverse_values[value]}")
            except KeyError:
                return PropertyError(detail=f"Value {value} is not valid for enum {self.name}")
        return PropertyError(detail=f"Cannot convert {value} to enum {self.name} of type {self.value_type}")

    def get_base_type_string(self, *, quoted: bool = False) -> str:
        return self.class_info.name

    def get_base_json_type_string(self, *, quoted: bool = False) -> str:
        return self.value_type.__name__

    def get_imports(self, *, prefix: str) -> set[str]:
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
    def values_from_list(values: list[str] | list[int]) -> dict[str, ValueType]:
        """Convert a list of values into dict of {name: value}, where value can sometimes be None"""
        output: dict[str, ValueType] = {}

        for i, value in enumerate(values):
            value = cast(Union[str, int], value)
            if isinstance(value, int):
                if value < 0:
                    output[f"VALUE_NEGATIVE_{-value}"] = value
                else:
                    output[f"VALUE_{value}"] = value
                continue
            if value and value[0].isalpha():
                key = value.upper()
            else:
                key = f"VALUE_{i}"
            if key in output:
                raise ValueError(f"Duplicate key {key} in Enum")
            sanitized_key = utils.snake_case(key).upper()
            output[sanitized_key] = utils.remove_string_escapes(value)
        return output
