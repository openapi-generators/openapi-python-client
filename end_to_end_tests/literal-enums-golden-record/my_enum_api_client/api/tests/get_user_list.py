from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.a_model import AModel
from ...models.an_enum import AnEnum
from ...models.an_enum_with_null import AnEnumWithNull
from ...models.get_user_list_int_enum_header import GetUserListIntEnumHeader
from ...models.get_user_list_string_enum_header import (
    GetUserListStringEnumHeader,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    an_enum_value: list[AnEnum],
    an_enum_value_with_null: list[Union[AnEnumWithNull, None]],
    an_enum_value_with_only_null: list[None],
    int_enum_header: Union[Unset, GetUserListIntEnumHeader] = UNSET,
    string_enum_header: Union[Unset, GetUserListStringEnumHeader] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(int_enum_header, Unset):
        headers["Int-Enum-Header"] = str(int_enum_header)

    if not isinstance(string_enum_header, Unset):
        headers["String-Enum-Header"] = str(string_enum_header)

    params: dict[str, Any] = {}

    json_an_enum_value = []
    for an_enum_value_item_data in an_enum_value:
        an_enum_value_item: str = an_enum_value_item_data
        json_an_enum_value.append(an_enum_value_item)

    params["an_enum_value"] = json_an_enum_value

    json_an_enum_value_with_null = []
    for an_enum_value_with_null_item_data in an_enum_value_with_null:
        an_enum_value_with_null_item: Union[None, str]
        if isinstance(an_enum_value_with_null_item_data, str):
            an_enum_value_with_null_item = an_enum_value_with_null_item_data
        else:
            an_enum_value_with_null_item = an_enum_value_with_null_item_data
        json_an_enum_value_with_null.append(an_enum_value_with_null_item)

    params["an_enum_value_with_null"] = json_an_enum_value_with_null

    json_an_enum_value_with_only_null = an_enum_value_with_only_null

    params["an_enum_value_with_only_null"] = json_an_enum_value_with_only_null

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/tests/",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["AModel"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AModel.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["AModel"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    an_enum_value: list[AnEnum],
    an_enum_value_with_null: list[Union[AnEnumWithNull, None]],
    an_enum_value_with_only_null: list[None],
    int_enum_header: Union[Unset, GetUserListIntEnumHeader] = UNSET,
    string_enum_header: Union[Unset, GetUserListStringEnumHeader] = UNSET,
) -> Response[list["AModel"]]:
    """Get List

     Get a list of things

    Args:
        an_enum_value (list[AnEnum]):
        an_enum_value_with_null (list[Union[AnEnumWithNull, None]]):
        an_enum_value_with_only_null (list[None]):
        int_enum_header (Union[Unset, GetUserListIntEnumHeader]):
        string_enum_header (Union[Unset, GetUserListStringEnumHeader]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AModel']]
    """

    kwargs = _get_kwargs(
        an_enum_value=an_enum_value,
        an_enum_value_with_null=an_enum_value_with_null,
        an_enum_value_with_only_null=an_enum_value_with_only_null,
        int_enum_header=int_enum_header,
        string_enum_header=string_enum_header,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    an_enum_value: list[AnEnum],
    an_enum_value_with_null: list[Union[AnEnumWithNull, None]],
    an_enum_value_with_only_null: list[None],
    int_enum_header: Union[Unset, GetUserListIntEnumHeader] = UNSET,
    string_enum_header: Union[Unset, GetUserListStringEnumHeader] = UNSET,
) -> Optional[list["AModel"]]:
    """Get List

     Get a list of things

    Args:
        an_enum_value (list[AnEnum]):
        an_enum_value_with_null (list[Union[AnEnumWithNull, None]]):
        an_enum_value_with_only_null (list[None]):
        int_enum_header (Union[Unset, GetUserListIntEnumHeader]):
        string_enum_header (Union[Unset, GetUserListStringEnumHeader]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AModel']
    """

    return sync_detailed(
        client=client,
        an_enum_value=an_enum_value,
        an_enum_value_with_null=an_enum_value_with_null,
        an_enum_value_with_only_null=an_enum_value_with_only_null,
        int_enum_header=int_enum_header,
        string_enum_header=string_enum_header,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    an_enum_value: list[AnEnum],
    an_enum_value_with_null: list[Union[AnEnumWithNull, None]],
    an_enum_value_with_only_null: list[None],
    int_enum_header: Union[Unset, GetUserListIntEnumHeader] = UNSET,
    string_enum_header: Union[Unset, GetUserListStringEnumHeader] = UNSET,
) -> Response[list["AModel"]]:
    """Get List

     Get a list of things

    Args:
        an_enum_value (list[AnEnum]):
        an_enum_value_with_null (list[Union[AnEnumWithNull, None]]):
        an_enum_value_with_only_null (list[None]):
        int_enum_header (Union[Unset, GetUserListIntEnumHeader]):
        string_enum_header (Union[Unset, GetUserListStringEnumHeader]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AModel']]
    """

    kwargs = _get_kwargs(
        an_enum_value=an_enum_value,
        an_enum_value_with_null=an_enum_value_with_null,
        an_enum_value_with_only_null=an_enum_value_with_only_null,
        int_enum_header=int_enum_header,
        string_enum_header=string_enum_header,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    an_enum_value: list[AnEnum],
    an_enum_value_with_null: list[Union[AnEnumWithNull, None]],
    an_enum_value_with_only_null: list[None],
    int_enum_header: Union[Unset, GetUserListIntEnumHeader] = UNSET,
    string_enum_header: Union[Unset, GetUserListStringEnumHeader] = UNSET,
) -> Optional[list["AModel"]]:
    """Get List

     Get a list of things

    Args:
        an_enum_value (list[AnEnum]):
        an_enum_value_with_null (list[Union[AnEnumWithNull, None]]):
        an_enum_value_with_only_null (list[None]):
        int_enum_header (Union[Unset, GetUserListIntEnumHeader]):
        string_enum_header (Union[Unset, GetUserListStringEnumHeader]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AModel']
    """

    return (
        await asyncio_detailed(
            client=client,
            an_enum_value=an_enum_value,
            an_enum_value_with_null=an_enum_value_with_null,
            an_enum_value_with_only_null=an_enum_value_with_only_null,
            int_enum_header=int_enum_header,
            string_enum_header=string_enum_header,
        )
    ).parsed
