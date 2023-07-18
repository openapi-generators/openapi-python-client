from http import HTTPStatus
from typing import Any, Dict

import httpx

from ... import errors
from ...client import Client
from ...models.post_responses_unions_simple_before_complex_response_200 import (
    PostResponsesUnionsSimpleBeforeComplexResponse200,
)
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/responses/unions/simple_before_complex".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(*, response: httpx.Response) -> PostResponsesUnionsSimpleBeforeComplexResponse200:
    if response.status_code == HTTPStatus.OK:
        response_200 = PostResponsesUnionsSimpleBeforeComplexResponse200.from_dict(response.json())

        return response_200
    response.raise_for_status()
    raise errors.UnexpectedStatus(response.status_code, response.content)


def _build_response(*, response: httpx.Response) -> Response[PostResponsesUnionsSimpleBeforeComplexResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[PostResponsesUnionsSimpleBeforeComplexResponse200]:
    """Regression test for #603

    Raises:
        httpx.HTTPStatusError: If the server returns an error status code.
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostResponsesUnionsSimpleBeforeComplexResponse200]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
) -> PostResponsesUnionsSimpleBeforeComplexResponse200:
    """Regression test for #603

    Raises:
        httpx.HTTPStatusError: If the server returns an error status code.
        errors.UnexpectedStatus: If the server returns an undocumented status code.
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
        httpx.HTTPStatusError: If the server returns an error status code.
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostResponsesUnionsSimpleBeforeComplexResponse200]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
) -> PostResponsesUnionsSimpleBeforeComplexResponse200:
    """Regression test for #603

    Raises:
        httpx.HTTPStatusError: If the server returns an error status code.
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostResponsesUnionsSimpleBeforeComplexResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
