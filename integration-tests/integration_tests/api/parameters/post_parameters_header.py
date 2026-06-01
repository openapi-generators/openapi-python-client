from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_parameters_header_response_200 import PostParametersHeaderResponse200
from ...models.public_error import PublicError
from ...types import Response


def _get_kwargs(
    *,
    boolean_header: bool,
    string_header: str,
    number_header: float,
    integer_header: int,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Boolean-Header"] = "true" if boolean_header else "false"

    headers["String-Header"] = string_header

    headers["Number-Header"] = str(number_header)

    headers["Integer-Header"] = str(integer_header)

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/parameters/header",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostParametersHeaderResponse200 | PublicError:
    response.raise_for_status()
    if response.status_code == 200:
        response_200 = PostParametersHeaderResponse200.from_dict(response.json())

        return response_200

    raise errors.UnexpectedStatus(response.status_code, response.content)


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostParametersHeaderResponse200 | PublicError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


async def _request_detailed(
    *,
    client: AuthenticatedClient | Client,
    boolean_header: bool,
    string_header: str,
    number_header: float,
    integer_header: int,
) -> Response[PostParametersHeaderResponse200 | PublicError]:
    """
    Args:
        boolean_header (bool):
        string_header (str):
        number_header (float):
        integer_header (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostParametersHeaderResponse200 | PublicError]
    """

    kwargs = _get_kwargs(
        boolean_header=boolean_header,
        string_header=string_header,
        number_header=number_header,
        integer_header=integer_header,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def request(
    *,
    client: AuthenticatedClient | Client,
    boolean_header: bool,
    string_header: str,
    number_header: float,
    integer_header: int,
) -> PostParametersHeaderResponse200 | PublicError:
    """
    Args:
        boolean_header (bool):
        string_header (str):
        number_header (float):
        integer_header (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostParametersHeaderResponse200 | PublicError
    """

    return (
        await _request_detailed(
            client=client,
            boolean_header=boolean_header,
            string_header=string_header,
            number_header=number_header,
            integer_header=integer_header,
        )
    ).parsed
