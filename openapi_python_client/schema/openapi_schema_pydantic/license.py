from pydantic import BaseModel, ConfigDict

from ..untrusted_string import UntrustedString


class License(BaseModel):
    """
    License information for the exposed API.

    References:
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#licenseObject
    """

    name: UntrustedString
    url: UntrustedString | None = None
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "examples": [{"name": "Apache 2.0", "url": "https://www.apache.org/licenses/LICENSE-2.0.html"}]
        },
    )
