from http import HTTPStatus
from io import BytesIO
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...types import File, Response


def _get_kwargs(
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/tests/octet_stream".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[File]:
    if response.status_code == HTTPStatus.OK:
        response_200 = File(payload=BytesIO(response.content))

        return response_200
    if response.status_code >= 400:
        if client.raise_on_unexpected_status or client.raise_on_error_status:
            raise errors.UnexpectedErrorStatus(f"Unexpected status code: {response.status_code}")
    else:
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedSuccessStatus(f"Unexpected status code: {response.status_code}")
    return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[File]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[File]:
    """Octet Stream

    Raises:
        errors.ErrorStatus: If the server returns an error status code and Client.raise_on_error_status is True.
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[File]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
) -> Optional[File]:
    """Octet Stream

    Raises:
        errors.ErrorStatus: If the server returns an error status code and Client.raise_on_error_status is True.
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[File]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[File]:
    """Octet Stream

    Raises:
        errors.ErrorStatus: If the server returns an error status code and Client.raise_on_error_status is True.
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[File]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
) -> Optional[File]:
    """Octet Stream

    Raises:
        errors.ErrorStatus: If the server returns an error status code and Client.raise_on_error_status is True.
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[File]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
