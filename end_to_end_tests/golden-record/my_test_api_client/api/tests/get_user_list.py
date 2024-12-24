import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.a_model import AModel
from ...models.an_enum import AnEnum
from ...models.an_enum_with_null import AnEnumWithNull
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(
    *,
    an_enum_value: list[AnEnum],
    an_enum_value_with_null: list[Union[AnEnumWithNull, None]],
    an_enum_value_with_only_null: list[None],
    some_date: Union[datetime.date, datetime.datetime],
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_an_enum_value = []
    for an_enum_value_item_data in an_enum_value:
        an_enum_value_item = an_enum_value_item_data.value
        json_an_enum_value.append(an_enum_value_item)

    params["an_enum_value"] = json_an_enum_value

    json_an_enum_value_with_null = []
    for an_enum_value_with_null_item_data in an_enum_value_with_null:
        an_enum_value_with_null_item: Union[None, str]
        if isinstance(an_enum_value_with_null_item_data, AnEnumWithNull):
            an_enum_value_with_null_item = an_enum_value_with_null_item_data.value
        else:
            an_enum_value_with_null_item = an_enum_value_with_null_item_data
        json_an_enum_value_with_null.append(an_enum_value_with_null_item)

    params["an_enum_value_with_null"] = json_an_enum_value_with_null

    json_an_enum_value_with_only_null = an_enum_value_with_only_null

    params["an_enum_value_with_only_null"] = json_an_enum_value_with_only_null

    json_some_date: str
    if isinstance(some_date, datetime.date):
        json_some_date = some_date.isoformat()
    else:
        json_some_date = some_date.isoformat()

    params["some_date"] = json_some_date

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/tests/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["AModel"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AModel.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if response.status_code == 423:
        response_423 = HTTPValidationError.from_dict(response.json())

        return response_423
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, list["AModel"]]]:
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
    some_date: Union[datetime.date, datetime.datetime],
) -> Response[Union[HTTPValidationError, list["AModel"]]]:
    """Get List

     Get a list of things

    Args:
        an_enum_value (list[AnEnum]):
        an_enum_value_with_null (list[Union[AnEnumWithNull, None]]):
        an_enum_value_with_only_null (list[None]):
        some_date (Union[datetime.date, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['AModel']]]
    """

    kwargs = _get_kwargs(
        an_enum_value=an_enum_value,
        an_enum_value_with_null=an_enum_value_with_null,
        an_enum_value_with_only_null=an_enum_value_with_only_null,
        some_date=some_date,
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
    some_date: Union[datetime.date, datetime.datetime],
) -> Optional[Union[HTTPValidationError, list["AModel"]]]:
    """Get List

     Get a list of things

    Args:
        an_enum_value (list[AnEnum]):
        an_enum_value_with_null (list[Union[AnEnumWithNull, None]]):
        an_enum_value_with_only_null (list[None]):
        some_date (Union[datetime.date, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['AModel']]
    """

    return sync_detailed(
        client=client,
        an_enum_value=an_enum_value,
        an_enum_value_with_null=an_enum_value_with_null,
        an_enum_value_with_only_null=an_enum_value_with_only_null,
        some_date=some_date,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    an_enum_value: list[AnEnum],
    an_enum_value_with_null: list[Union[AnEnumWithNull, None]],
    an_enum_value_with_only_null: list[None],
    some_date: Union[datetime.date, datetime.datetime],
) -> Response[Union[HTTPValidationError, list["AModel"]]]:
    """Get List

     Get a list of things

    Args:
        an_enum_value (list[AnEnum]):
        an_enum_value_with_null (list[Union[AnEnumWithNull, None]]):
        an_enum_value_with_only_null (list[None]):
        some_date (Union[datetime.date, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['AModel']]]
    """

    kwargs = _get_kwargs(
        an_enum_value=an_enum_value,
        an_enum_value_with_null=an_enum_value_with_null,
        an_enum_value_with_only_null=an_enum_value_with_only_null,
        some_date=some_date,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    an_enum_value: list[AnEnum],
    an_enum_value_with_null: list[Union[AnEnumWithNull, None]],
    an_enum_value_with_only_null: list[None],
    some_date: Union[datetime.date, datetime.datetime],
) -> Optional[Union[HTTPValidationError, list["AModel"]]]:
    """Get List

     Get a list of things

    Args:
        an_enum_value (list[AnEnum]):
        an_enum_value_with_null (list[Union[AnEnumWithNull, None]]):
        an_enum_value_with_only_null (list[None]):
        some_date (Union[datetime.date, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['AModel']]
    """

    return (
        await asyncio_detailed(
            client=client,
            an_enum_value=an_enum_value,
            an_enum_value_with_null=an_enum_value_with_null,
            an_enum_value_with_only_null=an_enum_value_with_only_null,
            some_date=some_date,
        )
    ).parsed
