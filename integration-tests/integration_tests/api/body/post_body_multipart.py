from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_body_multipart_body import PostBodyMultipartBody
from ...models.post_body_multipart_response_200 import PostBodyMultipartResponse200
from ...models.public_error import PublicError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: PostBodyMultipartBody | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/body/multipart",
    }

    if not isinstance(body, Unset):
        _kwargs["files"] = body.to_multipart()

    headers["Content-Type"] = "multipart/form-data; boundary=+++"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> PostBodyMultipartResponse200:
    if response.status_code == 200:
        response_200 = PostBodyMultipartResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        if client.raise_on_unexpected_status:
            response_400: PublicError | None = None
            try:
                response_400 = PublicError.from_dict(response.json())
            except Exception:
                pass
            raise errors.UnexpectedStatus(
                response.status_code,
                response.content,
                parsed=response_400,
            )

        return cast(PostBodyMultipartResponse200, None)

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return cast(PostBodyMultipartResponse200, None)


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostBodyMultipartResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


async def _request_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostBodyMultipartBody | Unset = UNSET,
) -> Response[PostBodyMultipartResponse200]:
    """
    Args:
        body (PostBodyMultipartBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns a status code that is not a documented
            success and Client.raise_on_unexpected_status is True. A documented error response is
            parsed onto UnexpectedStatus.parsed. With the flag set to False, those statuses return
            None instead of raising.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostBodyMultipartResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def request(
    *,
    client: AuthenticatedClient | Client,
    body: PostBodyMultipartBody | Unset = UNSET,
) -> PostBodyMultipartResponse200:
    """
    Args:
        body (PostBodyMultipartBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns a status code that is not a documented
            success and Client.raise_on_unexpected_status is True. A documented error response is
            parsed onto UnexpectedStatus.parsed. With the flag set to False, those statuses return
            None instead of raising.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostBodyMultipartResponse200
    """

    return (
        await _request_detailed(
            client=client,
            body=body,
        )
    ).parsed
