from typing import Optional

from pydantic import AnyUrl, BaseModel, Extra


class License(BaseModel):
    """
    License information for the exposed API.

    References:
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#licenseObject
    """

    name: str
    url: Optional[AnyUrl] = None

    class Config:  # pylint: disable=missing-class-docstring
        extra = Extra.allow
        schema_extra = {"examples": [{"name": "Apache 2.0", "url": "https://www.apache.org/licenses/LICENSE-2.0.html"}]}
