from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    param_path: str,
    *,
    client: Client,
    param_query: Union[Unset, None, str] = UNSET,
    param_header: Union[Unset, str] = UNSET,
    param_cookie: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/same-name-multiple-locations/{param}".format(client.base_url, param=param_path)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(param_header, Unset):
        headers["param"] = param_header

    if param_cookie is not UNSET:
        cookies["param"] = param_cookie

    params: Dict[str, Any] = {}
    params["param"] = param_query

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    param_path: str,
    *,
    client: Client,
    param_query: Union[Unset, None, str] = UNSET,
    param_header: Union[Unset, str] = UNSET,
    param_cookie: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """
    Args:
        param_path (str):
        param_query (Union[Unset, None, str]):
        param_header (Union[Unset, str]):
        param_cookie (Union[Unset, str]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        param_path=param_path,
        client=client,
        param_query=param_query,
        param_header=param_header,
        param_cookie=param_cookie,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    param_path: str,
    *,
    client: Client,
    param_query: Union[Unset, None, str] = UNSET,
    param_header: Union[Unset, str] = UNSET,
    param_cookie: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """
    Args:
        param_path (str):
        param_query (Union[Unset, None, str]):
        param_header (Union[Unset, str]):
        param_cookie (Union[Unset, str]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        param_path=param_path,
        client=client,
        param_query=param_query,
        param_header=param_header,
        param_cookie=param_cookie,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
