from http import HTTPStatus as _HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient as _AuthenticatedClient
from ...client import Client as _Client
from ...models.mixed_case_response_200 import MixedCaseResponse200
from ...types import UNSET
from ...types import Response as _Response


def _get_kwargs(
    *,
    mixed_case: str,
    mixedCase: str,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["mixed_case"] = mixed_case

    params["mixedCase"] = mixedCase

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/naming/mixed-case",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: _AuthenticatedClient | _Client, response: httpx.Response) -> MixedCaseResponse200 | None:
    if response.status_code == 200:
        response_200 = MixedCaseResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: _AuthenticatedClient | _Client, response: httpx.Response
) -> _Response[MixedCaseResponse200]:
    return _Response(
        status_code=_HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: _AuthenticatedClient | _Client,
    mixed_case: str,
    mixedCase: str,
) -> _Response[MixedCaseResponse200]:
    """
    Args:
        mixed_case (str):
        mixedCase (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MixedCaseResponse200]
    """

    kwargs = _get_kwargs(
        mixed_case=mixed_case,
        mixedCase=mixedCase,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: _AuthenticatedClient | _Client,
    mixed_case: str,
    mixedCase: str,
) -> MixedCaseResponse200 | None:
    """
    Args:
        mixed_case (str):
        mixedCase (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MixedCaseResponse200
    """

    return sync_detailed(
        client=client,
        mixed_case=mixed_case,
        mixedCase=mixedCase,
    ).parsed


async def asyncio_detailed(
    *,
    client: _AuthenticatedClient | _Client,
    mixed_case: str,
    mixedCase: str,
) -> _Response[MixedCaseResponse200]:
    """
    Args:
        mixed_case (str):
        mixedCase (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MixedCaseResponse200]
    """

    kwargs = _get_kwargs(
        mixed_case=mixed_case,
        mixedCase=mixedCase,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: _AuthenticatedClient | _Client,
    mixed_case: str,
    mixedCase: str,
) -> MixedCaseResponse200 | None:
    """
    Args:
        mixed_case (str):
        mixedCase (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MixedCaseResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            mixed_case=mixed_case,
            mixedCase=mixedCase,
        )
    ).parsed
