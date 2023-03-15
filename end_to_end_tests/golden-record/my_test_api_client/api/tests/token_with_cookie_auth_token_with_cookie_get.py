from http import HTTPStatus
from typing import Any, Dict, Union

import httpx

from ... import errors
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
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Union[Any, None]:
    if response.status_code == HTTPStatus.OK:
        response_200 = response.json()
        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = None
        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, None]]:
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
) -> Response[Union[Any, None]]:
    """TOKEN_WITH_COOKIE

     Test optional cookie parameters

    Args:
        my_token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, None]]
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


def sync(
    *,
    client: Client,
    my_token: str,
) -> Union[Any, None]:
    """TOKEN_WITH_COOKIE

     Test optional cookie parameters

    Args:
        my_token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, None]
    """

    return sync_detailed(
        client=client,
        my_token=my_token,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    my_token: str,
) -> Response[Union[Any, None]]:
    """TOKEN_WITH_COOKIE

     Test optional cookie parameters

    Args:
        my_token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, None]]
    """

    kwargs = _get_kwargs(
        client=client,
        my_token=my_token,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    my_token: str,
) -> Union[Any, None]:
    """TOKEN_WITH_COOKIE

     Test optional cookie parameters

    Args:
        my_token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, None]
    """

    return (
        await asyncio_detailed(
            client=client,
            my_token=my_token,
        )
    ).parsed
