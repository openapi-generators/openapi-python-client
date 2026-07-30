from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.an_int_enum import AnIntEnum
from ...types import UNSET, Response


def _get_kwargs(
    *,
    int_enum: AnIntEnum,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_int_enum = int_enum.value
    params["int_enum"] = json_int_enum

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/enum/int",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> None:
    if response.status_code == 200:
        return None

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[None]:
    # Called for the status check alone -- it raises on an undocumented code and has no
    # value to hand back.
    _parse_response(client=client, response=response)
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


async def _request_detailed(
    *,
    client: AuthenticatedClient | Client,
    int_enum: AnIntEnum,
) -> Response[None]:
    """Int Enum

    Args:
        int_enum (AnIntEnum): An enumeration.

    Raises:
        errors.UnexpectedStatus: If the server returns a status code that is not a documented
            success. A documented error response is parsed onto UnexpectedStatus.parsed. An
            undocumented status code raises only when Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[None]
    """

    kwargs = _get_kwargs(
        int_enum=int_enum,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def request(
    *,
    client: AuthenticatedClient | Client,
    int_enum: AnIntEnum,
) -> None:
    """Int Enum

    Args:
        int_enum (AnIntEnum): An enumeration.

    Raises:
        errors.UnexpectedStatus: If the server returns a status code that is not a documented
            success. A documented error response is parsed onto UnexpectedStatus.parsed. An
            undocumented status code raises only when Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        None
    """

    await _request_detailed(
        client=client,
        int_enum=int_enum,
    )
