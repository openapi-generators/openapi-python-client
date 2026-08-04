from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_bodies_multiple_data_body import PostBodiesMultipleDataBody
from ...models.post_bodies_multiple_files_body import PostBodiesMultipleFilesBody
from ...models.post_bodies_multiple_json_body import PostBodiesMultipleJsonBody
from ...types import UNSET, File, Response, Unset, dump_dict__for_transport, dump_json__for_transport


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
            _kwargs["content"] = dump_json__for_transport(body)

        headers["Content-Type"] = "application/json"
    if isinstance(body, File):
        if not isinstance(body, Unset):
            _kwargs["content"] = body.payload
        headers["Content-Type"] = "application/octet-stream"
    if isinstance(body, PostBodiesMultipleDataBody):
        if not isinstance(body, Unset):
            _kwargs["data"] = dump_dict__for_transport(body)
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, PostBodiesMultipleFilesBody):
        if not isinstance(body, Unset):
            _kwargs["files"] = body.to_multipart()

        headers["Content-Type"] = "multipart/form-data; boundary=+++"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> None:
    if response.status_code == 200:
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
    body: PostBodiesMultipleJsonBody | File | PostBodiesMultipleDataBody | PostBodiesMultipleFilesBody | Unset = UNSET,
) -> Response[None]:
    """Test multiple bodies

    Args:
        body (PostBodiesMultipleJsonBody | Unset):
        body (File | Unset):
        body (PostBodiesMultipleDataBody | Unset):
        body (PostBodiesMultipleFilesBody | Unset):

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
    body: PostBodiesMultipleJsonBody | File | PostBodiesMultipleDataBody | PostBodiesMultipleFilesBody | Unset = UNSET,
) -> None:
    """Test multiple bodies

    Args:
        body (PostBodiesMultipleJsonBody | Unset):
        body (File | Unset):
        body (PostBodiesMultipleDataBody | Unset):
        body (PostBodiesMultipleFilesBody | Unset):

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
