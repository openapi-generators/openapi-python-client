from dataclasses import InitVar, dataclass, field
from typing import Any, Dict

from .errors import ParseError
from .reference import Reference


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
        return f"[{self.reference.class_name}.from_dict(item) for item in cast(List[Dict[str, Any]], response.json())]"


@dataclass
class RefResponse(Response):
    """ Response is a single ref schema """

    reference: Reference

    def return_string(self) -> str:
        """ How this Response should be represented as a return type """
        return self.reference.class_name

    def constructor(self) -> str:
        """ How the return value of this response should be constructed """
        return f"{self.reference.class_name}.from_dict(cast(Dict[str, Any], response.json()))"


@dataclass
class BasicResponse(Response):
    """ Response is a basic type """

    openapi_type: InitVar[str]
    python_type: str = field(init=False)

    def __post_init__(self, openapi_type: str) -> None:
        self.python_type = openapi_types_to_python_type_strings[openapi_type]

    def return_string(self) -> str:
        """ How this Response should be represented as a return type """
        return self.python_type

    def constructor(self) -> str:
        """ How the return value of this response should be constructed """
        return f"{self.python_type}(response.text)"


openapi_types_to_python_type_strings = {
    "string": "str",
    "number": "float",
    "integer": "int",
    "boolean": "bool",
}


def response_from_dict(*, status_code: int, data: Dict[str, Any]) -> Response:
    """ Generate a Response from the OpenAPI dictionary representation of it """
    if "content" not in data:
        return Response(status_code=status_code)

    content = data["content"]
    if "application/json" in content:
        content_type = "application/json"
    elif "text/html" in content:
        content_type = "text/html"
    else:
        raise ParseError(data, message=f"Unsupported content_type {content}")

    schema_data = data["content"][content_type]["schema"]

    if "$ref" in schema_data:
        return RefResponse(status_code=status_code, reference=Reference.from_ref(schema_data["$ref"]),)
    response_type = schema_data.get("type")
    if response_type is None:
        return Response(status_code=status_code)
    if response_type == "array":
        return ListRefResponse(status_code=status_code, reference=Reference.from_ref(schema_data["items"]["$ref"]),)
    if response_type in openapi_types_to_python_type_strings:
        return BasicResponse(status_code=status_code, openapi_type=response_type)
    raise ParseError(data, message=f"Unrecognized type {schema_data['type']}")
