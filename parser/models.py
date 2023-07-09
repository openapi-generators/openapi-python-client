dfrom typing import (
    Literal,
    TYPE_CHECKING,
    Optional,
    Union,
    List,
    TypeVar,
    Any,
    Iterable,
    Sequence,
    cast,
    Set,
    Tuple,
    Dict,
)
from itertools import chain

from dataclasses import dataclass, field

import openapi_schema_pydantic as osp

from parser.types import DataType
from openapi_python_client.parser.properties.converter import convert


if TYPE_CHECKING:
    from parser.context import OpenapiContext


TSchemaType = Literal["boolean", "object", "array", "number", "string", "integer"]


@dataclass
class DataPropertyPath:
    """Describes a json path to a property"""

    path: Tuple[str, ...]
    prop: "SchemaWrapper"

    @property
    def json_path(self) -> str:
        return ".".join(self.path)

    def __str__(self) -> str:
        return f"DataPropertyPath {self.path}: {self.prop.name}"


@dataclass
class SchemaWrapper:
    """Wraps an openapi Schema to add useful attributes and methods"""

    schema: osp.Schema
    ref: Optional[osp.Reference]

    name: str
    """Name inferred from schema ref url or Schema.title property"""

    description: Optional[str]
    """Description from schema ref or schema.description property"""

    properties: List["Property"]

    types: List[TSchemaType]
    nullable: bool
    default: Optional[Any]
    """Default value of the schema (optional)"""

    array_item: Optional["SchemaWrapper"] = None
    all_of: List["SchemaWrapper"] = field(default_factory=list)
    any_of: List["SchemaWrapper"] = field(default_factory=list)
    one_of: List["SchemaWrapper"] = field(default_factory=list)

    @property
    def is_object(self) -> bool:
        return "object" in self.types

    @property
    def is_list(self) -> bool:
        return "array" in self.types

    @property
    def property_template(self) -> str:
        if self.is_union:
            return "union_property.py.jinja"
        elif self.types == ["integer"]:
            return "int_property.py.jinja"
        elif self.types == ["float"]:
            return "float_property.py.jinja"
        elif self.types == ["boolean"]:
            return "boolean_property.py.jinja"
        return "any_property.py.jinja"

    @property
    def union_schemas(self) -> List["SchemaWrapper"]:
        return self.any_of + self.one_of

    @property
    def is_union(self) -> bool:
        return not not self.union_schemas or len(self.types) > 1

    @property
    def type_hint(self) -> str:
        return DataType.from_schema(self).type_hint

    @classmethod
    def from_reference_guarded(
        cls,
        schema_ref: Union[osp.Schema, osp.Reference],
        context: "OpenapiContext",
        parent_properties: Optional[Sequence["Property"]] = None,
        level: int = 0,
    ) -> Optional["SchemaWrapper"]:
        if level > 3:
            return None
        level += 1
        return cls.from_reference(schema_ref, context, level=level)

    @classmethod
    def from_reference(
        cls,
        schema_ref: Union[osp.Schema, osp.Reference],
        context: "OpenapiContext",
        level: int = 0,
        parent_properties: Optional[Sequence["Property"]] = None,
    ) -> "SchemaWrapper":
        """Create a Schema wrapper from openapi Schema or reference.
        Recursively generates properties and nested allOf/anyOf/oneOf schemas up to max nesting level

        Args:
            schema_ref: The openapi schema or reference (`$ref`) object pointing to a schema
            context: The parser context
            level: Current recursion level. Used to prevent infinite recursion cycles.
        """
        name, schema = context.schema_and_name_from_reference(schema_ref)

        all_of = _remove_nones([cls.from_reference_guarded(ref, context, level=level) for ref in schema.allOf or []])

        # Properties from all_of child schemas should be merged
        property_map = {prop.name: prop for prop in parent_properties or []}
        property_map.update({prop.name: prop for prop in chain.from_iterable(s.properties for s in all_of)})
        required_props = set(schema.required or [])

        _props_list = _remove_nones(
            [
                Property.from_reference_guarded(name, ref, name in required_props, context, level=level)
                for name, ref in (schema.properties or {}).items()
            ]
        )

        property_map.update({prop.name: prop for prop in _props_list})

        properties = list(property_map.values())

        one_of = _remove_nones(
            [
                cls.from_reference_guarded(ref, context, parent_properties=properties, level=level)
                for ref in schema.oneOf or []
            ]
        )

        any_of = _remove_nones(
            [
                cls.from_reference_guarded(ref, context, parent_properties=properties, level=level)
                for ref in schema.anyOf or []
            ]
        )

        description = schema_ref.description or schema.description

        # TODO: may want to handle prefix items (tuple)
        array_item: Optional["SchemaWrapper"] = None
        if schema.items:
            array_item = cls.from_reference_guarded(schema.items, context, level=level)

        # Single type in OAI 3.0, list of types in 3.1
        # Nullable does not exist in 3.1, instead types: ["string", "null"]
        nullable = False
        if schema.type:
            if not isinstance(schema.type, list):
                schema_types = [schema.type]
            else:
                schema_types = schema.type.copy()
            if "null" in schema_types:
                nullable = True
                schema_types.remove("null")
        else:
            # TODO: Fallback on string. Should warn
            schema_types = ["string"]

        default = schema.default
        # Only do string escaping, other types can go as-is
        if isinstance(default, str):
            default = convert("str", default)

        return cls(
            schema=schema,
            name=name,
            description=description,
            ref=schema_ref if isinstance(schema_ref, osp.Reference) else None,
            properties=properties,
            all_of=all_of,
            one_of=one_of,
            any_of=any_of,
            types=cast(List[TSchemaType], schema_types),
            nullable=nullable,
            array_item=array_item,
            default=default,
        )


