from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    param_path: str,
    *,
    param_query: Union[Unset, str] = UNSET,
    param_header: Union[Unset, str] = UNSET,
    param_cookie: Union[Unset, str] = UNSET,
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
        "url": f"/same-name-multiple-locations/{param_path}",
        "params": params,
        "cookies": cookies,
    }

    _kwargs["headers"] = headers
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
    param_path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    param_query: Union[Unset, str] = UNSET,
    param_header: Union[Unset, str] = UNSET,
    param_cookie: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """
    Args:
        param_path (str):
        param_query (Union[Unset, str]):
        param_header (Union[Unset, str]):
        param_cookie (Union[Unset, str]):

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
    client: Union[AuthenticatedClient, Client],
    param_query: Union[Unset, str] = UNSET,
    param_header: Union[Unset, str] = UNSET,
    param_cookie: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """
    Args:
        param_path (str):
        param_query (Union[Unset, str]):
        param_header (Union[Unset, str]):
        param_cookie (Union[Unset, str]):

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
