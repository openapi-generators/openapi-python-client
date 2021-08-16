from typing import Optional

from pydantic import AnyUrl, BaseModel


class ExternalDocumentation(BaseModel):
    """Allows referencing an external resource for extended documentation.

    References:
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#externalDocumentationObject
    """

    description: Optional[str] = None
    url: AnyUrl

    class Config:  # pylint: disable=missing-class-docstring
        schema_extra = {"examples": [{"description": "Find more info here", "url": "https://example.com"}]}
