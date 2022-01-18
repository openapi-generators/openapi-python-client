from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Extra, Field, StrictInt, StrictStr

from ..data_type import DataType
from .discriminator import Discriminator
from .external_documentation import ExternalDocumentation
from .reference import Reference
from .xml import XML


class Schema(BaseModel):
    """
    The Schema Object allows the definition of input and output data types.
    These types can be objects, but also primitives and arrays.
    This object is an extended subset of the [JSON Schema Specification Wright Draft 00](https://json-schema.org/).

    References:
        - https://swagger.io/docs/specification/data-models/
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#schemaObject
    """

    title: Optional[str] = None
    multipleOf: Optional[float] = Field(default=None, gt=0.0)
    maximum: Optional[float] = None
    exclusiveMaximum: Optional[bool] = None
    minimum: Optional[float] = None
    exclusiveMinimum: Optional[bool] = None
    maxLength: Optional[int] = Field(default=None, ge=0)
    minLength: Optional[int] = Field(default=None, ge=0)
    pattern: Optional[str] = None
    maxItems: Optional[int] = Field(default=None, ge=0)
    minItems: Optional[int] = Field(default=None, ge=0)
    uniqueItems: Optional[bool] = None
    maxProperties: Optional[int] = Field(default=None, ge=0)
    minProperties: Optional[int] = Field(default=None, ge=0)
    required: Optional[List[str]] = Field(default=None, min_items=1)
    enum: Union[None, List[Optional[StrictInt]], List[Optional[StrictStr]]] = Field(default=None, min_items=1)
    type: Optional[DataType] = Field(default=None)
    allOf: List[Union[Reference, "Schema"]] = Field(default_factory=list)
    oneOf: List[Union[Reference, "Schema"]] = Field(default_factory=list)
    anyOf: List[Union[Reference, "Schema"]] = Field(default_factory=list)
    schema_not: Optional[Union[Reference, "Schema"]] = Field(default=None, alias="not")
    items: Optional[Union[Reference, "Schema"]] = None
    properties: Optional[Dict[str, Union[Reference, "Schema"]]] = None
    additionalProperties: Optional[Union[bool, Reference, "Schema"]] = None
    description: Optional[str] = None
    schema_format: Optional[str] = Field(default=None, alias="format")
    default: Optional[Any] = None
    nullable: bool = False
    discriminator: Optional[Discriminator] = None
    readOnly: Optional[bool] = None
    writeOnly: Optional[bool] = None
    xml: Optional[XML] = None
    externalDocs: Optional[ExternalDocumentation] = None
    example: Optional[Any] = None
    deprecated: Optional[bool] = None

    class Config:  # pylint: disable=missing-class-docstring
        extra = Extra.allow
        allow_population_by_field_name = True
        schema_extra = {
            "examples": [
                {"type": "string", "format": "email"},
                {
                    "type": "object",
                    "required": ["name"],
                    "properties": {
                        "name": {"type": "string"},
                        "address": {"$ref": "#/components/schemas/Address"},
                        "age": {"type": "integer", "format": "int32", "minimum": 0},
                    },
                },
                {"type": "object", "additionalProperties": {"type": "string"}},
                {"type": "object", "additionalProperties": {"$ref": "#/components/schemas/ComplexModel"}},
                {
                    "type": "object",
                    "properties": {"id": {"type": "integer", "format": "int64"}, "name": {"type": "string"}},
                    "required": ["name"],
                    "example": {"name": "Puma", "id": 1},
                },
                {
                    "type": "object",
                    "required": ["message", "code"],
                    "properties": {
                        "message": {"type": "string"},
                        "code": {"type": "integer", "minimum": 100, "maximum": 600},
                    },
                },
                {
                    "allOf": [
                        {"$ref": "#/components/schemas/ErrorModel"},
                        {"type": "object", "required": ["rootCause"], "properties": {"rootCause": {"type": "string"}}},
                    ]
                },
                {
                    "type": "object",
                    "discriminator": {"propertyName": "petType"},
                    "properties": {"name": {"type": "string"}, "petType": {"type": "string"}},
                    "required": ["name", "petType"],
                },
                {
                    "description": "A representation of a cat. "
                    "Note that `Cat` will be used as the discriminator value.",
                    "allOf": [
                        {"$ref": "#/components/schemas/Pet"},
                        {
                            "type": "object",
                            "properties": {
                                "huntingSkill": {
                                    "type": "string",
                                    "description": "The measured skill for hunting",
                                    "default": "lazy",
                                    "enum": ["clueless", "lazy", "adventurous", "aggressive"],
                                }
                            },
                            "required": ["huntingSkill"],
                        },
                    ],
                },
                {
                    "description": "A representation of a dog. "
                    "Note that `Dog` will be used as the discriminator value.",
                    "allOf": [
                        {"$ref": "#/components/schemas/Pet"},
                        {
                            "type": "object",
                            "properties": {
                                "packSize": {
                                    "type": "integer",
                                    "format": "int32",
                                    "description": "the size of the pack the dog is from",
                                    "default": 0,
                                    "minimum": 0,
                                }
                            },
                            "required": ["packSize"],
                        },
                    ],
                },
            ]
        }


Schema.update_forward_refs()
