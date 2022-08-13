from typing import Any, Dict

import httpx

from ...client import Client
from ...types import UNSET, Response


def _get_kwargs(
    path_param: str,
    *,
    client: Client,
    string_param: str,
    integer_param: int = 0,
    header_param: str,
    cookie_param: str,
) -> Dict[str, Any]:
    url = "{}/parameter-references/{path_param}".format(client.base_url, path_param=path_param)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    headers["header param"] = header_param

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
    path_param: str,
    *,
    client: Client,
    string_param: str,
    integer_param: int = 0,
    header_param: str,
    cookie_param: str,
) -> Response[Any]:
    """Test different types of parameter references

    Args:
        path_param (str):
        string_param (str):
        integer_param (int):
        header_param (str):
        cookie_param (str):

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

    return _build_response(response=response)


async def asyncio_detailed(
    path_param: str,
    *,
    client: Client,
    string_param: str,
    integer_param: int = 0,
    header_param: str,
    cookie_param: str,
) -> Response[Any]:
    """Test different types of parameter references

    Args:
        path_param (str):
        string_param (str):
        integer_param (int):
        header_param (str):
        cookie_param (str):

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

    return _build_response(response=response)
