from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_models_allof_response_200 import GetModelsAllofResponse200
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/models/allof",
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> GetModelsAllofResponse200:
    if response.status_code == 200:
        response_200 = GetModelsAllofResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return cast(GetModelsAllofResponse200, None)


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetModelsAllofResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


async def _request_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetModelsAllofResponse200]:
    """
    Raises:
        errors.UnexpectedStatus: If the server returns a status code that is not a documented
            success. A documented error response is parsed onto UnexpectedStatus.parsed. An
            undocumented status code raises only when Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetModelsAllofResponse200]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def request(
    *,
    client: AuthenticatedClient | Client,
) -> GetModelsAllofResponse200:
    """
    Raises:
        errors.UnexpectedStatus: If the server returns a status code that is not a documented
            success. A documented error response is parsed onto UnexpectedStatus.parsed. An
            undocumented status code raises only when Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetModelsAllofResponse200
    """

    return (
        await _request_detailed(
            client=client,
        )
    ).parsed
