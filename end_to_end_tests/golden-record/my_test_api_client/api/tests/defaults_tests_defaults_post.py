import datetime
from typing import Any, Dict, List, Optional, Union

import httpx
from dateutil.parser import isoparse

from ...client import Client
from ...models.an_enum import AnEnum
from ...models.http_validation_error import HTTPValidationError
from ...models.model_with_union_property import ModelWithUnionProperty
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    string_prop: Union[Unset, str] = "the default string",
    not_required_not_nullable_datetime_prop: Union[Unset, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    not_required_nullable_datetime_prop: Union[Unset, None, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    required_not_nullable_datetime_prop: datetime.datetime = isoparse("1010-10-10T00:00:00"),
    required_nullable_datetime_prop: Optional[datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    date_prop: Union[Unset, datetime.date] = isoparse("1010-10-10").date(),
    float_prop: Union[Unset, float] = 3.14,
    int_prop: Union[Unset, int] = 7,
    boolean_prop: Union[Unset, bool] = False,
    list_prop: Union[Unset, List[AnEnum]] = UNSET,
    union_prop: Union[Unset, float, str] = "not a float",
    union_prop_with_ref: Union[AnEnum, Unset, float] = 0.6,
    enum_prop: Union[Unset, AnEnum] = UNSET,
    model_prop: Union[Unset, ModelWithUnionProperty] = UNSET,
    required_model_prop: ModelWithUnionProperty,
    nullable_model_prop: Union[Unset, None, ModelWithUnionProperty] = UNSET,
    nullable_required_model_prop: Optional[ModelWithUnionProperty],
) -> Dict[str, Any]:
    url = "{}/tests/defaults".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_not_required_not_nullable_datetime_prop: Union[Unset, str] = UNSET
    if not isinstance(not_required_not_nullable_datetime_prop, Unset):
        json_not_required_not_nullable_datetime_prop = not_required_not_nullable_datetime_prop.isoformat()

    json_not_required_nullable_datetime_prop: Union[Unset, None, str] = UNSET
    if not isinstance(not_required_nullable_datetime_prop, Unset):
        json_not_required_nullable_datetime_prop = (
            not_required_nullable_datetime_prop.isoformat() if not_required_nullable_datetime_prop else None
        )

    json_required_not_nullable_datetime_prop = required_not_nullable_datetime_prop.isoformat()

    json_required_nullable_datetime_prop = (
        required_nullable_datetime_prop.isoformat() if required_nullable_datetime_prop else None
    )

    json_date_prop: Union[Unset, str] = UNSET
    if not isinstance(date_prop, Unset):
        json_date_prop = date_prop.isoformat()

    json_list_prop: Union[Unset, List[str]] = UNSET
    if not isinstance(list_prop, Unset):
        json_list_prop = []
        for list_prop_item_data in list_prop:
            list_prop_item = list_prop_item_data.value

            json_list_prop.append(list_prop_item)

    json_union_prop: Union[Unset, float, str]
    if isinstance(union_prop, Unset):
        json_union_prop = UNSET
    else:
        json_union_prop = union_prop

    json_union_prop_with_ref: Union[Unset, float, str]
    if isinstance(union_prop_with_ref, Unset):
        json_union_prop_with_ref = UNSET
    elif isinstance(union_prop_with_ref, AnEnum):
        json_union_prop_with_ref = UNSET
        if not isinstance(union_prop_with_ref, Unset):
            json_union_prop_with_ref = union_prop_with_ref.value

    else:
        json_union_prop_with_ref = union_prop_with_ref

    json_enum_prop: Union[Unset, str] = UNSET
    if not isinstance(enum_prop, Unset):
        json_enum_prop = enum_prop.value

    json_model_prop: Union[Unset, Dict[str, Any]] = UNSET
    if not isinstance(model_prop, Unset):
        json_model_prop = model_prop.to_dict()

    json_required_model_prop = required_model_prop.to_dict()

    json_nullable_model_prop: Union[Unset, None, Dict[str, Any]] = UNSET
    if not isinstance(nullable_model_prop, Unset):
        json_nullable_model_prop = nullable_model_prop.to_dict() if nullable_model_prop else None

    json_nullable_required_model_prop = nullable_required_model_prop.to_dict() if nullable_required_model_prop else None

    params: Dict[str, Any] = {
        "string_prop": string_prop,
        "not_required_not_nullable_datetime_prop": json_not_required_not_nullable_datetime_prop,
        "not_required_nullable_datetime_prop": json_not_required_nullable_datetime_prop,
        "required_not_nullable_datetime_prop": json_required_not_nullable_datetime_prop,
        "required_nullable_datetime_prop": json_required_nullable_datetime_prop,
        "date_prop": json_date_prop,
        "float_prop": float_prop,
        "int_prop": int_prop,
        "boolean_prop": boolean_prop,
        "list_prop": json_list_prop,
        "union_prop": json_union_prop,
        "union_prop_with_ref": json_union_prop_with_ref,
        "enum_prop": json_enum_prop,
    }
    if not isinstance(json_model_prop, Unset):
        params.update(json_model_prop)
    params.update(json_required_model_prop)
    if not isinstance(json_nullable_model_prop, Unset) and json_nullable_model_prop is not None:
        params.update(json_nullable_model_prop)
    if json_nullable_required_model_prop is not None:
        params.update(json_nullable_required_model_prop)
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = None

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    string_prop: Union[Unset, str] = "the default string",
    not_required_not_nullable_datetime_prop: Union[Unset, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    not_required_nullable_datetime_prop: Union[Unset, None, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    required_not_nullable_datetime_prop: datetime.datetime = isoparse("1010-10-10T00:00:00"),
    required_nullable_datetime_prop: Optional[datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    date_prop: Union[Unset, datetime.date] = isoparse("1010-10-10").date(),
    float_prop: Union[Unset, float] = 3.14,
    int_prop: Union[Unset, int] = 7,
    boolean_prop: Union[Unset, bool] = False,
    list_prop: Union[Unset, List[AnEnum]] = UNSET,
    union_prop: Union[Unset, float, str] = "not a float",
    union_prop_with_ref: Union[AnEnum, Unset, float] = 0.6,
    enum_prop: Union[Unset, AnEnum] = UNSET,
    model_prop: Union[Unset, ModelWithUnionProperty] = UNSET,
    required_model_prop: ModelWithUnionProperty,
    nullable_model_prop: Union[Unset, None, ModelWithUnionProperty] = UNSET,
    nullable_required_model_prop: Optional[ModelWithUnionProperty],
) -> Response[Union[None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        string_prop=string_prop,
        not_required_not_nullable_datetime_prop=not_required_not_nullable_datetime_prop,
        not_required_nullable_datetime_prop=not_required_nullable_datetime_prop,
        required_not_nullable_datetime_prop=required_not_nullable_datetime_prop,
        required_nullable_datetime_prop=required_nullable_datetime_prop,
        date_prop=date_prop,
        float_prop=float_prop,
        int_prop=int_prop,
        boolean_prop=boolean_prop,
        list_prop=list_prop,
        union_prop=union_prop,
        union_prop_with_ref=union_prop_with_ref,
        enum_prop=enum_prop,
        model_prop=model_prop,
        required_model_prop=required_model_prop,
        nullable_model_prop=nullable_model_prop,
        nullable_required_model_prop=nullable_required_model_prop,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    string_prop: Union[Unset, str] = "the default string",
    not_required_not_nullable_datetime_prop: Union[Unset, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    not_required_nullable_datetime_prop: Union[Unset, None, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    required_not_nullable_datetime_prop: datetime.datetime = isoparse("1010-10-10T00:00:00"),
    required_nullable_datetime_prop: Optional[datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    date_prop: Union[Unset, datetime.date] = isoparse("1010-10-10").date(),
    float_prop: Union[Unset, float] = 3.14,
    int_prop: Union[Unset, int] = 7,
    boolean_prop: Union[Unset, bool] = False,
    list_prop: Union[Unset, List[AnEnum]] = UNSET,
    union_prop: Union[Unset, float, str] = "not a float",
    union_prop_with_ref: Union[AnEnum, Unset, float] = 0.6,
    enum_prop: Union[Unset, AnEnum] = UNSET,
    model_prop: Union[Unset, ModelWithUnionProperty] = UNSET,
    required_model_prop: ModelWithUnionProperty,
    nullable_model_prop: Union[Unset, None, ModelWithUnionProperty] = UNSET,
    nullable_required_model_prop: Optional[ModelWithUnionProperty],
) -> Optional[Union[None, HTTPValidationError]]:
    """  """

    return sync_detailed(
        client=client,
        string_prop=string_prop,
        not_required_not_nullable_datetime_prop=not_required_not_nullable_datetime_prop,
        not_required_nullable_datetime_prop=not_required_nullable_datetime_prop,
        required_not_nullable_datetime_prop=required_not_nullable_datetime_prop,
        required_nullable_datetime_prop=required_nullable_datetime_prop,
        date_prop=date_prop,
        float_prop=float_prop,
        int_prop=int_prop,
        boolean_prop=boolean_prop,
        list_prop=list_prop,
        union_prop=union_prop,
        union_prop_with_ref=union_prop_with_ref,
        enum_prop=enum_prop,
        model_prop=model_prop,
        required_model_prop=required_model_prop,
        nullable_model_prop=nullable_model_prop,
        nullable_required_model_prop=nullable_required_model_prop,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    string_prop: Union[Unset, str] = "the default string",
    not_required_not_nullable_datetime_prop: Union[Unset, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    not_required_nullable_datetime_prop: Union[Unset, None, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    required_not_nullable_datetime_prop: datetime.datetime = isoparse("1010-10-10T00:00:00"),
    required_nullable_datetime_prop: Optional[datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    date_prop: Union[Unset, datetime.date] = isoparse("1010-10-10").date(),
    float_prop: Union[Unset, float] = 3.14,
    int_prop: Union[Unset, int] = 7,
    boolean_prop: Union[Unset, bool] = False,
    list_prop: Union[Unset, List[AnEnum]] = UNSET,
    union_prop: Union[Unset, float, str] = "not a float",
    union_prop_with_ref: Union[AnEnum, Unset, float] = 0.6,
    enum_prop: Union[Unset, AnEnum] = UNSET,
    model_prop: Union[Unset, ModelWithUnionProperty] = UNSET,
    required_model_prop: ModelWithUnionProperty,
    nullable_model_prop: Union[Unset, None, ModelWithUnionProperty] = UNSET,
    nullable_required_model_prop: Optional[ModelWithUnionProperty],
) -> Response[Union[None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        string_prop=string_prop,
        not_required_not_nullable_datetime_prop=not_required_not_nullable_datetime_prop,
        not_required_nullable_datetime_prop=not_required_nullable_datetime_prop,
        required_not_nullable_datetime_prop=required_not_nullable_datetime_prop,
        required_nullable_datetime_prop=required_nullable_datetime_prop,
        date_prop=date_prop,
        float_prop=float_prop,
        int_prop=int_prop,
        boolean_prop=boolean_prop,
        list_prop=list_prop,
        union_prop=union_prop,
        union_prop_with_ref=union_prop_with_ref,
        enum_prop=enum_prop,
        model_prop=model_prop,
        required_model_prop=required_model_prop,
        nullable_model_prop=nullable_model_prop,
        nullable_required_model_prop=nullable_required_model_prop,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    string_prop: Union[Unset, str] = "the default string",
    not_required_not_nullable_datetime_prop: Union[Unset, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    not_required_nullable_datetime_prop: Union[Unset, None, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    required_not_nullable_datetime_prop: datetime.datetime = isoparse("1010-10-10T00:00:00"),
    required_nullable_datetime_prop: Optional[datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    date_prop: Union[Unset, datetime.date] = isoparse("1010-10-10").date(),
    float_prop: Union[Unset, float] = 3.14,
    int_prop: Union[Unset, int] = 7,
    boolean_prop: Union[Unset, bool] = False,
    list_prop: Union[Unset, List[AnEnum]] = UNSET,
    union_prop: Union[Unset, float, str] = "not a float",
    union_prop_with_ref: Union[AnEnum, Unset, float] = 0.6,
    enum_prop: Union[Unset, AnEnum] = UNSET,
    model_prop: Union[Unset, ModelWithUnionProperty] = UNSET,
    required_model_prop: ModelWithUnionProperty,
    nullable_model_prop: Union[Unset, None, ModelWithUnionProperty] = UNSET,
    nullable_required_model_prop: Optional[ModelWithUnionProperty],
) -> Optional[Union[None, HTTPValidationError]]:
    """  """

    return (
        await asyncio_detailed(
            client=client,
            string_prop=string_prop,
            not_required_not_nullable_datetime_prop=not_required_not_nullable_datetime_prop,
            not_required_nullable_datetime_prop=not_required_nullable_datetime_prop,
            required_not_nullable_datetime_prop=required_not_nullable_datetime_prop,
            required_nullable_datetime_prop=required_nullable_datetime_prop,
            date_prop=date_prop,
            float_prop=float_prop,
            int_prop=int_prop,
            boolean_prop=boolean_prop,
            list_prop=list_prop,
            union_prop=union_prop,
            union_prop_with_ref=union_prop_with_ref,
            enum_prop=enum_prop,
            model_prop=model_prop,
            required_model_prop=required_model_prop,
            nullable_model_prop=nullable_model_prop,
            nullable_required_model_prop=nullable_required_model_prop,
        )
    ).parsed
