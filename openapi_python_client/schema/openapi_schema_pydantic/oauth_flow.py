from pydantic import BaseModel, ConfigDict

from ..untrusted_string import UntrustedString


class OAuthFlow(BaseModel):
    """
    Configuration details for a supported OAuth Flow

    References:
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#oauthFlowObject
        - https://swagger.io/docs/specification/authentication/oauth2/
    """

    authorizationUrl: UntrustedString | None = None
    tokenUrl: UntrustedString | None = None
    refreshUrl: UntrustedString | None = None
    scopes: dict[UntrustedString, UntrustedString]
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "examples": [
                {
                    "authorizationUrl": "https://example.com/api/oauth/dialog",
                    "scopes": {"write:pets": "modify pets in your account", "read:pets": "read your pets"},
                },
                {
                    "authorizationUrl": "https://example.com/api/oauth/dialog",
                    "tokenUrl": "https://example.com/api/oauth/token",
                    "scopes": {"write:pets": "modify pets in your account", "read:pets": "read your pets"},
                },
            ]
        },
    )
