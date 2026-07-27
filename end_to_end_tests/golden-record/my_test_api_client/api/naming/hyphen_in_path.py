from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response


def _get_kwargs(
    hyphen_in_path: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/naming/{hyphen_in_path}".format(
            hyphen_in_path=quote(str(hyphen_in_path), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> None:
    response.raise_for_status()
    if response.status_code == 200:
        return None

    raise errors.UnexpectedStatus(response.status_code, response.content)


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
    hyphen_in_path: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[None]:
    """
    Args:
        hyphen_in_path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[None]
    """

    kwargs = _get_kwargs(
        hyphen_in_path=hyphen_in_path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def request(
    hyphen_in_path: str,
    *,
    client: AuthenticatedClient | Client,
) -> None:
    """
    Args:
        hyphen_in_path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        None
    """

    await _request_detailed(
        hyphen_in_path=hyphen_in_path,
        client=client,
    )
