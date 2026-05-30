from typing import Any

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictInt, StrictStr, model_validator

from ..data_type import DataType
from .discriminator import Discriminator
from .external_documentation import ExternalDocumentation
from .reference import ReferenceOr
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

    title: str | None = None
    multipleOf: float | None = Field(default=None, gt=0.0)
    maximum: float | None = None
    exclusiveMaximum: bool | float | None = None
    minimum: float | None = None
    exclusiveMinimum: bool | float | None = None
    maxLength: int | None = Field(default=None, ge=0)
    minLength: int | None = Field(default=None, ge=0)
    pattern: str | None = None
    maxItems: int | None = Field(default=None, ge=0)
    minItems: int | None = Field(default=None, ge=0)
    uniqueItems: bool | None = None
    maxProperties: int | None = Field(default=None, ge=0)
    minProperties: int | None = Field(default=None, ge=0)
    required: list[str] | None = Field(default=None)
    enum: None | list[Any] = Field(default=None, min_length=1)
    const: None | StrictStr | StrictInt | StrictFloat | StrictBool = None
    type: DataType | list[DataType] | None = Field(default=None)
    allOf: list[ReferenceOr["Schema"]] = Field(default_factory=list)
    oneOf: list[ReferenceOr["Schema"]] = Field(default_factory=list)
    anyOf: list[ReferenceOr["Schema"]] = Field(default_factory=list)
    schema_not: ReferenceOr["Schema"] | None = Field(default=None, alias="not")
    items: ReferenceOr["Schema"] | None = None
    prefixItems: list[ReferenceOr["Schema"]] = Field(default_factory=list)
    properties: dict[str, ReferenceOr["Schema"]] | None = None
    additionalProperties: bool | ReferenceOr["Schema"] | None = None
    description: str | None = None
    schema_format: str | None = Field(default=None, alias="format")
    default: Any | None = None
    nullable: bool = Field(default=False)
    discriminator: Discriminator | None = None
    readOnly: bool | None = None
    writeOnly: bool | None = None
    xml: XML | None = None
    externalDocs: ExternalDocumentation | None = None
    example: Any | None = None
    deprecated: bool | None = None
    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
        json_schema_extra={
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
                {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/components/schemas/ComplexModel"},
                },
                {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "format": "int64"},
                        "name": {"type": "string"},
                    },
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
                        {
                            "type": "object",
                            "required": ["rootCause"],
                            "properties": {"rootCause": {"type": "string"}},
                        },
                    ]
                },
                {
                    "type": "object",
                    "discriminator": {"propertyName": "petType"},
                    "properties": {
                        "name": {"type": "string"},
                        "petType": {"type": "string"},
                    },
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
                                    "enum": [
                                        "clueless",
                                        "lazy",
                                        "adventurous",
                                        "aggressive",
                                    ],
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
        },
    )

    @model_validator(mode="after")
    def handle_exclusive_min_max(self) -> "Schema":
        """
        Convert exclusiveMinimum/exclusiveMaximum between OpenAPI v3.0 (bool) and v3.1 (numeric).
        """
        # Handle exclusiveMinimum
        if isinstance(self.exclusiveMinimum, bool) and self.minimum is not None:
            if self.exclusiveMinimum:
                self.exclusiveMinimum = self.minimum
                self.minimum = None
            else:
                self.exclusiveMinimum = None
        elif isinstance(self.exclusiveMinimum, float):
            self.minimum = None

        # Handle exclusiveMaximum
        if isinstance(self.exclusiveMaximum, bool) and self.maximum is not None:
            if self.exclusiveMaximum:
                self.exclusiveMaximum = self.maximum
                self.maximum = None
            else:
                self.exclusiveMaximum = None
        elif isinstance(self.exclusiveMaximum, float):
            self.maximum = None

        return self

    @model_validator(mode="after")
    def handle_nullable(self) -> "Schema":
        """Convert the old 3.0 `nullable` property into the new 3.1 style"""
        if not self.nullable:
            return self
        if isinstance(self.type, str):
            self.type = [self.type, DataType.NULL]
        elif isinstance(self.type, list):
            if DataType.NULL not in self.type:
                self.type.append(DataType.NULL)
        elif len(self.oneOf) > 0:
            self.oneOf.append(Schema(type=DataType.NULL))
        elif len(self.anyOf) > 0:
            self.anyOf.append(Schema(type=DataType.NULL))
        elif len(self.allOf) > 0:  # Nullable allOf is basically oneOf[null, allOf]
            self.oneOf = [Schema(type=DataType.NULL), Schema(allOf=self.allOf)]
            self.allOf = []
        return self
