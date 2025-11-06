from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_bodies_multiple_data_body import PostBodiesMultipleDataBody
from ...models.post_bodies_multiple_files_body import PostBodiesMultipleFilesBody
from ...models.post_bodies_multiple_json_body import PostBodiesMultipleJsonBody
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    *,
    body: PostBodiesMultipleJsonBody | File | PostBodiesMultipleDataBody | PostBodiesMultipleFilesBody | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/bodies/multiple",
    }

    if isinstance(body, PostBodiesMultipleJsonBody):
        if not isinstance(body, Unset):
            _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, File):
        if not isinstance(body, Unset):
            _kwargs["content"] = body.payload

        headers["Content-Type"] = "application/octet-stream"
    if isinstance(body, PostBodiesMultipleDataBody):
        if not isinstance(body, Unset):
            _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, PostBodiesMultipleFilesBody):
        if not isinstance(body, Unset):
            _kwargs["files"] = body.to_multipart()

        headers["Content-Type"] = "multipart/form-data"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | None:
    if response.status_code == 200:
        return None

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostBodiesMultipleJsonBody | File | PostBodiesMultipleDataBody | PostBodiesMultipleFilesBody | Unset = UNSET,
) -> Response[Any]:
    """Test multiple bodies

    Args:
        body (PostBodiesMultipleJsonBody | Unset):
        body (File | Unset):
        body (PostBodiesMultipleDataBody | Unset):
        body (PostBodiesMultipleFilesBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostBodiesMultipleJsonBody | File | PostBodiesMultipleDataBody | PostBodiesMultipleFilesBody | Unset = UNSET,
) -> Response[Any]:
    """Test multiple bodies

    Args:
        body (PostBodiesMultipleJsonBody | Unset):
        body (File | Unset):
        body (PostBodiesMultipleDataBody | Unset):
        body (PostBodiesMultipleFilesBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
