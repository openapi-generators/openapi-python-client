from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response


def _get_kwargs(
    param4: str,
    param2: int,
    param1: str,
    param3: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/multiple-path-parameters/{param4}/something/{param2}/{param1}/{param3}",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == 200:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    param4: str,
    param2: int,
    param1: str,
    param3: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Any]:
    """
    Args:
        param4 (str):
        param2 (int):
        param1 (str):
        param3 (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        param4=param4,
        param2=param2,
        param1=param1,
        param3=param3,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    param4: str,
    param2: int,
    param1: str,
    param3: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Any]:
    """
    Args:
        param4 (str):
        param2 (int):
        param1 (str):
        param3 (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        param4=param4,
        param2=param2,
        param1=param1,
        param3=param3,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
