from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
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
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[None]:
    if response.status_code == HTTPStatus.OK:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[None]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    param4: str,
    param2: int,
    param1: str,
    param3: int,
    *,
    client: Client,
) -> Response[None]:
    """
    Args:
        param4 (str):
        param2 (int):
        param1 (str):
        param3 (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[None]
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

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    param4: str,
    param2: int,
    param1: str,
    param3: int,
    *,
    client: Client,
) -> Response[None]:
    """
    Args:
        param4 (str):
        param2 (int):
        param1 (str):
        param3 (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[None]
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

    return _build_response(client=client, response=response)
