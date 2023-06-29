import ssl
from typing import Dict, Union, Optional, Tuple

from attrs import define, field, evolve
import httpx


@define
class Client:
    """A class for keeping track of data related to the API

    The following are accepted as keyword arguments and will be used to construct httpx Clients internally:

        ``base_url``: The base URL for the API, all requests are made to a relative path to this URL

        ``cookies``: A dictionary of cookies to be sent with every request

        ``headers``: A dictionary of headers to be sent with every request

        ``timeout``: The maximum amount of a time in seconds a request can take. API functions will raise
        httpx.TimeoutException if this is exceeded.

        ``verify_ssl``: Whether or not to verify the SSL certificate of the API server. This should be True in production,
        but can be set to False for testing purposes.

        ``follow_redirects``: Whether or not to follow redirects. Default value is False.

    Attributes:
        raise_on_unexpected_status: Whether or not to raise an errors.UnexpectedStatus if the API returns a
            status code that was not documented in the source OpenAPI document. Can also be provided as a keyword
            argument to the constructor.
    """

    raise_on_unexpected_status: bool = field(default=False, kw_only=True)
    _base_url: str
    _cookies: Dict[str, str] = field(factory=dict, kw_only=True)
    _headers: Dict[str, str] = field(factory=dict, kw_only=True)
    _timeout: float = field(default=5.0, kw_only=True)
    _verify_ssl: Union[str, bool, ssl.SSLContext] = field(default=True, kw_only=True)
    _follow_redirects: bool = field(default=False, kw_only=True)
    _client: Optional[httpx.Client] = field(default=None, init=False)
    _async_client: Optional[httpx.AsyncClient] = field(default=None, init=False)

    def with_headers(self, headers: Dict[str, str]) -> "Client":
        """Get a new client matching this one with additional headers"""
        if self._client is not None:
            self._client.headers.update(headers)
        if self._async_client is not None:
            self._async_client.headers.update(headers)
        return evolve(self, headers={**self._headers, **headers})

    def with_cookies(self, cookies: Dict[str, str]) -> "Client":
        """Get a new client matching this one with additional cookies"""
        if self._client is not None:
            self._client.cookies.update(cookies)
        if self._async_client is not None:
            self._async_client.cookies.update(cookies)
        return evolve(self, cookies={**self._cookies, **cookies})

    def with_timeout(self, timeout: float) -> "Client":
        """Get a new client matching this one with a new timeout (in seconds)"""
        if self._client is not None:
            self._client.timeout = timeout
        if self._async_client is not None:
            self._async_client.timeout = timeout
        return evolve(self, timeout=timeout)

    def set_client(self, client: httpx.Client) -> "Client":
        """Manually the underlying httpx.Client

        **NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.
        """
        self._client = client
        return self

    def get_client(self) -> httpx.Client:
        """Get the underlying httpx.Client, constructing a new one if not previously set"""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
            )
        return self._client

    def __enter__(self) -> "Client":
        """Enter a context manager for self.client—you cannot enter twice (see httpx docs)"""
        self.get_client().__enter__()
        return self

    def __exit__(self, *args, **kwargs) -> None:
        """Exit a context manager for self.client (see httpx docs)"""
        self.get_client().__exit__(*args, **kwargs)

    def set_async_client(self, async_client: httpx.AsyncClient) -> "Client":
        """Manually the underlying httpx.AsyncClient

        **NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.
        """
        self._async_client = async_client
        return self

    def get_async_client(self) -> httpx.AsyncClient:
        """Get the underlying httpx.AsyncClient, constructing a new one if not previously set"""
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(base_url=self._base_url, cookies=self._cookies, headers=self._headers, timeout=self._timeout, verify=self._verify_ssl, follow_redirects=self._follow_redirects)
        return self._async_client

    async def __aenter__(self) -> "Client":
        """Enter a context manager for self.async_client—you cannot enter twice (see httpx docs)"""
        await self.get_async_client().__aenter__()
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        """Exit a context manager for self.async_client (see httpx docs)"""
        await self.get_async_client().__aexit__(*args, **kwargs)


