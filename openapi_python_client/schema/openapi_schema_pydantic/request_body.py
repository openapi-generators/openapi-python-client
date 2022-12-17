from typing import Dict, Optional

from pydantic import BaseModel, Extra

from .media_type import MediaType


class RequestBody(BaseModel):
    """Describes a single request body.

    References:
        - https://swagger.io/docs/specification/describing-request-body/
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#requestBodyObject
    """

    description: Optional[str] = None
    content: Dict[str, MediaType]
    required: bool = False

    class Config:  # pylint: disable=missing-class-docstring
        extra = Extra.allow
        schema_extra = {
            "examples": [
                {
                    "description": "user to add to the system",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/User"},
                            "examples": {
                                "user": {
                                    "summary": "User Example",
                                    "externalValue": "http://foo.bar/examples/user-example.json",
                                }
                            },
                        },
                        "application/xml": {
                            "schema": {"$ref": "#/components/schemas/User"},
                            "examples": {
                                "user": {
                                    "summary": "User example in XML",
                                    "externalValue": "http://foo.bar/examples/user-example.xml",
                                }
                            },
                        },
                        "text/plain": {
                            "examples": {
                                "user": {
                                    "summary": "User example in Plain text",
                                    "externalValue": "http://foo.bar/examples/user-example.txt",
                                }
                            }
                        },
                        "*/*": {
                            "examples": {
                                "user": {
                                    "summary": "User example in other format",
                                    "externalValue": "http://foo.bar/examples/user-example.whatever",
                                }
                            }
                        },
                    },
                },
                {
                    "description": "user to add to the system",
                    "content": {"text/plain": {"schema": {"type": "array", "items": {"type": "string"}}}},
                },
            ]
        }
