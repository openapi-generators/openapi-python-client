from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.post_responses_unions_simple_before_complex_response_200 import (
    PostResponsesUnionsSimpleBeforeComplexResponse200,
)
from ...types import Response


def _get_kwargs() -> Dict[str, Any]:
    pass

    return {
        "method": "post",
        "url": "/responses/unions/simple_before_complex",
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[PostResponsesUnionsSimpleBeforeComplexResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PostResponsesUnionsSimpleBeforeComplexResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[PostResponsesUnionsSimpleBeforeComplexResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[PostResponsesUnionsSimpleBeforeComplexResponse200]:
    """Regression test for #603

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostResponsesUnionsSimpleBeforeComplexResponse200]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
) -> Optional[PostResponsesUnionsSimpleBeforeComplexResponse200]:
    """Regression test for #603

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostResponsesUnionsSimpleBeforeComplexResponse200
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[PostResponsesUnionsSimpleBeforeComplexResponse200]:
    """Regression test for #603

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostResponsesUnionsSimpleBeforeComplexResponse200]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
) -> Optional[PostResponsesUnionsSimpleBeforeComplexResponse200]:
    """Regression test for #603

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostResponsesUnionsSimpleBeforeComplexResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
