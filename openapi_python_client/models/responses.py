from dataclasses import dataclass, field
from typing import Optional, List, Dict, Union, ClassVar, TypedDict, Literal, cast
import stringcase


ContentType = Union[Literal["application/json"], Literal["text/html"]]


@dataclass
class Response:
    """ Describes a single response for an endpoint """

    status_code: int
    content_type: ContentType


@dataclass
class ListRefResponse(Response):
    """ Response is a list of some ref schema """

    ref: str


@dataclass
class RefResponse(Response):
    """ Response is a single ref schema """

    ref: str


@dataclass
class StringResponse(Response):
    """ Response is a string """
    pass


@dataclass
class EmptyResponse(Response):
    """ Response has no payload """
    pass


_openapi_types_to_python_type_strings = {
    "string": "str",
    "number": "float",
    "integer": "int",
    "boolean": "bool",
    "object": "Dict",
}


class _ResponseListSchemaDict(TypedDict):
    title: str
    type: Literal["array"]
    items: Dict[Literal["$ref"], str]


_ResponseRefSchemaDict = Dict[Literal["$ref"], str]
_ResponseStringSchemaDict = Dict[Literal["type"], Literal["string"]]
_ResponseSchemaDict = Union[_ResponseListSchemaDict, _ResponseRefSchemaDict, _ResponseStringSchemaDict]


class _ResponseContentDict(TypedDict):
    schema: _ResponseSchemaDict


class _ResponseDict(TypedDict):
    description: str
    content: Dict[ContentType, _ResponseContentDict]


def response_from_dict(
    *, status_code: int, data: _ResponseDict
) -> Response:
    """ Generate a Response from the OpenAPI dictionary representation of it """
    if "content" not in data:
        raise ValueError(f"Cannot parse response data: {data}")

    content = data["content"]
    content_type: ContentType
    if "application/json" in content:
        content_type = "application/json"
    elif "text/html" in content:
        content_type = "text/html"
    else:
        raise ValueError(f"Cannot parse content type of {data}")

    schema_data: _ResponseSchemaDict = data["content"][content_type]["schema"]

    if "$ref" in schema_data:
        return RefResponse(
            status_code=status_code,
            content_type=content_type,
            ref=schema_data["$ref"].split("/")[-1],
        )
    if "type" not in schema_data:
        return EmptyResponse(
            status_code=status_code,
            content_type=content_type,
        )
    if schema_data["type"] == "array":
        list_data = cast(_ResponseListSchemaDict, schema_data)
        return ListRefResponse(
            status_code=status_code,
            content_type=content_type,
            ref=list_data["items"]["$ref"].split("/")[-1],
        )
    if schema_data["type"] == "string":
        return StringResponse(
            status_code=status_code,
            content_type=content_type,
        )
