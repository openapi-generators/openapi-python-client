from http import HTTPStatus
from typing import Any, Dict

import httpx

from ... import errors
from ...client import Client
from ...models.post_form_data_inline_data import PostFormDataInlineData
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    form_data: PostFormDataInlineData,
) -> Dict[str, Any]:
    url = "{}/tests/post_form_data_inline".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "data": form_data.to_dict(),
    }


def _parse_response(*, response: httpx.Response) -> Any:
    if response.status_code == HTTPStatus.OK:
        response_200 = response.json()
        return response_200
    response.raise_for_status()
    raise errors.UnexpectedStatus(response.status_code, response.content)


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    form_data: PostFormDataInlineData,
) -> Response[Any]:
    """Post form data (inline schema)

     Post form data (inline schema)

    Raises:
        httpx.HTTPStatusError: If the server returns an error status code.
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        form_data=form_data,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    form_data: PostFormDataInlineData,
) -> Any:
    """Post form data (inline schema)

     Post form data (inline schema)

    Raises:
        httpx.HTTPStatusError: If the server returns an error status code.
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any
    """

    return sync_detailed(
        client=client,
        form_data=form_data,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    form_data: PostFormDataInlineData,
) -> Response[Any]:
    """Post form data (inline schema)

     Post form data (inline schema)

    Raises:
        httpx.HTTPStatusError: If the server returns an error status code.
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        form_data=form_data,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    form_data: PostFormDataInlineData,
) -> Any:
    """Post form data (inline schema)

     Post form data (inline schema)

    Raises:
        httpx.HTTPStatusError: If the server returns an error status code.
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any
    """

    return (
        await asyncio_detailed(
            client=client,
            form_data=form_data,
        )
    ).parsed
