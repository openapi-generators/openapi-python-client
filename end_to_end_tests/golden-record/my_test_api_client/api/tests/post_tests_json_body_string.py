from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    body: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/tests/json_body/string",
    }

    _kwargs["json"] = body

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> str:
    if response.status_code == 200:
        response_200 = cast(str, response.json())
        return response_200

    if response.status_code == 422:
        if client.raise_on_unexpected_status:
            response_422: HTTPValidationError | None = None
            try:
                response_422 = HTTPValidationError.from_dict(response.json())
            except Exception:
                pass
            raise errors.UnexpectedStatus(
                response.status_code,
                response.content,
                parsed=response_422,
            )

        return cast(str, None)

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return cast(str, None)


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
    body: str,
) -> Response[str]:
    """Json Body Which is String

    Args:
        body (str):

    Raises:
        errors.UnexpectedStatus: If the server returns a status code that is not a documented
            success and Client.raise_on_unexpected_status is True. A documented error response is
            parsed onto UnexpectedStatus.parsed. With the flag set to False, those statuses return
            None instead of raising.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def request(
    *,
    client: AuthenticatedClient | Client,
    body: str,
) -> str:
    """Json Body Which is String

    Args:
        body (str):

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
            body=body,
        )
    ).parsed