@define
class AuthenticatedClient:
    """A Client which has been authenticated for use on secured endpoints

    The following are accepted as keyword arguments and will be used to construct httpx Clients internally:

        ``base_url``: The base URL for the API, all requests are made to a relative path to this URL

        ``cookies``: A dictionary of cookies to be sent with every request

        ``headers``: A dictionary of headers to be sent with every request

        ``timeout``: The maximum amount of a time in seconds a request can take. API functions will raise
        httpx.TimeoutException if this is exceeded.

        ``verify_ssl``: Whether or not to verify the SSL certificate of the API server. This should be True in production,
        but can be set to False for testing purposes.

        ``follow_redirects``: Whether or not to follow redirects. Default value is False.

    Attributes:
        raise_on_unexpected_status: Whether or not to raise an errors.UnexpectedStatus if the API returns a
            status code that was not documented in the source OpenAPI document. Can also be provided as a keyword
            argument to the constructor.
    """

    raise_on_unexpected_status: bool = field(default=False, kw_only=True)
    _base_url: str
    token: str
    prefix: str = "Bearer"
    auth_header_name: str = "Authorization"
    _cookies: Dict[str, str] = field(factory=dict, kw_only=True)
    _headers: Dict[str, str] = field(factory=dict, kw_only=True)
    _timeout: float = field(default=5.0, kw_only=True)
    _verify_ssl: Union[str, bool, ssl.SSLContext] = field(default=True, kw_only=True)
    _follow_redirects: bool = field(default=False, kw_only=True)
    _client: Optional[httpx.Client] = field(default=None, init=False)
    _async_client: Optional[httpx.AsyncClient] = field(default=None, init=False)

    def with_headers(self, headers: Dict[str, str]) -> "AuthenticatedClient":
        """Get a new client matching this one with additional headers"""
        if self._client is not None:
            self._client.headers.update(headers)
        if self._async_client is not None:
            self._async_client.headers.update(headers)
        return evolve(self, headers={**self._headers, **headers})

    def with_cookies(self, cookies: Dict[str, str]) -> "AuthenticatedClient":
        """Get a new client matching this one with additional cookies"""
        if self._client is not None:
            self._client.cookies.update(cookies)
        if self._async_client is not None:
            self._async_client.cookies.update(cookies)
        return evolve(self, cookies={**self._cookies, **cookies})

    def with_timeout(self, timeout: float) -> "AuthenticatedClient":
        """Get a new client matching this one with a new timeout (in seconds)"""
        if self._client is not None:
            self._client.timeout = timeout
        if self._async_client is not None:
            self._async_client.timeout = timeout
        return evolve(self, timeout=timeout)

    def set_client(self, client: httpx.Client) -> "AuthenticatedClient":
        """Manually the underlying httpx.Client

        **NOTE**: This will override any other settings on the client, including cookies, headers, and timeout. Set up
          auth **manually** if using this method.
        """
        self._client = client
        return self

    def get_client(self) -> httpx.Client:
        """Get the underlying httpx.Client, constructing a new one if not previously set"""
        if self._client is None:
            self._headers[self.auth_header_name] = f"{self.prefix} {self.token}" if self.prefix else self.token
            self._client = httpx.Client(
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
            )
        return self._client

    def __enter__(self) -> "Client":
        """Enter a context manager for self.client—you cannot enter twice (see httpx docs)"""
        with self.get_client():
            yield self

    def set_async_client(self, async_client: httpx.AsyncClient) -> "AuthenticatedClient":
        """Manually the underlying httpx.AsyncClient

        **NOTE**: This will override any other settings on the client, including cookies, headers, and timeout. Set up
          auth **manually** if using this method.
        """
        self._async_client = async_client
        return self

    def get_async_client(self) -> httpx.AsyncClient:
        """Get the underlying httpx.AsyncClient"""
        if self._async_client is None:
            self._headers[self.auth_header_name] = f"{self.prefix} {self.token}" if self.prefix else self.token
            self._async_client = httpx.AsyncClient(
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
            )
        return self._async_client

    async def __aenter__(self) -> "Client":
        """Enter a context manager for self.async_client—you cannot enter twice (see httpx docs)"""
        async with self.get_async_client():
            yield self
