from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_naming_property_conflict_with_import_body import PostNamingPropertyConflictWithImportBody
from ...models.post_naming_property_conflict_with_import_response_200 import (
    PostNamingPropertyConflictWithImportResponse200,
)
from ...types import UNSET, Response, Unset, dump_json__for_transport


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
        _kwargs["content"] = dump_json__for_transport(body)

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostNamingPropertyConflictWithImportResponse200:
    if response.status_code == 200:
        response_200 = PostNamingPropertyConflictWithImportResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return cast(PostNamingPropertyConflictWithImportResponse200, None)


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostNamingPropertyConflictWithImportResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


async def _request_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostNamingPropertyConflictWithImportBody | Unset = UNSET,
) -> Response[PostNamingPropertyConflictWithImportResponse200]:
    """
    Args:
        body (PostNamingPropertyConflictWithImportBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns a status code that is not a documented
            success and Client.raise_on_unexpected_status is True. A documented error response is
            parsed onto UnexpectedStatus.parsed. With the flag set to False, those statuses return
            None instead of raising.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostNamingPropertyConflictWithImportResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def request(
    *,
    client: AuthenticatedClient | Client,
    body: PostNamingPropertyConflictWithImportBody | Unset = UNSET,
) -> PostNamingPropertyConflictWithImportResponse200:
    """
    Args:
        body (PostNamingPropertyConflictWithImportBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns a status code that is not a documented
            success and Client.raise_on_unexpected_status is True. A documented error response is
            parsed onto UnexpectedStatus.parsed. With the flag set to False, those statuses return
            None instead of raising.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostNamingPropertyConflictWithImportResponse200
    """

    return (
        await _request_detailed(
            client=client,
            body=body,
        )
    ).parsed
