from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, Extra, Field

from ..parameter_location import ParameterLocation
from .example import Example
from .media_type import MediaType
from .reference import Reference
from .schema import Schema


class Parameter(BaseModel):
    """
    Describes a single operation parameter.

    A unique parameter is defined by a combination of a [name](#parameterName) and [location](#parameterIn).

    References:
        - https://swagger.io/docs/specification/describing-parameters/
        - https://swagger.io/docs/specification/serialization/
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#parameterObject
    """

    name: str
    param_in: ParameterLocation = Field(alias="in")
    description: Optional[str] = None
    required: bool = False
    deprecated: bool = False
    allowEmptyValue: bool = False
    style: Optional[str] = None
    explode: bool = False
    allowReserved: bool = False
    param_schema: Optional[Union[Reference, Schema]] = Field(default=None, alias="schema")
    example: Optional[Any] = None
    examples: Optional[Dict[str, Union[Example, Reference]]] = None
    content: Optional[Dict[str, MediaType]] = None

    class Config:  # pylint: disable=missing-class-docstring
        extra = Extra.allow
        allow_population_by_field_name = True
        schema_extra = {
            "examples": [
                {
                    "name": "token",
                    "in": "header",
                    "description": "token to be passed as a header",
                    "required": True,
                    "schema": {"type": "array", "items": {"type": "integer", "format": "int64"}},
                    "style": "simple",
                },
                {
                    "name": "username",
                    "in": "path",
                    "description": "username to fetch",
                    "required": True,
                    "schema": {"type": "string"},
                },
                {
                    "name": "id",
                    "in": "query",
                    "description": "ID of the object to fetch",
                    "required": False,
                    "schema": {"type": "array", "items": {"type": "string"}},
                    "style": "form",
                    "explode": True,
                },
                {
                    "in": "query",
                    "name": "freeForm",
                    "schema": {"type": "object", "additionalProperties": {"type": "integer"}},
                    "style": "form",
                },
                {
                    "in": "query",
                    "name": "coordinates",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["lat", "long"],
                                "properties": {"lat": {"type": "number"}, "long": {"type": "number"}},
                            }
                        }
                    },
                },
            ]
        }
