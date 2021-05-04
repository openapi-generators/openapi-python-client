__all__ = [
    "MediaType",
    "OpenAPI",
    "Operation",
    "Parameter",
    "ParameterLocation",
    "PathItem",
    "Reference",
    "RequestBody",
    "Response",
    "Responses",
    "Schema",
]


import re
from typing import Callable, Iterator

from .openapi_schema_pydantic import MediaType
from .openapi_schema_pydantic import OpenAPI as _OpenAPI
from .openapi_schema_pydantic import Operation, Parameter, PathItem, Reference, RequestBody, Response, Responses, Schema
from .parameter_location import ParameterLocation

regex = re.compile(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)")


class SemVer:
    def __init__(self, str_value: str) -> None:
        self.str_value = str_value
        if not isinstance(str_value, str):
            raise TypeError("string required")
        m = regex.fullmatch(str_value)
        if not m:
            raise ValueError("invalid semantic versioning format")
        self.major = int(m.group(1))
        self.minor = int(m.group(2))
        self.patch = int(m.group(3))

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[str], "SemVer"]]:
        yield cls.validate

    @classmethod
    def validate(cls, v: str) -> "SemVer":
        return cls(v)

    def __str__(self) -> str:
        return self.str_value


class OpenAPI(_OpenAPI):
    openapi: SemVer
