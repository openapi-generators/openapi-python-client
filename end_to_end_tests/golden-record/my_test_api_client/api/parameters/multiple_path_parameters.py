from typing import Any, Dict

import httpx

from ...client import Client
from ...types import Response


def _get_kwargs(
    param_4: str,
    param_2: int,
    param_1: str,
    param_3: int,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/multiple-path-parameters/{param4}/{param2}/{param1}/{param3}".format(
        client.base_url, param4=param_4, param2=param_2, param1=param_1, param3=param_3
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _build_response(*, response: httpx.Response) -> Response[None]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    param_4: str,
    param_2: int,
    param_1: str,
    param_3: int,
    *,
    client: Client,
) -> Response[None]:
    kwargs = _get_kwargs(
        param_4=param_4,
        param_2=param_2,
        param_1=param_1,
        param_3=param_3,
        client=client,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    param_4: str,
    param_2: int,
    param_1: str,
    param_3: int,
    *,
    client: Client,
) -> Response[None]:
    kwargs = _get_kwargs(
        param_4=param_4,
        param_2=param_2,
        param_1=param_1,
        param_3=param_3,
        client=client,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)
