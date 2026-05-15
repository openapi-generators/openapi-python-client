from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.status_code_patterns_response_2xx import StatusCodePatternsResponse2XX
from ...models.status_code_patterns_response_4xx import StatusCodePatternsResponse4XX
from ...types import UNSET, Response, Unset


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/response/status-codes/patterns",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> StatusCodePatternsResponse2XX | StatusCodePatternsResponse4XX | None:
    if 200 <= response.status_code <= 299:
        response_2xx = StatusCodePatternsResponse2XX.from_dict(response.json())

        return response_2xx

    if 400 <= response.status_code <= 499:
        response_4xx = StatusCodePatternsResponse4XX.from_dict(response.json())

        return response_4xx

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[StatusCodePatternsResponse2XX | StatusCodePatternsResponse4XX]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    headers: dict[str, str] | None = None,
    timeout: httpx.Timeout | None | Unset = UNSET,
    auth: httpx.Auth | None | Unset = UNSET,
) -> Response[StatusCodePatternsResponse2XX | StatusCodePatternsResponse4XX]:
    """Status Code Patterns

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[StatusCodePatternsResponse2XX | StatusCodePatternsResponse4XX]
    """

    kwargs = _get_kwargs()
    if headers is not None:
        kwargs["headers"] = {**kwargs.get("headers", {}), **headers}
    if not isinstance(timeout, Unset):
        kwargs["timeout"] = timeout
    if not isinstance(auth, Unset):
        kwargs["auth"] = auth

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    headers: dict[str, str] | None = None,
    timeout: httpx.Timeout | None | Unset = UNSET,
    auth: httpx.Auth | None | Unset = UNSET,
) -> StatusCodePatternsResponse2XX | StatusCodePatternsResponse4XX | None:
    """Status Code Patterns

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        StatusCodePatternsResponse2XX | StatusCodePatternsResponse4XX
    """

    return sync_detailed(
        client=client,
        headers=headers,
        timeout=timeout,
        auth=auth,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    headers: dict[str, str] | None = None,
    timeout: httpx.Timeout | None | Unset = UNSET,
    auth: httpx.Auth | None | Unset = UNSET,
) -> Response[StatusCodePatternsResponse2XX | StatusCodePatternsResponse4XX]:
    """Status Code Patterns

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[StatusCodePatternsResponse2XX | StatusCodePatternsResponse4XX]
    """

    kwargs = _get_kwargs()
    if headers is not None:
        kwargs["headers"] = {**kwargs.get("headers", {}), **headers}
    if not isinstance(timeout, Unset):
        kwargs["timeout"] = timeout
    if not isinstance(auth, Unset):
        kwargs["auth"] = auth

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    headers: dict[str, str] | None = None,
    timeout: httpx.Timeout | None | Unset = UNSET,
    auth: httpx.Auth | None | Unset = UNSET,
) -> StatusCodePatternsResponse2XX | StatusCodePatternsResponse4XX | None:
    """Status Code Patterns

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        StatusCodePatternsResponse2XX | StatusCodePatternsResponse4XX
    """

    return (
        await asyncio_detailed(
            client=client,
            headers=headers,
            timeout=timeout,
            auth=auth,
        )
    ).parsed
