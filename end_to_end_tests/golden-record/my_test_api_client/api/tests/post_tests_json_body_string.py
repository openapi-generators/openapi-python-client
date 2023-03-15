from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: str,
) -> Dict[str, Any]:
    url = "{}/tests/json_body/string".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[HTTPValidationError, str]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(str, response.json())
        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        if client.raise_on_error_status:
            raise errors.ExpectedErrorStatus(f"Failed status code: {response.status_code}")
        return response_422
    if response.status_code >= 400:
        if client.raise_on_unexpected_status or client.raise_on_error_status:
            raise errors.UnexpectedErrorStatus(f"Unexpected status code: {response.status_code}")
    else:
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedSuccessStatus(f"Unexpected status code: {response.status_code}")
    return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[HTTPValidationError, str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: str,
) -> Response[Union[HTTPValidationError, str]]:
    """Json Body Which is String

    Args:
        json_body (str):

    Raises:
        errors.ErrorStatus: If the server returns an error status code and Client.raise_on_error_status is True.
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, str]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    json_body: str,
) -> Optional[Union[HTTPValidationError, str]]:
    """Json Body Which is String

    Args:
        json_body (str):

    Raises:
        errors.ErrorStatus: If the server returns an error status code and Client.raise_on_error_status is True.
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, str]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: str,
) -> Response[Union[HTTPValidationError, str]]:
    """Json Body Which is String

    Args:
        json_body (str):

    Raises:
        errors.ErrorStatus: If the server returns an error status code and Client.raise_on_error_status is True.
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, str]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    json_body: str,
) -> Optional[Union[HTTPValidationError, str]]:
    """Json Body Which is String

    Args:
        json_body (str):

    Raises:
        errors.ErrorStatus: If the server returns an error status code and Client.raise_on_error_status is True.
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, str]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
