from typing import Dict, Optional

from pydantic import AnyUrl, BaseModel, Extra


class OAuthFlow(BaseModel):
    """
    Configuration details for a supported OAuth Flow

    References:
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#oauthFlowObject
        - https://swagger.io/docs/specification/authentication/oauth2/
    """

    authorizationUrl: Optional[AnyUrl] = None
    tokenUrl: Optional[AnyUrl] = None
    refreshUrl: Optional[AnyUrl] = None
    scopes: Dict[str, str]

    class Config:  # pylint: disable=missing-class-docstring
        extra = Extra.allow
        schema_extra = {
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
        }
