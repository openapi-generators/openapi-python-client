from http import HTTPStatus
from typing import Any, Optional, Union

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
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[PostParametersHeaderResponse200, PublicError]]:
    if response.status_code == 200:
        response_200 = PostParametersHeaderResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = PublicError.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[PostParametersHeaderResponse200, PublicError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    boolean_header: bool,
    string_header: str,
    number_header: float,
    integer_header: int,
) -> Response[Union[PostParametersHeaderResponse200, PublicError]]:
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
        Response[Union[PostParametersHeaderResponse200, PublicError]]
    """

    kwargs = _get_kwargs(
        boolean_header=boolean_header,
        string_header=string_header,
        number_header=number_header,
        integer_header=integer_header,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    boolean_header: bool,
    string_header: str,
    number_header: float,
    integer_header: int,
) -> Optional[Union[PostParametersHeaderResponse200, PublicError]]:
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
        Union[PostParametersHeaderResponse200, PublicError]
    """

    return sync_detailed(
        client=client,
        boolean_header=boolean_header,
        string_header=string_header,
        number_header=number_header,
        integer_header=integer_header,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    boolean_header: bool,
    string_header: str,
    number_header: float,
    integer_header: int,
) -> Response[Union[PostParametersHeaderResponse200, PublicError]]:
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
        Response[Union[PostParametersHeaderResponse200, PublicError]]
    """

    kwargs = _get_kwargs(
        boolean_header=boolean_header,
        string_header=string_header,
        number_header=number_header,
        integer_header=integer_header,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    boolean_header: bool,
    string_header: str,
    number_header: float,
    integer_header: int,
) -> Optional[Union[PostParametersHeaderResponse200, PublicError]]:
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
        Union[PostParametersHeaderResponse200, PublicError]
    """

    return (
        await asyncio_detailed(
            client=client,
            boolean_header=boolean_header,
            string_header=string_header,
            number_header=number_header,
            integer_header=integer_header,
        )
    ).parsed
