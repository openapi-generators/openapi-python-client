from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.a_model import AModel
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: AModel,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/tests/json_body",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = response.json()
        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AModel,
    headers: dict[str, str] | None = None,
    timeout: httpx.Timeout | None | Unset = UNSET,
    auth: httpx.Auth | None | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    """Json Body

     Try sending a JSON body

    Args:
        body (AModel): A Model for testing all the ways custom objects can be used

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
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
    body: AModel,
    headers: dict[str, str] | None = None,
    timeout: httpx.Timeout | None | Unset = UNSET,
    auth: httpx.Auth | None | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    """Json Body

     Try sending a JSON body

    Args:
        body (AModel): A Model for testing all the ways custom objects can be used

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
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
    body: AModel,
    headers: dict[str, str] | None = None,
    timeout: httpx.Timeout | None | Unset = UNSET,
    auth: httpx.Auth | None | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    """Json Body

     Try sending a JSON body

    Args:
        body (AModel): A Model for testing all the ways custom objects can be used

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
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
    body: AModel,
    headers: dict[str, str] | None = None,
    timeout: httpx.Timeout | None | Unset = UNSET,
    auth: httpx.Auth | None | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    """Json Body

     Try sending a JSON body

    Args:
        body (AModel): A Model for testing all the ways custom objects can be used

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
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
