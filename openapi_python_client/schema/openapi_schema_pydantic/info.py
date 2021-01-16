from typing import Optional

from pydantic import AnyUrl, BaseModel

from .contact import Contact
from .license import License


class Info(BaseModel):
    """
    The object provides metadata about the API.
    The metadata MAY be used by the clients if needed,
    and MAY be presented in editing or documentation generation tools for convenience.
    """

    title: str
    """
    **REQUIRED**. The title of the API.
    """

    description: Optional[str] = None
    """
    A short description of the API.
    [CommonMark syntax](https://spec.commonmark.org/) MAY be used for rich text representation.
    """

    termsOfService: Optional[AnyUrl] = None
    """
    A URL to the Terms of Service for the API.
    MUST be in the format of a URL.
    """

    contact: Optional[Contact] = None
    """
    The contact information for the exposed API.
    """

    license: Optional[License] = None
    """
    The license information for the exposed API.
    """

    version: str
    """
    **REQUIRED**. The version of the OpenAPI document
    (which is distinct from the [OpenAPI Specification version](#oasVersion) or the API implementation version).
    """

    class Config:
        schema_extra = {
            "examples": [
                {
                    "title": "Sample Pet Store App",
                    "description": "This is a sample server for a pet store.",
                    "termsOfService": "http://example.com/terms/",
                    "contact": {
                        "name": "API Support",
                        "url": "http://www.example.com/support",
                        "email": "support@example.com",
                    },
                    "license": {"name": "Apache 2.0", "url": "https://www.apache.org/licenses/LICENSE-2.0.html"},
                    "version": "1.0.1",
                }
            ]
        }
