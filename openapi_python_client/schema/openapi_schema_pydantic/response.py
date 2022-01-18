from typing import Dict, Optional, Union

from pydantic import BaseModel, Extra

from .header import Header
from .link import Link
from .media_type import MediaType
from .reference import Reference


class Response(BaseModel):
    """
    Describes a single response from an API Operation, including design-time,
    static `links` to operations based on the response.

    References:
        - https://swagger.io/docs/specification/describing-responses/
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#responseObject
    """

    description: str
    headers: Optional[Dict[str, Union[Header, Reference]]] = None
    content: Optional[Dict[str, MediaType]] = None
    links: Optional[Dict[str, Union[Link, Reference]]] = None

    class Config:  # pylint: disable=missing-class-docstring
        extra = Extra.allow
        schema_extra = {
            "examples": [
                {
                    "description": "A complex object array response",
                    "content": {
                        "application/json": {
                            "schema": {"type": "array", "items": {"$ref": "#/components/schemas/VeryComplexType"}}
                        }
                    },
                },
                {"description": "A simple string response", "content": {"text/plain": {"schema": {"type": "string"}}}},
                {
                    "description": "A simple string response",
                    "content": {"text/plain": {"schema": {"type": "string", "example": "whoa!"}}},
                    "headers": {
                        "X-Rate-Limit-Limit": {
                            "description": "The number of allowed requests in the current period",
                            "schema": {"type": "integer"},
                        },
                        "X-Rate-Limit-Remaining": {
                            "description": "The number of remaining requests in the current period",
                            "schema": {"type": "integer"},
                        },
                        "X-Rate-Limit-Reset": {
                            "description": "The number of seconds left in the current period",
                            "schema": {"type": "integer"},
                        },
                    },
                },
                {"description": "object created"},
            ]
        }
