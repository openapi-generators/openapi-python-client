from dataclasses import dataclass
from typing import Any, Dict, Literal, TypedDict, Union

from .reference import Reference

ContentType = Union[Literal["application/json"], Literal["text/html"]]


@dataclass
class Response:
    """ Describes a single response for an endpoint """

    status_code: int

    def return_string(self) -> str:
        """ How this Response should be represented as a return type """
        return "None"

    def constructor(self) -> str:
        """ How the return value of this response should be constructed """
        return "None"


@dataclass
class ListRefResponse(Response):
    """ Response is a list of some ref schema """

    reference: Reference

    def return_string(self) -> str:
        """ How this Response should be represented as a return type """
        return f"List[{self.reference.class_name}]"

    def constructor(self) -> str:
        """ How the return value of this response should be constructed """
        return f"[{self.reference.class_name}.from_dict(item) for item in response.json()]"


@dataclass
class RefResponse(Response):
    """ Response is a single ref schema """

    reference: Reference

    def return_string(self) -> str:
        """ How this Response should be represented as a return type """
        return self.reference.class_name

    def constructor(self) -> str:
        """ How the return value of this response should be constructed """
        return f"{self.reference.class_name}.from_dict(response.json())"


@dataclass
class StringResponse(Response):
    """ Response is a string """

    def return_string(self) -> str:
        """ How this Response should be represented as a return type """
        return "str"

    def constructor(self) -> str:
        """ How the return value of this response should be constructed """
        return "response.text"


_openapi_types_to_python_type_strings = {
    "string": "str",
    "number": "float",
    "integer": "int",
    "boolean": "bool",
    "object": "Dict",
}


class _ResponseDict(TypedDict):
    description: str
    content: Dict[ContentType, Any]


def response_from_dict(*, status_code: int, data: _ResponseDict) -> Response:
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

    schema_data = data["content"][content_type]["schema"]

    if "$ref" in schema_data:
        return RefResponse(status_code=status_code, reference=Reference.from_ref(schema_data["$ref"]),)
    if "type" not in schema_data:
        return Response(status_code=status_code)
    if schema_data["type"] == "array":
        return ListRefResponse(status_code=status_code, reference=Reference.from_ref(schema_data["items"]["$ref"]),)
    if schema_data["type"] == "string":
        return StringResponse(status_code=status_code)
    raise ValueError(f"Cannot parse response of type {schema_data['type']}")
