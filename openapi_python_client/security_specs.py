from typing import Literal, TypedDict, Dict
from base64 import b64encode

from dlt.common.configuration.specs.base_configuration import BaseConfiguration, configspec


class CredentialsHttpParams(TypedDict):
    cookies: Dict[str, str]
    params: Dict[str, str]
    headers: Dict[str, str]


@configspec
class ApiKeyCredentialsBase(BaseConfiguration):
    type: Literal["apiKey"] = "apiKey"
    location: Literal["header", "cookie", "param"]  # Alias for scheme "in" field
    name: str
    api_key: str

    def to_http_params(self) -> CredentialsHttpParams:
        result: CredentialsHttpParams = dict(cookies={}, headers={}, params={})
        result[self.location + "s"][self.name] = self.api_key  # type: ignore
        return result


@configspec
class HttpBasicCredentialsBase(BaseConfiguration):
    type: Literal["http"] = "http"
    scheme: Literal["basic"] = "basic"
    username: str
    password: str

    def to_http_params(self) -> CredentialsHttpParams:
        encoded = b64encode(f"{self.username}:{self.password}".encode()).decode()
        return dict(cookies={}, headers={"Authorization": "Basic " + encoded}, params={})


@configspec
class HttpBearerCredentialsBase(BaseConfiguration):
    type: Literal["http"] = "http"
    scheme: Literal["bearer"] = "bearer"
    token: str

    def to_http_params(self) -> CredentialsHttpParams:
        return dict(cookies={}, headers={"Authorization": "Bearer " + self.token}, params={})


@configspec
class OAuth2CredentialsBase(BaseConfiguration):
    # TODO: Separate class for flows (implcit, authorization_code, client_credentials, etc)
    type: Literal["oauth2"] = "oauth2"
    access_token: str

    def to_http_params(self) -> CredentialsHttpParams:
        return dict(cookies={}, headers={"Authorization": "Bearer " + self.access_token}, params={})
