from typing import Dict, Optional

from pydantic import BaseModel

from .reference import Reference


class Encoding(BaseModel):
    """A single encoding definition applied to a single schema property.

    References:
        - https://swagger.io/docs/specification/describing-request-body/
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#encodingObject
    """

    contentType: Optional[str] = None
    headers: Optional[Dict[str, Reference]] = None
    style: Optional[str] = None
    explode: bool = False
    allowReserved: bool = False

    class Config:  # pylint: disable=missing-class-docstring
        schema_extra = {
            "examples": [
                {
                    "contentType": "image/png, image/jpeg",
                    "headers": {
                        "X-Rate-Limit-Limit": {
                            "description": "The number of allowed requests in the current period",
                            "schema": {"type": "integer"},
                        }
                    },
                }
            ]
        }
