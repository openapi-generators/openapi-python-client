from http import HTTPStatus as _HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient as _AuthenticatedClient
from ...client import Client as _Client
from ...types import UNSET, Unset
from ...types import Response as _Response


def _get_kwargs(
    *,
    body: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/config/content-type-override",
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body

    headers["Content-Type"] = "openapi/python/client"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: _AuthenticatedClient | _Client, response: httpx.Response) -> str | None:
    if response.status_code == 200:
        response_200 = cast(str, response.json())
        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: _AuthenticatedClient | _Client, response: httpx.Response) -> _Response[str]:
    return _Response(
        status_code=_HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: _AuthenticatedClient | _Client,
    body: str | Unset = UNSET,
) -> _Response[str]:
    """Content Type Override

    Args:
        body (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: _AuthenticatedClient | _Client,
    body: str | Unset = UNSET,
) -> str | None:
    """Content Type Override

    Args:
        body (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        str
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: _AuthenticatedClient | _Client,
    body: str | Unset = UNSET,
) -> _Response[str]:
    """Content Type Override

    Args:
        body (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: _AuthenticatedClient | _Client,
    body: str | Unset = UNSET,
) -> str | None:
    """Content Type Override

    Args:
        body (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        str
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
