from typing import TYPE_CHECKING, Dict, Optional, Union

from pydantic import BaseModel, Extra

from .reference import Reference

if TYPE_CHECKING:  # pragma: no cover
    from .header import Header
else:
    Header = "Header"  # pylint: disable=invalid-name


class Encoding(BaseModel):
    """A single encoding definition applied to a single schema property.

    References:
        - https://swagger.io/docs/specification/describing-request-body/
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#encodingObject
    """

    contentType: Optional[str] = None
    headers: Optional[Dict[str, Union[Header, Reference]]] = None
    style: Optional[str] = None
    explode: bool = False
    allowReserved: bool = False

    class Config:  # pylint: disable=missing-class-docstring
        extra = Extra.allow
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
