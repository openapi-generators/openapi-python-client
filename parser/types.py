from __future__ import annotations

from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from parser.models import SchemaWrapper


TOpenApiType = Literal["boolean", "object", "array", "number", "string", "integer"]


class DataType:
    @property
    def type_hint(self) -> str:
        # TODO
        return "Any"

    @classmethod
    def from_schema(cls, schema: "SchemaWrapper") -> "DataType":
        return cls()
        pass

    # def _get_type_string_flat(self) -> str:
    #     py_types = []
    #     for oa_type in self.types:
    #         if oa_type == "boolean":
    #             py_types.append("bool")
    #         elif oa_type == "object":
    #             py_types.append("Dict[str, Any]")
    #         elif oa_type == "array":
    #             if self.array_item:
    #                 py_types.append("Sequence[{}]".format(self.array_item._get_type_string()))
    #             py_types.append("Sequence[Any]")
    #         elif oa_type == "string":
    #             py_types.append("str")
    #         elif oa_type == "number":
    #             py_types.append("float")
    #         elif oa_type == "integer":
    #             py_types.append("int")

    # def _get_type_string(self) -> str:
    #     if self.is_union:
    #         union_types = [m._get_type_string() for m in self.any_of + self.one_of]
    #         if len(union_types) == 1:
    #             return union_types[0]
    #         return "Union[{}]".format(", ".join(union_types))
    #     if self.type == "null":
    #         return "None"
    #     elif self.type == "boolean":
    #         return "bool"
    #     elif self.type == "object":
    #         return "Dict[str, Any]"
    #     elif self.type == "array":
    #         if self.array_item:
    #             return "Sequence[{}]".format(self.array_item._get_type_string())
    #         return "Sequence[Any]"
    #     elif self.type == "string":
    #         return "str"
    #     elif self.type == "number":
    #         return "float"
    #     elif self.type == "integer":
    #         return "int"
    #     raise ValueError(f"Uknown schema type '{self.type}'")
