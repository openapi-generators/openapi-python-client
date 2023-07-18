from http import HTTPStatus
from typing import Any, Dict, Union

import httpx

from ... import errors
from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    common: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/common_parameters".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["common"] = common

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> None:
    if response.status_code == HTTPStatus.OK:
        return None
    response.raise_for_status()
    raise errors.UnexpectedStatus(response.status_code, response.content)


def _build_response(*, response: httpx.Response) -> Response[None]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),  # type: ignore[func-returns-value]
    )


def sync_detailed(
    *,
    client: Client,
    common: Union[Unset, None, str] = UNSET,
) -> Response[None]:
    """
    Args:
        common (Union[Unset, None, str]):

    Raises:
        httpx.HTTPStatusError: If the server returns an error status code.
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[None]
    """

    kwargs = _get_kwargs(
        client=client,
        common=common,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: Client,
    common: Union[Unset, None, str] = UNSET,
) -> Response[None]:
    """
    Args:
        common (Union[Unset, None, str]):

    Raises:
        httpx.HTTPStatusError: If the server returns an error status code.
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[None]
    """

    kwargs = _get_kwargs(
        client=client,
        common=common,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
