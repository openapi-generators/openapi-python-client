"""Models for API authenticators."""

from __future__ import annotations

import base64
import math
import typing as t
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit

import jwt
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from pydantic import BaseModel, root_validator, validator

from dlt.common import logger, pendulum, timedelta


class APIAuthenticator(BaseModel):
    """Base class for API authenticators."""

    auth_headers: t.Dict[str, str] = {}
    auth_params: t.Dict[str, str] = {}

    @staticmethod
    def add_parameters(initial_url: str, extra_parameters: dict) -> str:
        """Add parameters to an URL and return the new URL."""
        scheme, netloc, path, query_string, fragment = urlsplit(initial_url)
        query_params = parse_qs(query_string)
        query_params.update(
            {
                parameter_name: [parameter_value]
                for parameter_name, parameter_value in extra_parameters.items()
            },
        )

        new_query_string = urlencode(query_params, doseq=True)

        return urlunsplit((scheme, netloc, path, new_query_string, fragment))

    def authenticate_request(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        """Authenticate a request."""
        if self.auth_headers:
            request.headers.update(self.auth_headers)
        if request.url and self.auth_params:
            request.url = APIAuthenticator.add_parameters(request.url, self.auth_params)
        return request

    def __call__(self, r: requests.PreparedRequest) -> requests.PreparedRequest:
        """Authenticate a request."""
        return self.authenticate_request(r)


class APIKeyAuthenticator(APIAuthenticator):
    """API authenticator using an API key."""

    key: str
    value: str
    location: t.Literal["headers", "params"] = "headers"

    @root_validator
    def post_root(cls, values: dict) -> "APIKeyAuthenticator":
        """Add the API key to the authentication parameters."""
        if values["location"] == "headers":
            values["auth_headers"][values["key"]] = values["value"]
        elif values["location"] == "params":
            values["auth_params"][values["key"]] = values["value"]
        else:
            raise ValueError("Invalid location for API key, must be 'headers' or 'params'")
        return values


class BearerTokenAuthenticator(APIAuthenticator):
    """API authenticator using a bearer token."""

    token: str
    base64_encode: bool = False

    @root_validator
    def post_root(cls, values: dict) -> "BearerTokenAuthenticator":
        """Add the bearer token to the authentication headers."""
        if values["base64_encode"]:
            values["token"] = base64.b64encode(values["token"].encode("utf-8")).decode("utf-8")
        values["auth_headers"]["Authorization"] = f"Bearer {values['token']}"
        return values


class BasicAuthenticator(APIAuthenticator):
    """API authenticator using basic authentication."""

    username: str
    password: str

    @root_validator
    def post_root(cls, values: dict) -> "BasicAuthenticator":
        """Add the basic authentication to the authentication headers."""
        credentials = f"{values['username']}:{values['password']}".encode("utf-8")
        token = base64.b64encode(credentials).decode("utf-8")
        values["auth_headers"]["Authorization"] = f"Basic {token}"
        return values


class NoAuthAuthenticator(APIAuthenticator):
    """API authenticator using no authentication."""

    pass


class _OAuthAuthenticator(APIAuthenticator):
    """API authenticator using OAuth 2.0."""

    auth_endpoint: str
    oauth_scopes: str | t.List[str]
    oauth_headers: dict = {}
    default_expiration: int | None = None

    # Internal tracking attributes
    access_token: str | None = None
    refresh_token: str | None = None
    last_refreshed: pendulum.DateTime | None = None
    expires_in: int | None = None

    @validator("oauth_scopes", pre=True)
    def validate_oauth_scopes(cls, value: str | t.List[str]) -> str:
        """Validate the OAuth scopes."""
        if isinstance(value, list):
            return " ".join(value)
        return value

    @property
    def auth_headers(self) -> dict:
        """Return a dictionary of auth headers to be applied."""
        if not self.is_token_valid():
            self.update_access_token()
        result = super().auth_headers
        result["Authorization"] = f"Bearer {self.access_token}"
        return result

    def is_token_valid(self) -> bool:
        """Check if the access token is valid."""
        if self.access_token is None:
            return False
        if self.expires_in is None:
            return True
        if self.last_refreshed is None:
            return True
        if self.default_expiration is None:
            return True
        if self.last_refreshed + timedelta(seconds=self.expires_in) < pendulum.now():
            return False
        return True

    def update_access_token(self) -> None:
        """Update the access token."""
        if self.auth_endpoint is None:
            raise ValueError("No auth endpoint specified")
        if self.oauth_scopes is None:
            raise ValueError("No OAuth scopes specified")
        if self.oauth_headers is None:
            raise ValueError("No OAuth headers specified")

        logger.debug("Updating access token")
        response = requests.post(
            url=self.auth_endpoint,
            headers=self.oauth_headers,
            data={
                "grant_type": "client_credentials",
                "scope": self.oauth_scopes,
            },
        )
        response.raise_for_status()
        response_data = response.json()
        self.access_token = response_data["access_token"]
        self.refresh_token = response_data.get("refresh_token")
        self.expires_in = response_data.get("expires_in")
        self.last_refreshed = pendulum.now()


class OAuthJWTAuthenticator(_OAuthAuthenticator):
    """API authenticator using OAuth 2.0 with JWT."""

    client_id: str
    private_key: str
    private_key_passphrase: str | None = None

    @property
    def oauth_request_body(self) -> dict:
        """Return request body for OAuth request."""
        request_time: pendulum.DateTime = pendulum.utcnow()
        return {
            "iss": self.client_id,
            "scope": self.oauth_scopes,
            "aud": self.auth_endpoint,
            "exp": math.floor((request_time + timedelta(hours=1)).timestamp()),
            "iat": math.floor(request_time.timestamp()),
        }

    @property
    def oauth_request_payload(self) -> dict:
        """Return request paytload for OAuth request."""
        private_key: bytes | t.Any = bytes(self.private_key, "UTF-8")
        if self.private_key_passphrase:
            passphrase = bytes(self.private_key_passphrase, "UTF-8")
            private_key = serialization.load_pem_private_key(
                private_key,
                password=passphrase,
                backend=default_backend(),
            )
        private_key_string: str | t.Any = private_key.decode("UTF-8")
        return {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": jwt.encode(
                self.oauth_request_body,
                private_key_string,
                "RS256",
            ),
        }

    def update_access_token(self) -> None:
        """Update `access_token` along with: `last_refreshed` and `expires_in`.

        Raises:
            RuntimeError: When OAuth login fails.
        """
        request_time: pendulum.DateTime = pendulum.utcnow()
        auth_request_payload = self.oauth_request_payload
        token_response = requests.post(
            self.auth_endpoint,
            headers=self.oauth_headers,
            data=auth_request_payload,
            timeout=60,
        )
        try:
            token_response.raise_for_status()
        except requests.HTTPError as e:
            raise RuntimeError(
                "Failed OAuth login, response was '%s'. %s", token_response.json(), e
            ) from e

        logger.info("OAuth authorization attempt was successful.")

        token_json: dict = token_response.json()
        self.access_token = token_json["access_token"]
        expiration = token_json.get("expires_in", self.default_expiration)
        self.expires_in = int(expiration) if expiration else None
        if self.expires_in is None:
            logger.debug(
                (
                    "No expires_in receied in OAuth response and no "
                    "default_expiration set. Token will be treated as if it never "
                    "expires."
                ),
            )
        self.last_refreshed = request_time


