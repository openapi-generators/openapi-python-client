from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/responses/unions/number-or-string",
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> float | str:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> float | str:
            if type(data) not in {int, float, str}:
                raise TypeError(f"Response did not match any declared union type, got {type(data).__name__}")
            return cast(float | str, data)

        response_200 = _parse_response_200(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return cast(float | str, None)


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[float | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


async def _request_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[float | str]:
    """A union with a `number` member: JSON draws no int/float distinction, so an integer body is valid.

    Raises:
        errors.UnexpectedStatus: If the server returns a status code that is not a documented
            success and Client.raise_on_unexpected_status is True. A documented error response is
            parsed onto UnexpectedStatus.parsed. With the flag set to False, those statuses return
            None instead of raising.
        TypeError: If a response body matches none of the types the OpenAPI document declares for it.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[float | str]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def request(
    *,
    client: AuthenticatedClient | Client,
) -> float | str:
    """A union with a `number` member: JSON draws no int/float distinction, so an integer body is valid.

    Raises:
        errors.UnexpectedStatus: If the server returns a status code that is not a documented
            success and Client.raise_on_unexpected_status is True. A documented error response is
            parsed onto UnexpectedStatus.parsed. With the flag set to False, those statuses return
            None instead of raising.
        TypeError: If a response body matches none of the types the OpenAPI document declares for it.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        float | str
    """

    return (
        await _request_detailed(
            client=client,
        )
    ).parsed
