from dataclasses import InitVar, dataclass, field
from typing import Union

import openapi_schema_pydantic as oai

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


def response_from_data(*, status_code: int, data: Union[oai.Response, oai.Reference]) -> Response:
    """ Generate a Response from the OpenAPI dictionary representation of it """

    if isinstance(data, oai.Reference) or data.content is None:
        return Response(status_code=status_code)

    content = data.content
    schema_data = None
    if "application/json" in content:
        schema_data = data.content["application/json"].media_type_schema
    elif "text/html" in content:
        schema_data = data.content["text/html"].media_type_schema

    if schema_data is None:
        raise ParseError(data, message=f"Unsupported content_type {content}")

    if isinstance(schema_data, oai.Reference):
        return RefResponse(status_code=status_code, reference=Reference.from_ref(schema_data.ref),)
    response_type = schema_data.type
    if response_type is None:
        return Response(status_code=status_code)
    if response_type == "array" and isinstance(schema_data.items, oai.Reference):
        return ListRefResponse(status_code=status_code, reference=Reference.from_ref(schema_data.items.ref),)
    if response_type in openapi_types_to_python_type_strings:
        return BasicResponse(status_code=status_code, openapi_type=response_type)
    raise ParseError(data, message=f"Unrecognized type {schema_data.type}")
