from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.status_code_patterns_response_2xx import StatusCodePatternsResponse2XX
from ...models.status_code_patterns_response_4xx import StatusCodePatternsResponse4XX
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/response/status-codes/patterns",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[StatusCodePatternsResponse2XX, StatusCodePatternsResponse4XX]]:
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
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[StatusCodePatternsResponse2XX, StatusCodePatternsResponse4XX]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[StatusCodePatternsResponse2XX, StatusCodePatternsResponse4XX]]:
    """Status Code Patterns

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[StatusCodePatternsResponse2XX, StatusCodePatternsResponse4XX]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[StatusCodePatternsResponse2XX, StatusCodePatternsResponse4XX]]:
    """Status Code Patterns

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[StatusCodePatternsResponse2XX, StatusCodePatternsResponse4XX]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[StatusCodePatternsResponse2XX, StatusCodePatternsResponse4XX]]:
    """Status Code Patterns

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[StatusCodePatternsResponse2XX, StatusCodePatternsResponse4XX]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[StatusCodePatternsResponse2XX, StatusCodePatternsResponse4XX]]:
    """Status Code Patterns

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[StatusCodePatternsResponse2XX, StatusCodePatternsResponse4XX]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
