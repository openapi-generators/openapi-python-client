from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_models_allof_response_200 import GetModelsAllofResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/models/allof",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetModelsAllofResponse200 | None:
    if response.status_code == 200:
        response_200 = GetModelsAllofResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetModelsAllofResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    headers: dict[str, str] | None = None,
    timeout: httpx.Timeout | None | Unset = UNSET,
    auth: httpx.Auth | None | Unset = UNSET,
) -> Response[GetModelsAllofResponse200]:
    """
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetModelsAllofResponse200]
    """

    kwargs = _get_kwargs()
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
    headers: dict[str, str] | None = None,
    timeout: httpx.Timeout | None | Unset = UNSET,
    auth: httpx.Auth | None | Unset = UNSET,
) -> GetModelsAllofResponse200 | None:
    """
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetModelsAllofResponse200
    """

    return sync_detailed(
        client=client,
        headers=headers,
        timeout=timeout,
        auth=auth,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    headers: dict[str, str] | None = None,
    timeout: httpx.Timeout | None | Unset = UNSET,
    auth: httpx.Auth | None | Unset = UNSET,
) -> Response[GetModelsAllofResponse200]:
    """
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetModelsAllofResponse200]
    """

    kwargs = _get_kwargs()
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
    headers: dict[str, str] | None = None,
    timeout: httpx.Timeout | None | Unset = UNSET,
    auth: httpx.Auth | None | Unset = UNSET,
) -> GetModelsAllofResponse200 | None:
    """
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetModelsAllofResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            headers=headers,
            timeout=timeout,
            auth=auth,
        )
    ).parsed
