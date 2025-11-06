from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_naming_property_conflict_with_import_body import PostNamingPropertyConflictWithImportBody
from ...models.post_naming_property_conflict_with_import_response_200 import (
    PostNamingPropertyConflictWithImportResponse200,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: PostNamingPropertyConflictWithImportBody | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/naming/property-conflict-with-import",
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostNamingPropertyConflictWithImportResponse200 | None:
    if response.status_code == 200:
        response_200 = PostNamingPropertyConflictWithImportResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostNamingPropertyConflictWithImportResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostNamingPropertyConflictWithImportBody | Unset = UNSET,
) -> Response[PostNamingPropertyConflictWithImportResponse200]:
    """
    Args:
        body (PostNamingPropertyConflictWithImportBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostNamingPropertyConflictWithImportResponse200]
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
    client: AuthenticatedClient | Client,
    body: PostNamingPropertyConflictWithImportBody | Unset = UNSET,
) -> PostNamingPropertyConflictWithImportResponse200 | None:
    """
    Args:
        body (PostNamingPropertyConflictWithImportBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostNamingPropertyConflictWithImportResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostNamingPropertyConflictWithImportBody | Unset = UNSET,
) -> Response[PostNamingPropertyConflictWithImportResponse200]:
    """
    Args:
        body (PostNamingPropertyConflictWithImportBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostNamingPropertyConflictWithImportResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: PostNamingPropertyConflictWithImportBody | Unset = UNSET,
) -> PostNamingPropertyConflictWithImportResponse200 | None:
    """
    Args:
        body (PostNamingPropertyConflictWithImportBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostNamingPropertyConflictWithImportResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
