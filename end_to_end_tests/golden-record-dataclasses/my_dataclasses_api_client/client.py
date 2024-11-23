from copy import copy
from dataclasses import dataclass, field, replace
from typing import Any, Dict, Optional

import httpx


@dataclass
class _HttpxConfig:
    cookies: Dict[str, str] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    timeout: Optional[httpx.Timeout] = None
    verify_ssl: bool = True
    follow_redirects: bool = False
    httpx_args: Dict[str, str] = field(default_factory=dict)


class Client:
    """A class for keeping track of data related to the API

    The following are accepted as keyword arguments and will be used to construct httpx Clients internally:

        ``base_url``: The base URL for the API, all requests are made to a relative path to this URL

        ``cookies``: A dictionary of cookies to be sent with every request

        ``headers``: A dictionary of headers to be sent with every request

        ``timeout``: The maximum amount of a time a request can take. API functions will raise
        httpx.TimeoutException if this is exceeded.

        ``verify_ssl``: Whether or not to verify the SSL certificate of the API server. This should be True in production,
        but can be set to False for testing purposes.

        ``follow_redirects``: Whether or not to follow redirects. Default value is False.

        ``httpx_args``: A dictionary of additional arguments to be passed to the ``httpx.Client`` and ``httpx.AsyncClient`` constructor.


    Attributes:
        raise_on_unexpected_status: Whether or not to raise an errors.UnexpectedStatus if the API returns a
            status code that was not documented in the source OpenAPI document. Can also be provided as a keyword
            argument to the constructor.
    """

    _base_url: str
    _httpx_config: _HttpxConfig
    _client: Optional[httpx.Client]
    _async_client: Optional[httpx.AsyncClient]

    def __init__(
        self,
        base_url: str,
        cookies: Dict[str, str] = {},
        headers: Dict[str, str] = {},
        timeout: Optional[httpx.Timeout] = None,
        verify_ssl: bool = True,
        follow_redirects: bool = False,
        httpx_args: Dict[str, Any] = {},
        raise_on_unexpected_status: bool = False,
    ) -> None:
        self.raise_on_unexpected_status = raise_on_unexpected_status
        self._base_url = base_url
        self._httpx_config = _HttpxConfig(cookies, headers, timeout, verify_ssl, follow_redirects, httpx_args)
        self._client = None
        self._async_client = None

    def _with_httpx_config(self, httpx_config: _HttpxConfig) -> "Client":
        ret = copy(self)
        ret._httpx_config = httpx_config
        ret._client = None
        ret._async_client = None
        return ret

    def with_headers(self, headers: Dict[str, str]) -> "Client":
        """Get a new client matching this one with additional headers"""
        if self._client is not None:
            self._client.headers.update(headers)
        if self._async_client is not None:
            self._async_client.headers.update(headers)
        return self._with_httpx_config(
            replace(self._httpx_config, headers={**self._httpx_config.headers, **headers}),
        )

    def with_cookies(self, cookies: Dict[str, str]) -> "Client":
        """Get a new client matching this one with additional cookies"""
        if self._client is not None:
            self._client.cookies.update(cookies)
        if self._async_client is not None:
            self._async_client.cookies.update(cookies)
        return self._with_httpx_config(
            replace(self._httpx_config, cookies={**self._httpx_config.cookies, **cookies}),
        )

    def with_timeout(self, timeout: httpx.Timeout) -> "Client":
        """Get a new client matching this one with a new timeout (in seconds)"""
        if self._client is not None:
            self._client.timeout = timeout
        if self._async_client is not None:
            self._async_client.timeout = timeout
        return self._with_httpx_config(replace(self._httpx_config, timeout=timeout))

    def set_httpx_client(self, client: httpx.Client) -> "Client":
        """Manually set the underlying httpx.Client

        **NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.
        """
        self._client = client
        return self

    def get_httpx_client(self) -> httpx.Client:
        """Get the underlying httpx.Client, constructing a new one if not previously set"""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self._base_url,
                cookies=self._httpx_config.cookies,
                headers=self._httpx_config.headers,
                timeout=self._httpx_config.timeout,
                verify=self._httpx_config.verify_ssl,
                follow_redirects=self._httpx_config.follow_redirects,
                **self._httpx_config.httpx_args,
            )
        return self._client

    def __enter__(self) -> "Client":
        """Enter a context manager for self.client—you cannot enter twice (see httpx docs)"""
        self.get_httpx_client().__enter__()
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        """Exit a context manager for internal httpx.Client (see httpx docs)"""
        self.get_httpx_client().__exit__(*args, **kwargs)

    def set_async_httpx_client(self, async_client: httpx.AsyncClient) -> "Client":
        """Manually the underlying httpx.AsyncClient

        **NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.
        """
        self._async_client = async_client
        return self

    def get_async_httpx_client(self) -> httpx.AsyncClient:
        """Get the underlying httpx.AsyncClient, constructing a new one if not previously set"""
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(
                base_url=self._httpx_config.base_url,
                cookies=self._httpx_config.cookies,
                headers=self._httpx_config.headers,
                timeout=self._httpx_config.timeout,
                verify=self._httpx_config.verify_ssl,
                follow_redirects=self._httpx_config.follow_redirects,
                **self._httpx_config.httpx_args,
            )
        return self._async_client

    async def __aenter__(self) -> "Client":
        """Enter a context manager for underlying httpx.AsyncClient—you cannot enter twice (see httpx docs)"""
        await self.get_async_httpx_client().__aenter__()
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        """Exit a context manager for underlying httpx.AsyncClient (see httpx docs)"""
        await self.get_async_httpx_client().__aexit__(*args, **kwargs)


