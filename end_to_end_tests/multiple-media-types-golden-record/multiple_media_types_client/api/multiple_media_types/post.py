from http import HTTPStatus
from typing import Any, Literal, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ErrorResponse, Literal["Why have a fixed response? I dunno"]]]:
    if response.status_code == 200:
        response_200: Union[Literal["Why have a fixed response? I dunno"], Any]
        if response.headers.get("content-type") == "application/json":
            response_200 = cast(Literal["Why have a fixed response? I dunno"], response.json())
            if response_200 != "Why have a fixed response? I dunno":
                raise ValueError(
                    f"response_200 must match const 'Why have a fixed response? I dunno', got '{response_200}'"
                )
            return response_200
        if response.headers.get("content-type") == "application/octet-stream":
            response_200 = cast(Any, response.content)
            return response_200
    if response.status_code == 404:
        response_404: Any
        if response.headers.get("content-type") == "text/plain":
            response_404 = cast(Any, response.text)
            return response_404
    if response.status_code == 503:
        response_503: Union[ErrorResponse, Any]
        if response.headers.get("content-type") == "application/json":
            response_503 = ErrorResponse.from_dict(response.json())

            return response_503
        if response.headers.get("content-type") == "text/plain":
            response_503 = cast(Any, response.text)
            return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, ErrorResponse, Literal["Why have a fixed response? I dunno"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, ErrorResponse, Literal["Why have a fixed response? I dunno"]]]:
    """
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse, Literal['Why have a fixed response? I dunno']]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, ErrorResponse, Literal["Why have a fixed response? I dunno"]]]:
    """
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse, Literal['Why have a fixed response? I dunno']]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, ErrorResponse, Literal["Why have a fixed response? I dunno"]]]:
    """
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse, Literal['Why have a fixed response? I dunno']]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, ErrorResponse, Literal["Why have a fixed response? I dunno"]]]:
    """
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse, Literal['Why have a fixed response? I dunno']]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
