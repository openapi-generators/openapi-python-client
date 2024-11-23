from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_location_header_types_int_enum_header import GetLocationHeaderTypesIntEnumHeader
from ...models.get_location_header_types_string_enum_header import GetLocationHeaderTypesStringEnumHeader
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    boolean_header: Union[Unset, bool] = UNSET,
    string_header: Union[Unset, str] = UNSET,
    number_header: Union[Unset, float] = UNSET,
    integer_header: Union[Unset, int] = UNSET,
    int_enum_header: Union[Unset, GetLocationHeaderTypesIntEnumHeader] = UNSET,
    string_enum_header: Union[Unset, GetLocationHeaderTypesStringEnumHeader] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(boolean_header, Unset):
        headers["Boolean-Header"] = "true" if boolean_header else "false"

    if not isinstance(string_header, Unset):
        headers["String-Header"] = string_header

    if not isinstance(number_header, Unset):
        headers["Number-Header"] = str(number_header)

    if not isinstance(integer_header, Unset):
        headers["Integer-Header"] = str(integer_header)

    if not isinstance(int_enum_header, Unset):
        headers["Int-Enum-Header"] = str(int_enum_header)

    if not isinstance(string_enum_header, Unset):
        headers["String-Enum-Header"] = str(string_enum_header)

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/location/header/types",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == 200:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    boolean_header: Union[Unset, bool] = UNSET,
    string_header: Union[Unset, str] = UNSET,
    number_header: Union[Unset, float] = UNSET,
    integer_header: Union[Unset, int] = UNSET,
    int_enum_header: Union[Unset, GetLocationHeaderTypesIntEnumHeader] = UNSET,
    string_enum_header: Union[Unset, GetLocationHeaderTypesStringEnumHeader] = UNSET,
) -> Response[Any]:
    """
    Args:
        boolean_header (Union[Unset, bool]):
        string_header (Union[Unset, str]):
        number_header (Union[Unset, float]):
        integer_header (Union[Unset, int]):
        int_enum_header (Union[Unset, GetLocationHeaderTypesIntEnumHeader]):
        string_enum_header (Union[Unset, GetLocationHeaderTypesStringEnumHeader]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        boolean_header=boolean_header,
        string_header=string_header,
        number_header=number_header,
        integer_header=integer_header,
        int_enum_header=int_enum_header,
        string_enum_header=string_enum_header,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    boolean_header: Union[Unset, bool] = UNSET,
    string_header: Union[Unset, str] = UNSET,
    number_header: Union[Unset, float] = UNSET,
    integer_header: Union[Unset, int] = UNSET,
    int_enum_header: Union[Unset, GetLocationHeaderTypesIntEnumHeader] = UNSET,
    string_enum_header: Union[Unset, GetLocationHeaderTypesStringEnumHeader] = UNSET,
) -> Response[Any]:
    """
    Args:
        boolean_header (Union[Unset, bool]):
        string_header (Union[Unset, str]):
        number_header (Union[Unset, float]):
        integer_header (Union[Unset, int]):
        int_enum_header (Union[Unset, GetLocationHeaderTypesIntEnumHeader]):
        string_enum_header (Union[Unset, GetLocationHeaderTypesStringEnumHeader]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        boolean_header=boolean_header,
        string_header=string_header,
        number_header=number_header,
        integer_header=integer_header,
        int_enum_header=int_enum_header,
        string_enum_header=string_enum_header,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
