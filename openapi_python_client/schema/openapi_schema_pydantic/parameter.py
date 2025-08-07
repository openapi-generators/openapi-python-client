from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ..parameter_location import ParameterLocation
from ..style import Style
from .example import Example
from .media_type import MediaType
from .reference import ReferenceOr
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
    style: Optional[Style] = None
    explode: Optional[bool] = None
    allowReserved: bool = False
    param_schema: Optional[ReferenceOr[Schema]] = Field(default=None, alias="schema")
    example: Optional[Any] = None
    examples: Optional[dict[str, ReferenceOr[Example]]] = None
    content: Optional[dict[str, MediaType]] = None

    @model_validator(mode='after')
    @classmethod
    def validate_dependencies(cls, model: "Parameter") -> "Parameter":
        param_in = model.param_in
        explode = model.explode

        if model.style is None:
            if param_in in [ParameterLocation.PATH, ParameterLocation.HEADER]:
                model.style = Style.SIMPLE
            elif param_in in [ParameterLocation.QUERY, ParameterLocation.COOKIE]:
                model.style = Style.FORM


        # Validate style based on parameter location, not all combinations are valid.
        # https://swagger.io/docs/specification/v3_0/serialization/
        if param_in == ParameterLocation.PATH:
            if model.style not in (Style.SIMPLE, Style.LABEL, Style.MATRIX):
                raise ValueError(f"Invalid style '{model.style}' for path parameter")
        elif param_in == ParameterLocation.QUERY:
            if model.style not in (Style.FORM, Style.SPACE_DELIMITED, Style.PIPE_DELIMITED, Style.DEEP_OBJECT):
                raise ValueError(f"Invalid style '{model.style}' for query parameter")
        elif param_in == ParameterLocation.HEADER:
            if model.style != Style.SIMPLE:
                raise ValueError(f"Invalid style '{model.style}' for header parameter")
        elif param_in == ParameterLocation.COOKIE:
            if model.style != Style.FORM:
                raise ValueError(f"Invalid style '{model.style}' for cookie parameter")


        if explode is None:
            if model.style == Style.FORM:
                model.explode = True
            else:
                model.explode = False

        return model



    model_config = ConfigDict(
        # `MediaType` is not build yet, will rebuild in `__init__.py`:
        defer_build=True,
        extra="allow",
        populate_by_name=True,
        json_schema_extra={
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
        },
    )
