from typing import Dict, Optional

from pydantic import AnyUrl, BaseModel


class OAuthFlow(BaseModel):
    """
    Configuration details for a supported OAuth Flow
    """

    authorizationUrl: Optional[AnyUrl] = None
    """
    **REQUIRED** for `oauth2 ("implicit", "authorizationCode")`.
    The authorization URL to be used for this flow.
    This MUST be in the form of a URL.
    """

    tokenUrl: Optional[str] = None
    """
    **REQUIRED** for `oauth2 ("password", "clientCredentials", "authorizationCode")`.
    The token URL to be used for this flow.
    This MUST be in the form of a URL.
    """

    refreshUrl: Optional[AnyUrl] = None
    """
    The URL to be used for obtaining refresh tokens. This MUST be in the form of a URL.
    """

    scopes: Dict[str, str]
    """
    **REQUIRED**. The available scopes for the OAuth2 security scheme.
    A map between the scope name and a short description for it.
    The map MAY be empty.
    """

    class Config:
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
