from pydantic import BaseModel, ConfigDict

from openapi_python_client.schema.untrusted_string import UntrustedString


class Contact(BaseModel):
    """
    Contact information for the exposed API.

    See Also:
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#contactObject
    """

    name: UntrustedString | None = None
    url: UntrustedString | None = None
    email: UntrustedString | None = None
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "examples": [
                {"name": "API Support", "url": "http://www.example.com/support", "email": "support@example.com"}
            ]
        },
    )
