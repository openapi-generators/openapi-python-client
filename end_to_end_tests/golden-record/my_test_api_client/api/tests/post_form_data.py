from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.a_form_data import AFormData
from ...types import Response


def _get_kwargs(
    *,
    body: AFormData,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/tests/post_form_data",
    }

    _kwargs["data"] = body.to_dict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> None:
    response.raise_for_status()
    if response.status_code == 200:
        return None

    raise errors.UnexpectedStatus(response.status_code, response.content)


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
    body: AFormData,
) -> Response[None]:
    """Post form data

     Post form data

    Args:
        body (AFormData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
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
    body: AFormData,
) -> None:
    """Post form data

     Post form data

    Args:
        body (AFormData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        None
    """

    await _request_detailed(
        client=client,
        body=body,
    )
