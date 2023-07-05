from typing import Literal, TYPE_CHECKING, Optional, Union, List, TypeVar, Any, Iterable

from dataclasses import dataclass, field

import openapi_schema_pydantic as osp

if TYPE_CHECKING:
    from parser.context import OpenapiContext


TSchemaType = Literal["null", "boolean", "object", "array", "number", "string", "integer"]


@dataclass
class Schema:
    schema: osp.Schema
    name: str
    type: TSchemaType


@dataclass
class Response:
    schema: osp.Response
    root_object: Schema | None
    status_code: str
    description: str


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

    all_of: List["SchemaWrapper"] = field(default_factory=list)
    any_of: List["SchemaWrapper"] = field(default_factory=list)
    one_of: List["SchemaWrapper"] = field(default_factory=list)

    @classmethod
    def from_reference_guarded(
        cls, schema_ref: Union[osp.Schema, osp.Reference], context: "OpenapiContext", level: int = 0
    ) -> Optional["SchemaWrapper"]:
        if level > 3:
            return None
        level += 1
        return cls.from_reference(schema_ref, context, level=level)

    @classmethod
    def from_reference(
        cls, schema_ref: Union[osp.Schema, osp.Reference], context: "OpenapiContext", level: int = 0
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

        one_of = _remove_nones([cls.from_reference_guarded(ref, context, level=level) for ref in schema.oneOf or []])

        any_of = _remove_nones([cls.from_reference_guarded(ref, context, level=level) for ref in schema.anyOf or []])

        properties = _remove_nones(
            [
                Property.from_reference_guarded(name, ref, context, level=level)
                for name, ref in (schema.properties or {}).items()
            ]
        )

        description = schema_ref.description or schema.description

        return cls(
            schema=schema,
            name=name,
            description=description,
            ref=schema_ref if isinstance(schema_ref, osp.Reference) else None,
            properties=properties,
            all_of=all_of,
            one_of=one_of,
            any_of=any_of,
        )


@dataclass
class Property:
    name: str
    schema: SchemaWrapper

    @classmethod
    def from_reference_guarded(
        cls, name: str, schema_ref: Union[osp.Schema, osp.Reference], context: "OpenapiContext", level: int = 0
    ) -> "Property":
        if level >= 3:
            return None
        schema = SchemaWrapper.from_reference_guarded(schema_ref, context, level=level)
        return cls(name=name, schema=schema)


T = TypeVar("T", bound=Any)


def _remove_nones(seq: Iterable[Optional[T]]) -> List[T]:
    return [x for x in seq if seq is not None]
