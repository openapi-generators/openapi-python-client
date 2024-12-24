from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    path_param: str,
    *,
    string_param: Union[Unset, str] = UNSET,
    integer_param: Union[Unset, int] = 0,
    header_param: Union[None, Unset, str] = UNSET,
    cookie_param: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(header_param, Unset):
        headers["header param"] = header_param

    cookies = {}
    if cookie_param is not UNSET:
        cookies["cookie param"] = cookie_param

    params: dict[str, Any] = {}

    params["string param"] = string_param

    params["integer param"] = integer_param

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/parameter-references/{path_param}",
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
    path_param: str,
    *,
    client: Union[AuthenticatedClient, Client],
    string_param: Union[Unset, str] = UNSET,
    integer_param: Union[Unset, int] = 0,
    header_param: Union[None, Unset, str] = UNSET,
    cookie_param: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """Test different types of parameter references

    Args:
        path_param (str):
        string_param (Union[Unset, str]):
        integer_param (Union[Unset, int]):  Default: 0.
        header_param (Union[None, Unset, str]):
        cookie_param (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        path_param=path_param,
        string_param=string_param,
        integer_param=integer_param,
        header_param=header_param,
        cookie_param=cookie_param,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    path_param: str,
    *,
    client: Union[AuthenticatedClient, Client],
    string_param: Union[Unset, str] = UNSET,
    integer_param: Union[Unset, int] = 0,
    header_param: Union[None, Unset, str] = UNSET,
    cookie_param: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """Test different types of parameter references

    Args:
        path_param (str):
        string_param (Union[Unset, str]):
        integer_param (Union[Unset, int]):  Default: 0.
        header_param (Union[None, Unset, str]):
        cookie_param (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        path_param=path_param,
        string_param=string_param,
        integer_param=integer_param,
        header_param=header_param,
        cookie_param=cookie_param,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