class AuthenticatedClient:
    """A Client which has been authenticated for use on secured endpoints

    The following are accepted as keyword arguments and will be used to construct httpx Clients internally:

        ``base_url``: The base URL for the API, all requests are made to a relative path to this URL

        ``cookies``: A dictionary of cookies to be sent with every request

        ``headers``: A dictionary of headers to be sent with every request

        ``timeout``: The maximum amount of a time a request can take. API functions will raise
        httpx.TimeoutException if this is exceeded.

        ``verify_ssl``: Whether or not to verify the SSL certificate of the API server. This should be True in production,
        but can be set to False for testing purposes.

        ``follow_redirects``: Whether or not to follow redirects. Default value is False.

        ``httpx_args``: A dictionary of additional arguments to be passed to the ``httpx.Client`` and ``httpx.AsyncClient`` constructor.


    Attributes:
        raise_on_unexpected_status: Whether or not to raise an errors.UnexpectedStatus if the API returns a
            status code that was not documented in the source OpenAPI document. Can also be provided as a keyword
            argument to the constructor.
        token: The token to use for authentication
        prefix: The prefix to use for the Authorization header
        auth_header_name: The name of the Authorization header
    """

    _base_url: str
    token: str
    prefix: str = "Bearer"
    auth_header_name: str = "Authorization"
    _httpx_config: _HttpxConfig
    _client: Optional[httpx.Client]
    _async_client: Optional[httpx.AsyncClient]

    def __init__(
        self,
        base_url: str,
        token: str,
        prefix: str = "Bearer",
        auth_header_name: str = "Authorization",
        cookies: Dict[str, str] = {},
        headers: Dict[str, str] = {},
        timeout: Optional[httpx.Timeout] = None,
        verify_ssl: bool = True,
        follow_redirects: bool = False,
        httpx_args: Dict[str, Any] = {},
        raise_on_unexpected_status: bool = False,
    ) -> None:
        self.raise_on_unexpected_status = raise_on_unexpected_status
        self._base_url = base_url
        self._httpx_config = _HttpxConfig(cookies, headers, timeout, verify_ssl, follow_redirects, httpx_args)
        self._client = None
        self._async_client = None

        self.token = token
        self.prefix = prefix
        self.auth_header_name = auth_header_name

    def _with_httpx_config(self, httpx_config: _HttpxConfig) -> "AuthenticatedClient":
        ret = copy(self)
        ret._httpx_config = httpx_config
        ret._client = None
        ret._async_client = None
        return ret

    def with_headers(self, headers: Dict[str, str]) -> "AuthenticatedClient":
        """Get a new client matching this one with additional headers"""
        if self._client is not None:
            self._client.headers.update(headers)
        if self._async_client is not None:
            self._async_client.headers.update(headers)
        return self._with_httpx_config(
            replace(self._httpx_config, headers={**self._httpx_config.headers, **headers}),
        )

    def with_cookies(self, cookies: Dict[str, str]) -> "AuthenticatedClient":
        """Get a new client matching this one with additional cookies"""
        if self._client is not None:
            self._client.cookies.update(cookies)
        if self._async_client is not None:
            self._async_client.cookies.update(cookies)
        return self._with_httpx_config(
            replace(self._httpx_config, cookies={**self._httpx_config.cookies, **cookies}),
        )

    def with_timeout(self, timeout: httpx.Timeout) -> "AuthenticatedClient":
        """Get a new client matching this one with a new timeout (in seconds)"""
        if self._client is not None:
            self._client.timeout = timeout
        if self._async_client is not None:
            self._async_client.timeout = timeout
        return self._with_httpx_config(replace(self._httpx_config, timeout=timeout))

    def set_httpx_client(self, client: httpx.Client) -> "AuthenticatedClient":
        """Manually set the underlying httpx.Client

        **NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.
        """
        self._client = client
        return self

    def get_httpx_client(self) -> httpx.Client:
        """Get the underlying httpx.Client, constructing a new one if not previously set"""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self._base_url,
                cookies=self._httpx_config.cookies,
                headers={
                    self.auth_header_name: (f"{self.prefix} {self.token}" if self.prefix else self.token),
                    **self._httpx_config.headers,
                },
                timeout=self._httpx_config.timeout,
                verify=self._httpx_config.verify_ssl,
                follow_redirects=self._httpx_config.follow_redirects,
                **self._httpx_config.httpx_args,
            )
        return self._client

    def __enter__(self) -> "AuthenticatedClient":
        """Enter a context manager for self.client—you cannot enter twice (see httpx docs)"""
        self.get_httpx_client().__enter__()
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        """Exit a context manager for internal httpx.Client (see httpx docs)"""
        self.get_httpx_client().__exit__(*args, **kwargs)

    def set_async_httpx_client(self, async_client: httpx.AsyncClient) -> "AuthenticatedClient":
        """Manually the underlying httpx.AsyncClient

        **NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.
        """
        self._async_client = async_client
        return self

    def get_async_httpx_client(self) -> httpx.AsyncClient:
        """Get the underlying httpx.AsyncClient, constructing a new one if not previously set"""
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(
                base_url=self._httpx_config.base_url,
                cookies=self._httpx_config.cookies,
                headers={
                    self.auth_header_name: (f"{self.prefix} {self.token}" if self.prefix else self.token),
                    **self._httpx_config.headers,
                },
                timeout=self._httpx_config.timeout,
                verify=self._httpx_config.verify_ssl,
                follow_redirects=self._httpx_config.follow_redirects,
                **self._httpx_config.httpx_args,
            )
        return self._async_client

    async def __aenter__(self) -> "AuthenticatedClient":
        """Enter a context manager for underlying httpx.AsyncClient—you cannot enter twice (see httpx docs)"""
        await self.get_async_httpx_client().__aenter__()
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        """Exit a context manager for underlying httpx.AsyncClient (see httpx docs)"""
        await self.get_async_httpx_client().__aexit__(*args, **kwargs)
