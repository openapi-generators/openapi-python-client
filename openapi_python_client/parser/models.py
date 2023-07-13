from __future__ import annotations
from typing import Literal, TYPE_CHECKING, Optional, Union, List, TypeVar, Any, Iterable, Sequence, cast, Tuple, Dict
from itertools import chain
from dataclasses import dataclass, field

from dlt.common.utils import digest128

import openapi_schema_pydantic as osp
from openapi_python_client.parser.types import DataType
from openapi_python_client.parser.properties.converter import convert

if TYPE_CHECKING:
    from openapi_python_client.parser.context import OpenapiContext


TSchemaType = Literal["boolean", "object", "array", "number", "string", "integer"]

MAX_RECURSION_DEPTH = 4


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

    crawled_properties: SchemaCrawler
    hash_key: str

    array_item: Optional["SchemaWrapper"] = None
    all_of: List["SchemaWrapper"] = field(default_factory=list)
    any_of: List["SchemaWrapper"] = field(default_factory=list)
    one_of: List["SchemaWrapper"] = field(default_factory=list)

    @property
    def has_properties(self) -> bool:
        return bool(self.properties or self.any_of or self.all_of)

    @property
    def all_properties(self) -> List["Property"]:
        props = {p.name: p for p in self.properties}
        for child in self.any_of + self.one_of:
            for prop in child.all_properties:
                if prop.name in props:
                    continue
                props[prop.name] = prop
        return list(props.values())

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
        if level >= MAX_RECURSION_DEPTH:
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

        crawler = SchemaCrawler()
        result = cls(
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
            crawled_properties=crawler,
            hash_key=digest128(schema.json(sort_keys=True)),
        )
        crawler.crawl(result)
        return result


@dataclass
class Property:
    name: str
    required: bool
    schema: SchemaWrapper

    def get_imports(self) -> List[str]:
        imports = []
        if self.schema.is_union:
            imports.append("from typing import Union")
        # TODO: other types
        return imports

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
        if level >= MAX_RECURSION_DEPTH:
            return None
        schema = SchemaWrapper.from_reference_guarded(schema_ref, context, level=level)
        return cls(name=name, required=required, schema=schema)


T = TypeVar("T", bound=Any)


def _remove_nones(seq: Iterable[Optional[T]]) -> List[T]:
    return [x for x in seq if x is not None]


class SchemaCrawler:
    """Creates flattened path: schema mappings of all properties within a schema"""

    def __init__(self) -> None:
        self.object_properties: Dict[Tuple[str, ...], SchemaWrapper] = {}
        self.list_properties: Dict[Tuple[str, ...], SchemaWrapper] = {}
        self.all_properties: Dict[Tuple[str, ...], SchemaWrapper] = {}

    def find_property_by_name(self, name: str, fallback: Optional[str] = None) -> Optional[DataPropertyPath]:
        """Find a property with the given name somewhere in the object tree.

        Prefers paths higher up in the object over deeply nested paths.

        Args:
            name: The name of the property to look for
            fallback: Optional fallback property to get when `name` is not found

        Returns:
            If property is found, `DataPropertyPath` object containing the corresponding schema and path tuple/json path
        """
        named = []
        fallbacks = []
        for path, prop in self.all_properties.items():
            if name in path:
                named.append((path, prop))
            if fallback and fallback in path:
                fallbacks.append((path, prop))
        named.sort(key=lambda item: len(item[0]))
        fallbacks.sort(key=lambda item: len(item[0]))
        if named:
            return DataPropertyPath(*named[0])
        elif fallbacks:
            return DataPropertyPath(*fallbacks[0])
        return None

    def crawl(self, schema: SchemaWrapper, path: Tuple[str, ...] = ()) -> None:
        if schema is None:
            breakpoint()
        self.all_properties[path] = schema
        if schema.is_object:
            self.object_properties[path] = schema
            for prop in schema.all_properties:
                prop_path = path + (prop.name,)
                self.all_properties[prop_path] = prop.schema
                if prop.is_list or prop.is_object:
                    self.crawl(prop.schema, prop_path)
        elif schema.is_list and schema.array_item is not None:
            array_item = schema.array_item
            self.list_properties[path] = array_item
            self.crawl(array_item, path + ("[*]",))
