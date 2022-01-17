from typing import Any, Dict

import httpx

from ...client import Client
from ...types import Response


def _get_kwargs(
    param4: str,
    param2: int,
    param1: str,
    param3: int,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/multiple-path-parameters/{param4}/something/{param2}/{param1}/{param3}".format(
        client.base_url, param4=param4, param2=param2, param1=param1, param3=param3
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    param4: str,
    param2: int,
    param1: str,
    param3: int,
    *,
    client: Client,
) -> Response[Any]:
    """
    Args:
        param4 (str):
        param2 (int):
        param1 (str):
        param3 (int):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        param4=param4,
        param2=param2,
        param1=param1,
        param3=param3,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    param4: str,
    param2: int,
    param1: str,
    param3: int,
    *,
    client: Client,
) -> Response[Any]:
    """
    Args:
        param4 (str):
        param2 (int):
        param1 (str):
        param3 (int):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        param4=param4,
        param2=param2,
        param1=param1,
        param3=param3,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