@dataclass
class Property:
    name: str
    required: bool
    schema: SchemaWrapper

    @property
    def is_list(self) -> bool:
        return self.schema.is_list

    @property
    def is_object(self) -> bool:
        return self.schema.is_object

    def type_hint(self) -> str:
        return self.schema.type_hint

    @classmethod
    def from_reference_guarded(
        cls,
        name: str,
        schema_ref: Union[osp.Schema, osp.Reference],
        required: bool,
        context: "OpenapiContext",
        level: int = 0,
    ) -> "Property":
        if level >= 3:
            return None
        schema = SchemaWrapper.from_reference_guarded(schema_ref, context, level=level)
        return cls(name=name, required=required, schema=schema)


T = TypeVar("T", bound=Any)


def _remove_nones(seq: Iterable[Optional[T]]) -> List[T]:
    return [x for x in seq if x is not None]


def traverse_properties(
    property_obj: Property,
    path: Tuple[str, ...] = (),
    list_properties: Optional[Dict[Tuple[str, ...], Property]] = None,
    model_properties: Optional[Dict[Tuple[str, ...], Property]] = None,
    seen: Optional[Set[str]] = None,
) -> Tuple[Dict[Tuple[str, ...], SchemaWrapper], Dict[Tuple[str, ...], Property]]:
    """
    Recursively traverse a ModelProperty or ListProperty object to generate mappings of:

    a. All ListProperty objects which contain models (arrays of objects in openapi)
    b. All ModelProperty descendents of the property

    The result is a tuple of two dicts with json paths as keys and `ModelProperty` objects as values.

    :param property_obj: The ModelProperty or ListProperty object to traverse.
    :param path: The current path, used for constructing the path to each property.
    :param list_properties: Optional. A dictionary to store the paths referencing ListProperty
                            objects with ModelProperty as their inner property.
    :param model_properties: Optional. A dictionary to store the paths referencing ModelProperty objects.
    :return: A tuple containing two dictionaries, mapping jsonpaths to ModelProperty objects
    """
    if list_properties is None:
        list_properties = {}
    if model_properties is None:
        model_properties = {}
    if seen is None:
        seen = set()

    array_item = property_obj.schema.array_item

    if property_obj.is_object:
        # Avoid infinite self referencing call cycles
        # if property_obj.class_info.name in seen:
        #     return list_properties, model_properties

        # seen.add(property_obj.class_info.name)
        model_properties[path] = property_obj
        for prop in property_obj.schema.properties:
            # for prop in property_obj.optional_properties or []:
            if prop.is_list or prop.is_object:
                traverse_properties(prop, path + (prop.name,), list_properties, model_properties, seen)

        # for prop in property_obj.required_properties or []:
        #     if isinstance(prop, (ModelProperty, ListProperty)):
        #         traverse_properties(prop, path + (prop.name,), list_properties, model_properties, seen)

    elif property_obj.is_list and array_item and array_item.is_object:
        # elif isinstance(property_obj, ListProperty) and isinstance(property_obj.inner_property, ModelProperty):
        inner = Property("", True, array_item)
        # inner = property_obj.inner_property
        list_properties[path] = inner
        traverse_properties(inner, path + ("[*]",), list_properties, model_properties, seen)

    return list_properties, model_properties
