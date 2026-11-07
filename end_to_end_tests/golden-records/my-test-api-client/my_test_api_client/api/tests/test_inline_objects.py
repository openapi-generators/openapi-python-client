from http import HTTPStatus as _HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient as _AuthenticatedClient
from ...client import Client as _Client
from ...models.test_inline_objects_body import TestInlineObjectsBody
from ...models.test_inline_objects_response_200 import TestInlineObjectsResponse200
from ...types import Response as _Response


def _get_kwargs(
    *,
    body: TestInlineObjectsBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/tests/inline_objects",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: _AuthenticatedClient | _Client, response: httpx.Response
) -> TestInlineObjectsResponse200 | None:
    if response.status_code == 200:
        response_200 = TestInlineObjectsResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: _AuthenticatedClient | _Client, response: httpx.Response
) -> _Response[TestInlineObjectsResponse200]:
    return _Response(
        status_code=_HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: _AuthenticatedClient | _Client,
    body: TestInlineObjectsBody,
) -> _Response[TestInlineObjectsResponse200]:
    """Test Inline Objects

    Args:
        body (TestInlineObjectsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TestInlineObjectsResponse200]
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
    body: TestInlineObjectsBody,
) -> TestInlineObjectsResponse200 | None:
    """Test Inline Objects

    Args:
        body (TestInlineObjectsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TestInlineObjectsResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: _AuthenticatedClient | _Client,
    body: TestInlineObjectsBody,
) -> _Response[TestInlineObjectsResponse200]:
    """Test Inline Objects

    Args:
        body (TestInlineObjectsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TestInlineObjectsResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: _AuthenticatedClient | _Client,
    body: TestInlineObjectsBody,
) -> TestInlineObjectsResponse200 | None:
    """Test Inline Objects

    Args:
        body (TestInlineObjectsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TestInlineObjectsResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
