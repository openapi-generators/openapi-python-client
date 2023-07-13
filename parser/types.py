from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from parser.models import SchemaWrapper


TOpenApiType = Literal["boolean", "object", "array", "number", "string", "integer"]

OATypeToPyType = {"boolean": "bool", "number": "float", "string": "str", "integer": "int"}


def schema_to_type_hint(schema: SchemaWrapper) -> str:
    types = schema.types
    tpl = "Optional[{}]" if schema.nullable else "{}"
    union_types: Dict[str, None] = {}  # Using a dict as a faux ordered set (for deterministic client code)
    for s_type in types:
        py_type = OATypeToPyType.get(s_type)
        if py_type:
            union_types[py_type] = None
            continue
        elif s_type == "object":
            union_types["Dict[str, Any]"] = None
        elif s_type == "array":
            item_type = schema_to_type_hint(schema.array_item)
            py_type = f"List[{item_type}]"
            union_types[py_type] = None
    for one_of in schema.one_of + schema.any_of:
        union_types[schema_to_type_hint(one_of)] = None

    final_type = ""
    if len(union_types) == 1:
        final_type = next(iter(union_types))
    elif len(union_types) == 0:
        final_type = "Any"
    else:
        final_type = ", ".join(union_types)
    return tpl.format(final_type)


@dataclass
class DataType:
    type_hint: str

    @classmethod
    def from_schema(cls, schema: "SchemaWrapper") -> "DataType":
        return cls(type_hint=schema_to_type_hint(schema))
