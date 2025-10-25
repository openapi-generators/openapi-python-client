from pydantic import BaseModel, ConfigDict

from .oauth_flow import OAuthFlow


class OAuthFlows(BaseModel):
    """
    Allows configuration of the supported OAuth Flows.

    References:
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#oauthFlowsObject
        - https://swagger.io/docs/specification/authentication/oauth2/
    """

    implicit: OAuthFlow | None = None
    password: OAuthFlow | None = None
    clientCredentials: OAuthFlow | None = None
    authorizationCode: OAuthFlow | None = None
    model_config = ConfigDict(extra="allow")
