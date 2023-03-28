from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    path_param: str,
    *,
    client: Client,
    string_param: Union[Unset, None, str] = UNSET,
    integer_param: Union[Unset, None, int] = 0,
    header_param: Union[Unset, str] = UNSET,
    cookie_param: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/parameter-references/{path_param}".format(client.base_url, path_param=path_param)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(header_param, Unset):
        headers["header param"] = header_param

    if cookie_param is not UNSET:
        cookies["cookie param"] = cookie_param

    params: Dict[str, Any] = {}
    params["string param"] = string_param

    params["integer param"] = integer_param

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.OK:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    path_param: str,
    *,
    client: Client,
    string_param: Union[Unset, None, str] = UNSET,
    integer_param: Union[Unset, None, int] = 0,
    header_param: Union[Unset, str] = UNSET,
    cookie_param: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """Test different types of parameter references

    Args:
        path_param (str):
        string_param (Union[Unset, None, str]):
        integer_param (Union[Unset, None, int]):
        header_param (Union[Unset, str]):
        cookie_param (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        path_param=path_param,
        client=client,
        string_param=string_param,
        integer_param=integer_param,
        header_param=header_param,
        cookie_param=cookie_param,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    path_param: str,
    *,
    client: Client,
    string_param: Union[Unset, None, str] = UNSET,
    integer_param: Union[Unset, None, int] = 0,
    header_param: Union[Unset, str] = UNSET,
    cookie_param: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """Test different types of parameter references

    Args:
        path_param (str):
        string_param (Union[Unset, None, str]):
        integer_param (Union[Unset, None, int]):
        header_param (Union[Unset, str]):
        cookie_param (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        path_param=path_param,
        client=client,
        string_param=string_param,
        integer_param=integer_param,
        header_param=header_param,
        cookie_param=cookie_param,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)
