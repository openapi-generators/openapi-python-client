__all__ = ["EnumProperty"]

from typing import Any, ClassVar, Dict, List, Optional, Set, Type, Union, cast, Tuple

import attr

from ... import schema as oai
from ... import utils
from .property import Property
from .schemas import Class
from ... import Config
from ... import schema as oai
from ..errors import PropertyError
from .schemas import Schemas
from .types import NoneProperty

ValueType = Union[str, int]


@attr.s(auto_attribs=True, frozen=True)
class EnumProperty(Property):
    """A property that should use an enum"""

    values: Dict[str, ValueType]
    class_info: Class
    value_type: Type[ValueType]
    default: Optional[Any] = attr.ib()

    template: ClassVar[str] = "enum_property.py.jinja"

    _allowed_locations: ClassVar[Set[oai.ParameterLocation]] = {
        oai.ParameterLocation.QUERY,
        oai.ParameterLocation.PATH,
        oai.ParameterLocation.COOKIE,
        oai.ParameterLocation.HEADER,
    }

    # pylint: disable=unused-argument
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
    def values_from_list(values: Union[List[str], List[int]]) -> Dict[str, ValueType]:
        """Convert a list of values into dict of {name: value}, where value can sometimes be None"""
        output: Dict[str, ValueType] = {}

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


def build_enum_property(
    *,
    data: oai.Schema,
    name: str,
    required: bool,
    schemas: Schemas,
    enum: Union[List[Optional[str]], List[Optional[int]]],
    parent_name: Optional[str],
    config: Config,
) -> Tuple[Union[EnumProperty, NoneProperty, PropertyError], Schemas]:
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
        A tuple containing either the created property or a PropertyError describing what went wrong AND update schemas.
    """

    if len(enum) == 0:
        return PropertyError(detail="No values provided for Enum", data=data), schemas

    class_name = data.title or name
    if parent_name:
        class_name = f"{utils.pascal_case(parent_name)}{utils.pascal_case(class_name)}"
    class_info = Class.from_string(string=class_name, config=config)

    # OpenAPI allows for null as an enum value, but it doesn't make sense with how enums are constructed in Python.
    # So instead, if null is a possible value, make the property nullable.
    # Mypy is not smart enough to know that the type is right though
    value_list: Union[List[str], List[int]] = [value for value in enum if value is not None]  # type: ignore
    if len(value_list) < len(enum):
        data.nullable = True

    # It's legal to have an enum that only contains null as a value, we don't bother constructing an enum in that case
    if len(value_list) == 0:
        return (
            NoneProperty(
                name=name,
                required=required,
                nullable=False,
                default="None",
                python_name=utils.PythonIdentifier(value=name, prefix=config.field_prefix),
                description=None,
                example=None,
            ),
            schemas,
        )
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
        nullable=data.nullable,
        class_info=class_info,
        values=values,
        value_type=value_type,
        default=None,
        python_name=utils.PythonIdentifier(value=name, prefix=config.field_prefix),
        description=data.description,
        example=data.example,
    )

    default = get_enum_default(prop, data)
    if isinstance(default, PropertyError):
        return default, schemas
    prop = attr.evolve(prop, default=default)

    schemas = attr.evolve(schemas, classes_by_name={**schemas.classes_by_name, class_info.name: prop})
    return prop, schemas


def get_enum_default(prop: EnumProperty, data: oai.Schema) -> Union[Optional[str], PropertyError]:
    """
    Run through the available values in an EnumProperty and return the string representing the default value
    in `data`.

    Args:
        prop: The EnumProperty to search for the default value.
        data: The schema containing the default value for this enum.

    Returns:
        If `default` is `None`, then `None`.
            If `default` is a valid value in `prop`, then the string representing that variant (e.g. MyEnum.MY_VARIANT)
            If `default` is a value that doesn't match a variant of the enum, then a `PropertyError`.
    """
    default = data.default
    if default is None:
        return None

    inverse_values = {v: k for k, v in prop.values.items()}
    try:
        return f"{prop.class_info.name}.{inverse_values[default]}"
    except KeyError:
        return PropertyError(detail=f"{default} is an invalid default for enum {prop.class_info.name}", data=data)
