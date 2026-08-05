from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.a_model import AModel
from ...models.http_validation_error import HTTPValidationError
from ...types import Response, dump_json__for_transport


def _get_kwargs(
    *,
    body: AModel,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/tests/callback",
    }

    _kwargs["content"] = dump_json__for_transport(body)

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> None:
    if response.status_code == 200:
        return None

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

        return None

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[None]:
    # Called for the status check alone -- it raises on an undocumented code and has no
    # value to hand back.
    _parse_response(client=client, response=response)
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


async def _request_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AModel,
) -> Response[None]:
    """Path with callback

     Try sending a request related to a callback

    Args:
        body (AModel): A Model for testing all the ways custom objects can be used

    Raises:
        errors.UnexpectedStatus: If the server returns a status code that is not a documented
            success and Client.raise_on_unexpected_status is True. A documented error response is
            parsed onto UnexpectedStatus.parsed. With the flag set to False, those statuses return
            None instead of raising.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[None]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def request(
    *,
    client: AuthenticatedClient | Client,
    body: AModel,
) -> None:
    """Path with callback

     Try sending a request related to a callback

    Args:
        body (AModel): A Model for testing all the ways custom objects can be used

    Raises:
        errors.UnexpectedStatus: If the server returns a status code that is not a documented
            success and Client.raise_on_unexpected_status is True. A documented error response is
            parsed onto UnexpectedStatus.parsed. With the flag set to False, those statuses return
            None instead of raising.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        None
    """

    await _request_detailed(
        client=client,
        body=body,
    )
