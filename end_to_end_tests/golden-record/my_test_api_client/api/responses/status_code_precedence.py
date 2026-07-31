from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/response/status-codes/precedence",
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> str:
    if response.status_code == 200:
        response_200 = response.text
        return response_200

    if response.status_code == 404:
        if client.raise_on_unexpected_status:
            response_404 = response.text
            raise errors.UnexpectedStatus(
                response.status_code,
                response.content,
                parsed=response_404,
            )

        return cast(str, None)

    if 400 <= response.status_code <= 499:
        if client.raise_on_unexpected_status:
            response_4xx = response.text
            raise errors.UnexpectedStatus(
                response.status_code,
                response.content,
                parsed=response_4xx,
            )

        return cast(str, None)

    response_default = response.text
    return response_default


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


async def _request_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[str]:
    """Status Codes Precedence

     Verify that specific status codes are always checked first, then ranges, then default

    Raises:
        errors.UnexpectedStatus: If the server returns a status code that is not a documented
            success and Client.raise_on_unexpected_status is True. A documented error response is
            parsed onto UnexpectedStatus.parsed. With the flag set to False, those statuses return
            None instead of raising.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def request(
    *,
    client: AuthenticatedClient | Client,
) -> str:
    """Status Codes Precedence

     Verify that specific status codes are always checked first, then ranges, then default

    Raises:
        errors.UnexpectedStatus: If the server returns a status code that is not a documented
            success and Client.raise_on_unexpected_status is True. A documented error response is
            parsed onto UnexpectedStatus.parsed. With the flag set to False, those statuses return
            None instead of raising.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        str
    """

    return (
        await _request_detailed(
            client=client,
        )
    ).parsed
