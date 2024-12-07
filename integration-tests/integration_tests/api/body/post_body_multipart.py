from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_body_multipart_body import PostBodyMultipartBody
from ...models.post_body_multipart_response_200 import PostBodyMultipartResponse200
from ...models.public_error import PublicError
from ...types import Response


def _get_kwargs(
    *,
    body: PostBodyMultipartBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/body/multipart",
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[PostBodyMultipartResponse200, PublicError]]:
    if response.status_code == 200:
        response_200 = PostBodyMultipartResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = PublicError.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[PostBodyMultipartResponse200, PublicError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: PostBodyMultipartBody,
) -> Response[Union[PostBodyMultipartResponse200, PublicError]]:
    """
    Args:
        body (PostBodyMultipartBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[PostBodyMultipartResponse200, PublicError]]
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
    client: Union[AuthenticatedClient, Client],
    body: PostBodyMultipartBody,
) -> Optional[Union[PostBodyMultipartResponse200, PublicError]]:
    """
    Args:
        body (PostBodyMultipartBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[PostBodyMultipartResponse200, PublicError]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: PostBodyMultipartBody,
) -> Response[Union[PostBodyMultipartResponse200, PublicError]]:
    """
    Args:
        body (PostBodyMultipartBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[PostBodyMultipartResponse200, PublicError]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: PostBodyMultipartBody,
) -> Optional[Union[PostBodyMultipartResponse200, PublicError]]:
    """
    Args:
        body (PostBodyMultipartBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[PostBodyMultipartResponse200, PublicError]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
