from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    my_token: str,
) -> Dict[str, Any]:
    url = "{}/auth/token_with_cookie".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    cookies["MyToken"] = my_token

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Any]:
    if response.status_code == 200:
        response_200 = None

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
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
    my_token: str,
) -> Response[Any]:
    kwargs = _get_kwargs(
        client=client,
        my_token=my_token,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    my_token: str,
) -> Optional[Any]:
    """Test optional cookie parameters"""

    return sync_detailed(
        client=client,
        my_token=my_token,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    my_token: str,
) -> Response[Any]:
    kwargs = _get_kwargs(
        client=client,
        my_token=my_token,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    my_token: str,
) -> Optional[Any]:
    """Test optional cookie parameters"""

    return (
        await asyncio_detailed(
            client=client,
            my_token=my_token,
        )
    ).parsed
