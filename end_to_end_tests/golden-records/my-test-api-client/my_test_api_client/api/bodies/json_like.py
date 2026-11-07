from http import HTTPStatus as _HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient as _AuthenticatedClient
from ...client import Client as _Client
from ...models.json_like_body import JsonLikeBody
from ...types import UNSET, Unset
from ...types import Response as _Response


def _get_kwargs(
    *,
    body: JsonLikeBody | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/bodies/json-like",
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/vnd+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: _AuthenticatedClient | _Client, response: httpx.Response) -> Any | None:
    if response.status_code == 200:
        return None

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: _AuthenticatedClient | _Client, response: httpx.Response) -> _Response[Any]:
    return _Response(
        status_code=_HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: _AuthenticatedClient | _Client,
    body: JsonLikeBody | Unset = UNSET,
) -> _Response[Any]:
    """A content type that works like json but isn't application/json

    Args:
        body (JsonLikeBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: _AuthenticatedClient | _Client,
    body: JsonLikeBody | Unset = UNSET,
) -> _Response[Any]:
    """A content type that works like json but isn't application/json

    Args:
        body (JsonLikeBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
