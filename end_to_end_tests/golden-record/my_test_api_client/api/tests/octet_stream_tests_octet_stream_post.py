from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.octet_stream_tests_octet_stream_post_response_200 import OctetStreamTestsOctetStreamPostResponse200
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    *,
    body: File | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/tests/octet_stream",
    }

    if not isinstance(body, Unset):
        _kwargs["content"] = body.payload
    headers["Content-Type"] = "application/octet-stream"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> OctetStreamTestsOctetStreamPostResponse200:
    if response.status_code == 200:
        response_200 = OctetStreamTestsOctetStreamPostResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        if client.raise_on_unexpected_status:
            response_422 = HTTPValidationError.from_dict(response.json())

            raise errors.UnexpectedStatus(
                response.status_code,
                response.content,
                parsed=response_422,
            )

        return cast(OctetStreamTestsOctetStreamPostResponse200, None)

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return cast(OctetStreamTestsOctetStreamPostResponse200, None)


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[OctetStreamTestsOctetStreamPostResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


async def _request_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: File | Unset = UNSET,
) -> Response[OctetStreamTestsOctetStreamPostResponse200]:
    """Binary (octet stream) request body

    Args:
        body (File | Unset): A file to upload

    Raises:
        errors.UnexpectedStatus: If the server returns a status code that is not a documented
            success and Client.raise_on_unexpected_status is True. A documented error response is
            parsed onto UnexpectedStatus.parsed. With the flag set to False, those statuses return
            None instead of raising.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OctetStreamTestsOctetStreamPostResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def request(
    *,
    client: AuthenticatedClient | Client,
    body: File | Unset = UNSET,
) -> OctetStreamTestsOctetStreamPostResponse200:
    """Binary (octet stream) request body

    Args:
        body (File | Unset): A file to upload

    Raises:
        errors.UnexpectedStatus: If the server returns a status code that is not a documented
            success and Client.raise_on_unexpected_status is True. A documented error response is
            parsed onto UnexpectedStatus.parsed. With the flag set to False, those statuses return
            None instead of raising.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OctetStreamTestsOctetStreamPostResponse200
    """

    return (
        await _request_detailed(
            client=client,
            body=body,
        )
    ).parsed
