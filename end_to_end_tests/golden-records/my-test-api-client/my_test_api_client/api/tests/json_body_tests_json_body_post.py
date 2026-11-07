from http import HTTPStatus as _HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient as _AuthenticatedClient
from ...client import Client as _Client
from ...models.a_model import AModel
from ...models.http_validation_error import HTTPValidationError
from ...types import Response as _Response


def _get_kwargs(
    *,
    body: AModel,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/tests/json_body",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: _AuthenticatedClient | _Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = response.json()
        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: _AuthenticatedClient | _Client, response: httpx.Response
) -> _Response[Any | HTTPValidationError]:
    return _Response(
        status_code=_HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: _AuthenticatedClient | _Client,
    body: AModel,
) -> _Response[Any | HTTPValidationError]:
    """Json Body

     Try sending a JSON body

    Args:
        body (AModel): A Model for testing all the ways custom objects can be used

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: _AuthenticatedClient | _Client,
    body: AModel,
) -> Any | HTTPValidationError | None:
    """Json Body

     Try sending a JSON body

    Args:
        body (AModel): A Model for testing all the ways custom objects can be used

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: _AuthenticatedClient | _Client,
    body: AModel,
) -> _Response[Any | HTTPValidationError]:
    """Json Body

     Try sending a JSON body

    Args:
        body (AModel): A Model for testing all the ways custom objects can be used

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: _AuthenticatedClient | _Client,
    body: AModel,
) -> Any | HTTPValidationError | None:
    """Json Body

     Try sending a JSON body

    Args:
        body (AModel): A Model for testing all the ways custom objects can be used

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
