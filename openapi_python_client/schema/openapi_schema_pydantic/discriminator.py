from pydantic import BaseModel, ConfigDict

from ..untrusted_string import UntrustedString


class Discriminator(BaseModel):
    """
    When request bodies or response payloads may be one of a number of different schemas,
    a `discriminator` object can be used to aid in serialization, deserialization, and validation.

    The discriminator is a specific object in a schema which is used to inform the consumer of the specification
    of an alternative schema based on the value associated with it.

    When using the discriminator, _inline_ schemas will not be considered.

    References:
        - https://swagger.io/docs/specification/data-models/inheritance-and-polymorphism/
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#discriminatorObject
    """

    propertyName: UntrustedString
    mapping: dict[UntrustedString, UntrustedString] | None = None
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "examples": [
                {
                    "propertyName": "petType",
                    "mapping": {
                        "dog": "#/components/schemas/Dog",
                        "monster": "https://gigantic-server.com/schemas/Monster/schema.json",
                    },
                }
            ]
        },
    )
