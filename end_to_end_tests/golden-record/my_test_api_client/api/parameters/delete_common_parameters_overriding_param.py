from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    param_path: str,
    *,
    param_query: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["param"] = param_query

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/common_parameters_overriding/{param_path}".format(
            param_path=quote(str(param_path), safe=""),
        ),
        "params": params,
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
    param_path: str,
    *,
    client: AuthenticatedClient | Client,
    param_query: str | Unset = UNSET,
) -> Response[None]:
    """
    Args:
        param_path (str):
        param_query (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[None]
    """

    kwargs = _get_kwargs(
        param_path=param_path,
        param_query=param_query,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def request(
    param_path: str,
    *,
    client: AuthenticatedClient | Client,
    param_query: str | Unset = UNSET,
) -> None:
    """
    Args:
        param_path (str):
        param_query (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        None
    """

    await _request_detailed(
        param_path=param_path,
        client=client,
        param_query=param_query,
    )
