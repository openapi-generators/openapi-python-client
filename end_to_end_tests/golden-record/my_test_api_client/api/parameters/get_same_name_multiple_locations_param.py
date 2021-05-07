from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    param_path: Union[Unset, str] = UNSET,
    param_query: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/same-name-multiple-locations/{param}".format(client.base_url, param=param_path)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "param": param_query,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Any]:
    if response.status_code == 200:
        response_200 = None

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    param_path: Union[Unset, str] = UNSET,
    param_query: Union[Unset, str] = UNSET,
) -> Response[Any]:
    kwargs = _get_kwargs(
        client=client,
        param_path=param_path,
        param_query=param_query,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    param_path: Union[Unset, str] = UNSET,
    param_query: Union[Unset, str] = UNSET,
) -> Optional[Any]:
    """ """

    return sync_detailed(
        client=client,
        param_path=param_path,
        param_query=param_query,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    param_path: Union[Unset, str] = UNSET,
    param_query: Union[Unset, str] = UNSET,
) -> Response[Any]:
    kwargs = _get_kwargs(
        client=client,
        param_path=param_path,
        param_query=param_query,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    param_path: Union[Unset, str] = UNSET,
    param_query: Union[Unset, str] = UNSET,
) -> Optional[Any]:
    """ """

    return (
        await asyncio_detailed(
            client=client,
            param_path=param_path,
            param_query=param_query,
        )
    ).parsed
