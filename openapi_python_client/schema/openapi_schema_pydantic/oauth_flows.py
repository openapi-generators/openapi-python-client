from typing import Optional

from pydantic import BaseModel, Extra

from .oauth_flow import OAuthFlow


class OAuthFlows(BaseModel):
    """
    Allows configuration of the supported OAuth Flows.

    References:
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#oauthFlowsObject
        - https://swagger.io/docs/specification/authentication/oauth2/
    """

    implicit: Optional[OAuthFlow] = None
    password: Optional[OAuthFlow] = None
    clientCredentials: Optional[OAuthFlow] = None
    authorizationCode: Optional[OAuthFlow] = None

    class Config:  # pylint: disable=missing-class-docstring
        extra = Extra.allow
