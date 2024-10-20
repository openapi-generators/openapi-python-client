from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_bodies_multiple_data_body import PostBodiesMultipleDataBody
from ...models.post_bodies_multiple_files_body import PostBodiesMultipleFilesBody
from ...models.post_bodies_multiple_json_body import PostBodiesMultipleJsonBody
from ...types import File, Response


def _get_kwargs(
    *,
    body: Union[
        PostBodiesMultipleJsonBody,
        File,
        PostBodiesMultipleDataBody,
        PostBodiesMultipleFilesBody,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/bodies/multiple",
    }

    if isinstance(body, PostBodiesMultipleJsonBody):
        _json_body = body.to_dict()

        _kwargs["json"] = _json_body
        headers["Content-Type"] = "application/json"
    if isinstance(body, File):
        _content_body = body.payload

        _kwargs["content"] = _content_body
        headers["Content-Type"] = "application/octet-stream"
    if isinstance(body, PostBodiesMultipleDataBody):
        _data_body = body.to_dict()

        _kwargs["data"] = _data_body
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, PostBodiesMultipleFilesBody):
        _files_body = body.to_multipart()

        _kwargs["files"] = _files_body
        headers["Content-Type"] = "multipart/form-data"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == 200:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        PostBodiesMultipleJsonBody,
        File,
        PostBodiesMultipleDataBody,
        PostBodiesMultipleFilesBody,
    ],
) -> Response[Any]:
    """Test multiple bodies

    Args:
        body (PostBodiesMultipleJsonBody):
        body (File):
        body (PostBodiesMultipleDataBody):
        body (PostBodiesMultipleFilesBody):

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
    client: Union[AuthenticatedClient, Client],
    body: Union[
        PostBodiesMultipleJsonBody,
        File,
        PostBodiesMultipleDataBody,
        PostBodiesMultipleFilesBody,
    ],
) -> Response[Any]:
    """Test multiple bodies

    Args:
        body (PostBodiesMultipleJsonBody):
        body (File):
        body (PostBodiesMultipleDataBody):
        body (PostBodiesMultipleFilesBody):

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