class APIAuthenticatorChain(APIAuthenticator):
    """API authenticator using a chain of authenticators."""

    authenticators: t.List[APIAuthenticator] = []

    def authenticate_request(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        """Authenticate a request."""
        for authenticator in self.authenticators:
            request = authenticator.authenticate_request(request)
        return request


class APIAuthenticatorFactory:
    """Factory for API authenticators."""

    @staticmethod
    def create_authenticator(authenticator: t.Union[APIAuthenticator, dict]) -> APIAuthenticator:
        """Create an API authenticator from a dict or an APIAuthenticator."""
        if isinstance(authenticator, APIAuthenticator):
            return authenticator
        elif isinstance(authenticator, dict):
            authenticator_type = authenticator.pop("type", "NoAuthAuthenticator")
            if authenticator_type == "NoAuthAuthenticator":
                return NoAuthAuthenticator(**authenticator)
            elif authenticator_type == "APIKeyAuthenticator":
                return APIKeyAuthenticator(**authenticator)
            elif authenticator_type == "BearerTokenAuthenticator":
                return BearerTokenAuthenticator(**authenticator)
            elif authenticator_type == "BasicAuthenticator":
                return BasicAuthenticator(**authenticator)
            elif authenticator_type == "OAuthAuthenticator":
                return OAuthJWTAuthenticator(**authenticator)
            elif authenticator_type == "APIAuthenticatorChain":
                return APIAuthenticatorChain(
                    authenticators=[
                        APIAuthenticatorFactory.create_authenticator(authenticator)
                        for authenticator in authenticator["authenticators"]
                    ]
                )
            else:
                raise ValueError(f"Unknown authenticator type: {authenticator_type}")
        else:
            raise ValueError("Unknown authenticator type")
