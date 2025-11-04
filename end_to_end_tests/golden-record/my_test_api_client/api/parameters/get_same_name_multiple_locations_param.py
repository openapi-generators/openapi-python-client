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
    param_header: str | Unset = UNSET,
    param_cookie: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(param_header, Unset):
        headers["param"] = param_header

    cookies = {}
    if param_cookie is not UNSET:
        cookies["param"] = param_cookie

    params: dict[str, Any] = {}

    params["param"] = param_query

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/same-name-multiple-locations/{param_path}".format(
            param_path=quote(str(param_path), safe=""),
        ),
        "params": params,
        "cookies": cookies,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | None:
    if response.status_code == 200:
        return None

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    param_path: str,
    *,
    client: AuthenticatedClient | Client,
    param_query: str | Unset = UNSET,
    param_header: str | Unset = UNSET,
    param_cookie: str | Unset = UNSET,
) -> Response[Any]:
    """
    Args:
        param_path (str):
        param_query (str | Unset):
        param_header (str | Unset):
        param_cookie (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        param_path=param_path,
        param_query=param_query,
        param_header=param_header,
        param_cookie=param_cookie,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    param_path: str,
    *,
    client: AuthenticatedClient | Client,
    param_query: str | Unset = UNSET,
    param_header: str | Unset = UNSET,
    param_cookie: str | Unset = UNSET,
) -> Response[Any]:
    """
    Args:
        param_path (str):
        param_query (str | Unset):
        param_header (str | Unset):
        param_cookie (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        param_path=param_path,
        param_query=param_query,
        param_header=param_header,
        param_cookie=param_cookie,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
