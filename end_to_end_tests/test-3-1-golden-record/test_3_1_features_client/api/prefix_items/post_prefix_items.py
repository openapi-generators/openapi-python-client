from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_prefix_items_body import PostPrefixItemsBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: PostPrefixItemsBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/prefixItems",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> str | None:
    if response.status_code == 200:
        response_200 = cast(str, response.json())
        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPrefixItemsBody,
    headers: dict[str, str] | None = None,
    timeout: httpx.Timeout | None | Unset = UNSET,
    auth: httpx.Auth | None | Unset = UNSET,
) -> Response[str]:
    """
    Args:
        body (PostPrefixItemsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        body=body,
    )
    if headers is not None:
        kwargs["headers"] = {**kwargs.get("headers", {}), **headers}
    if not isinstance(timeout, Unset):
        kwargs["timeout"] = timeout
    if not isinstance(auth, Unset):
        kwargs["auth"] = auth

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: PostPrefixItemsBody,
    headers: dict[str, str] | None = None,
    timeout: httpx.Timeout | None | Unset = UNSET,
    auth: httpx.Auth | None | Unset = UNSET,
) -> str | None:
    """
    Args:
        body (PostPrefixItemsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        str
    """

    return sync_detailed(
        client=client,
        body=body,
        headers=headers,
        timeout=timeout,
        auth=auth,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPrefixItemsBody,
    headers: dict[str, str] | None = None,
    timeout: httpx.Timeout | None | Unset = UNSET,
    auth: httpx.Auth | None | Unset = UNSET,
) -> Response[str]:
    """
    Args:
        body (PostPrefixItemsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        body=body,
    )
    if headers is not None:
        kwargs["headers"] = {**kwargs.get("headers", {}), **headers}
    if not isinstance(timeout, Unset):
        kwargs["timeout"] = timeout
    if not isinstance(auth, Unset):
        kwargs["auth"] = auth

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: PostPrefixItemsBody,
    headers: dict[str, str] | None = None,
    timeout: httpx.Timeout | None | Unset = UNSET,
    auth: httpx.Auth | None | Unset = UNSET,
) -> str | None:
    """
    Args:
        body (PostPrefixItemsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        str
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            headers=headers,
            timeout=timeout,
            auth=auth,
        )
    ).parsed
