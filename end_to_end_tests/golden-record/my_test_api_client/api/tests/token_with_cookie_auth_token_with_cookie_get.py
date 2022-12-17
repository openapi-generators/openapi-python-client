from http import HTTPStatus
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

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    cookies["MyToken"] = my_token

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.OK:
        response_200 = None
        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = None
        return response_401
    if client.raise_on_unexpected_status:
        raise Exception(f"Unexpected status code: {response.status_code}")
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
    *,
    client: Client,
    my_token: str,
) -> Response[Any]:
    """TOKEN_WITH_COOKIE

     Test optional cookie parameters

    Args:
        my_token (str):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        my_token=my_token,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: Client,
    my_token: str,
) -> Response[Any]:
    """TOKEN_WITH_COOKIE

     Test optional cookie parameters

    Args:
        my_token (str):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        my_token=my_token,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)
