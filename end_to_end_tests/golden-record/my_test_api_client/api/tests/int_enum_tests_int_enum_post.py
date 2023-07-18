from http import HTTPStatus
from typing import Any, Dict

import httpx

from ... import errors
from ...client import Client
from ...models.an_int_enum import AnIntEnum
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: Client,
    int_enum: AnIntEnum,
) -> Dict[str, Any]:
    url = "{}/tests/int_enum".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_int_enum = int_enum.value

    params["int_enum"] = json_int_enum

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Any:
    if response.status_code == HTTPStatus.OK:
        response_200 = response.json()
        return response_200
    response.raise_for_status()
    raise errors.UnexpectedStatus(response.status_code, response.content)


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    int_enum: AnIntEnum,
) -> Response[Any]:
    """Int Enum

    Args:
        int_enum (AnIntEnum): An enumeration.

    Raises:
        httpx.HTTPStatusError: If the server returns an error status code.
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        int_enum=int_enum,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    int_enum: AnIntEnum,
) -> Any:
    """Int Enum

    Args:
        int_enum (AnIntEnum): An enumeration.

    Raises:
        httpx.HTTPStatusError: If the server returns an error status code.
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any
    """

    return sync_detailed(
        client=client,
        int_enum=int_enum,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    int_enum: AnIntEnum,
) -> Response[Any]:
    """Int Enum

    Args:
        int_enum (AnIntEnum): An enumeration.

    Raises:
        httpx.HTTPStatusError: If the server returns an error status code.
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        int_enum=int_enum,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    int_enum: AnIntEnum,
) -> Any:
    """Int Enum

    Args:
        int_enum (AnIntEnum): An enumeration.

    Raises:
        httpx.HTTPStatusError: If the server returns an error status code.
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any
    """

    return (
        await asyncio_detailed(
            client=client,
            int_enum=int_enum,
        )
    ).parsed
