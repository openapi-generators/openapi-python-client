import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx
from dateutil.parser import isoparse

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.an_enum import AnEnum
from ...models.http_validation_error import HTTPValidationError
from ...models.model_with_union_property import ModelWithUnionProperty
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    string_prop: str = "the default string",
    string_with_num: str = "1",
    date_prop: datetime.date = isoparse("1010-10-10").date(),
    float_prop: float = 3.14,
    float_with_int: float = 3.0,
    int_prop: int = 7,
    boolean_prop: bool = False,
    list_prop: list[AnEnum],
    union_prop: Union[float, str] = "not a float",
    union_prop_with_ref: Union[AnEnum, Unset, float] = 0.6,
    enum_prop: AnEnum,
    model_prop: "ModelWithUnionProperty",
    required_model_prop: "ModelWithUnionProperty",
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["string_prop"] = string_prop

    params["string with num"] = string_with_num

    json_date_prop = date_prop.isoformat()
    params["date_prop"] = json_date_prop

    params["float_prop"] = float_prop

    params["float_with_int"] = float_with_int

    params["int_prop"] = int_prop

    params["boolean_prop"] = boolean_prop

    json_list_prop = []
    for list_prop_item_data in list_prop:
        list_prop_item = list_prop_item_data.value
        json_list_prop.append(list_prop_item)

    params["list_prop"] = json_list_prop

    json_union_prop: Union[float, str]
    json_union_prop = union_prop
    params["union_prop"] = json_union_prop

    json_union_prop_with_ref: Union[Unset, float, str]
    if isinstance(union_prop_with_ref, Unset):
        json_union_prop_with_ref = UNSET
    elif isinstance(union_prop_with_ref, AnEnum):
        json_union_prop_with_ref = union_prop_with_ref.value
    else:
        json_union_prop_with_ref = union_prop_with_ref
    params["union_prop_with_ref"] = json_union_prop_with_ref

    json_enum_prop = enum_prop.value
    params["enum_prop"] = json_enum_prop

    json_model_prop = model_prop.to_dict()
    params.update(json_model_prop)

    json_required_model_prop = required_model_prop.to_dict()
    params.update(json_required_model_prop)

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/defaults",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError]]:
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
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    string_prop: str = "the default string",
    string_with_num: str = "1",
    date_prop: datetime.date = isoparse("1010-10-10").date(),
    float_prop: float = 3.14,
    float_with_int: float = 3.0,
    int_prop: int = 7,
    boolean_prop: bool = False,
    list_prop: list[AnEnum],
    union_prop: Union[float, str] = "not a float",
    union_prop_with_ref: Union[AnEnum, Unset, float] = 0.6,
    enum_prop: AnEnum,
    model_prop: "ModelWithUnionProperty",
    required_model_prop: "ModelWithUnionProperty",
) -> Response[Union[Any, HTTPValidationError]]:
    """Defaults

    Args:
        string_prop (str):  Default: 'the default string'.
        string_with_num (str):  Default: '1'.
        date_prop (datetime.date):  Default: isoparse('1010-10-10').date().
        float_prop (float):  Default: 3.14.
        float_with_int (float):  Default: 3.0.
        int_prop (int):  Default: 7.
        boolean_prop (bool):  Default: False.
        list_prop (list[AnEnum]):
        union_prop (Union[float, str]):  Default: 'not a float'.
        union_prop_with_ref (Union[AnEnum, Unset, float]):  Default: 0.6.
        enum_prop (AnEnum): For testing Enums in all the ways they can be used
        model_prop (ModelWithUnionProperty):
        required_model_prop (ModelWithUnionProperty):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        string_prop=string_prop,
        string_with_num=string_with_num,
        date_prop=date_prop,
        float_prop=float_prop,
        float_with_int=float_with_int,
        int_prop=int_prop,
        boolean_prop=boolean_prop,
        list_prop=list_prop,
        union_prop=union_prop,
        union_prop_with_ref=union_prop_with_ref,
        enum_prop=enum_prop,
        model_prop=model_prop,
        required_model_prop=required_model_prop,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    string_prop: str = "the default string",
    string_with_num: str = "1",
    date_prop: datetime.date = isoparse("1010-10-10").date(),
    float_prop: float = 3.14,
    float_with_int: float = 3.0,
    int_prop: int = 7,
    boolean_prop: bool = False,
    list_prop: list[AnEnum],
    union_prop: Union[float, str] = "not a float",
    union_prop_with_ref: Union[AnEnum, Unset, float] = 0.6,
    enum_prop: AnEnum,
    model_prop: "ModelWithUnionProperty",
    required_model_prop: "ModelWithUnionProperty",
) -> Optional[Union[Any, HTTPValidationError]]:
    """Defaults

    Args:
        string_prop (str):  Default: 'the default string'.
        string_with_num (str):  Default: '1'.
        date_prop (datetime.date):  Default: isoparse('1010-10-10').date().
        float_prop (float):  Default: 3.14.
        float_with_int (float):  Default: 3.0.
        int_prop (int):  Default: 7.
        boolean_prop (bool):  Default: False.
        list_prop (list[AnEnum]):
        union_prop (Union[float, str]):  Default: 'not a float'.
        union_prop_with_ref (Union[AnEnum, Unset, float]):  Default: 0.6.
        enum_prop (AnEnum): For testing Enums in all the ways they can be used
        model_prop (ModelWithUnionProperty):
        required_model_prop (ModelWithUnionProperty):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        string_prop=string_prop,
        string_with_num=string_with_num,
        date_prop=date_prop,
        float_prop=float_prop,
        float_with_int=float_with_int,
        int_prop=int_prop,
        boolean_prop=boolean_prop,
        list_prop=list_prop,
        union_prop=union_prop,
        union_prop_with_ref=union_prop_with_ref,
        enum_prop=enum_prop,
        model_prop=model_prop,
        required_model_prop=required_model_prop,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    string_prop: str = "the default string",
    string_with_num: str = "1",
    date_prop: datetime.date = isoparse("1010-10-10").date(),
    float_prop: float = 3.14,
    float_with_int: float = 3.0,
    int_prop: int = 7,
    boolean_prop: bool = False,
    list_prop: list[AnEnum],
    union_prop: Union[float, str] = "not a float",
    union_prop_with_ref: Union[AnEnum, Unset, float] = 0.6,
    enum_prop: AnEnum,
    model_prop: "ModelWithUnionProperty",
    required_model_prop: "ModelWithUnionProperty",
) -> Response[Union[Any, HTTPValidationError]]:
    """Defaults

    Args:
        string_prop (str):  Default: 'the default string'.
        string_with_num (str):  Default: '1'.
        date_prop (datetime.date):  Default: isoparse('1010-10-10').date().
        float_prop (float):  Default: 3.14.
        float_with_int (float):  Default: 3.0.
        int_prop (int):  Default: 7.
        boolean_prop (bool):  Default: False.
        list_prop (list[AnEnum]):
        union_prop (Union[float, str]):  Default: 'not a float'.
        union_prop_with_ref (Union[AnEnum, Unset, float]):  Default: 0.6.
        enum_prop (AnEnum): For testing Enums in all the ways they can be used
        model_prop (ModelWithUnionProperty):
        required_model_prop (ModelWithUnionProperty):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        string_prop=string_prop,
        string_with_num=string_with_num,
        date_prop=date_prop,
        float_prop=float_prop,
        float_with_int=float_with_int,
        int_prop=int_prop,
        boolean_prop=boolean_prop,
        list_prop=list_prop,
        union_prop=union_prop,
        union_prop_with_ref=union_prop_with_ref,
        enum_prop=enum_prop,
        model_prop=model_prop,
        required_model_prop=required_model_prop,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    string_prop: str = "the default string",
    string_with_num: str = "1",
    date_prop: datetime.date = isoparse("1010-10-10").date(),
    float_prop: float = 3.14,
    float_with_int: float = 3.0,
    int_prop: int = 7,
    boolean_prop: bool = False,
    list_prop: list[AnEnum],
    union_prop: Union[float, str] = "not a float",
    union_prop_with_ref: Union[AnEnum, Unset, float] = 0.6,
    enum_prop: AnEnum,
    model_prop: "ModelWithUnionProperty",
    required_model_prop: "ModelWithUnionProperty",
) -> Optional[Union[Any, HTTPValidationError]]:
    """Defaults

    Args:
        string_prop (str):  Default: 'the default string'.
        string_with_num (str):  Default: '1'.
        date_prop (datetime.date):  Default: isoparse('1010-10-10').date().
        float_prop (float):  Default: 3.14.
        float_with_int (float):  Default: 3.0.
        int_prop (int):  Default: 7.
        boolean_prop (bool):  Default: False.
        list_prop (list[AnEnum]):
        union_prop (Union[float, str]):  Default: 'not a float'.
        union_prop_with_ref (Union[AnEnum, Unset, float]):  Default: 0.6.
        enum_prop (AnEnum): For testing Enums in all the ways they can be used
        model_prop (ModelWithUnionProperty):
        required_model_prop (ModelWithUnionProperty):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            string_prop=string_prop,
            string_with_num=string_with_num,
            date_prop=date_prop,
            float_prop=float_prop,
            float_with_int=float_with_int,
            int_prop=int_prop,
            boolean_prop=boolean_prop,
            list_prop=list_prop,
            union_prop=union_prop,
            union_prop_with_ref=union_prop_with_ref,
            enum_prop=enum_prop,
            model_prop=model_prop,
            required_model_prop=required_model_prop,
        )
    ).parsed
