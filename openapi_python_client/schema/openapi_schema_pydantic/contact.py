from typing import Optional

from pydantic import AnyUrl, BaseModel, Extra


class Contact(BaseModel):
    """
    Contact information for the exposed API.

    See Also:
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#contactObject
    """

    name: Optional[str] = None
    url: Optional[AnyUrl] = None
    email: Optional[str] = None

    class Config:  # pylint: disable=missing-class-docstring
        extra = Extra.allow
        schema_extra = {
            "examples": [
                {"name": "API Support", "url": "http://www.example.com/support", "email": "support@example.com"}
            ]
        }
