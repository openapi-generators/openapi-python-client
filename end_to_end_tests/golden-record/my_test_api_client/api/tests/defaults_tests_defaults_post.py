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
    string_prop_query: Union[Unset, str] = "the default string",
    not_required_not_nullable_datetime_prop_query: Union[Unset, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    not_required_nullable_datetime_prop_query: Union[Unset, None, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    required_not_nullable_datetime_prop_query: datetime.datetime = isoparse("1010-10-10T00:00:00"),
    required_nullable_datetime_prop_query: Optional[datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    date_prop_query: Union[Unset, datetime.date] = isoparse("1010-10-10").date(),
    float_prop_query: Union[Unset, float] = 3.14,
    int_prop_query: Union[Unset, int] = 7,
    boolean_prop_query: Union[Unset, bool] = False,
    list_prop_query: Union[Unset, List[AnEnum]] = UNSET,
    union_prop_query: Union[Unset, float, str] = "not a float",
    union_prop_with_ref_query: Union[AnEnum, Unset, float] = 0.6,
    enum_prop_query: Union[Unset, AnEnum] = UNSET,
    model_prop_query: Union[Unset, ModelWithUnionProperty] = UNSET,
    required_model_prop_query: ModelWithUnionProperty,
    nullable_model_prop_query: Union[Unset, None, ModelWithUnionProperty] = UNSET,
    nullable_required_model_prop_query: Optional[ModelWithUnionProperty],
) -> Dict[str, Any]:
    url = "{}/tests/defaults".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_not_required_not_nullable_datetime_prop_query: Union[Unset, str] = UNSET
    if not isinstance(not_required_not_nullable_datetime_prop_query, Unset):
        json_not_required_not_nullable_datetime_prop_query = not_required_not_nullable_datetime_prop_query.isoformat()

    json_not_required_nullable_datetime_prop_query: Union[Unset, None, str] = UNSET
    if not isinstance(not_required_nullable_datetime_prop_query, Unset):
        json_not_required_nullable_datetime_prop_query = (
            not_required_nullable_datetime_prop_query.isoformat() if not_required_nullable_datetime_prop_query else None
        )

    json_required_not_nullable_datetime_prop_query = required_not_nullable_datetime_prop_query.isoformat()

    json_required_nullable_datetime_prop_query = (
        required_nullable_datetime_prop_query.isoformat() if required_nullable_datetime_prop_query else None
    )

    json_date_prop_query: Union[Unset, str] = UNSET
    if not isinstance(date_prop_query, Unset):
        json_date_prop_query = date_prop_query.isoformat()

    json_list_prop_query: Union[Unset, List[str]] = UNSET
    if not isinstance(list_prop_query, Unset):
        json_list_prop_query = []
        for list_prop_item_data in list_prop_query:
            list_prop_item = list_prop_item_data.value

            json_list_prop_query.append(list_prop_item)

    json_union_prop_query: Union[Unset, float, str]
    if isinstance(union_prop_query, Unset):
        json_union_prop_query = UNSET
    else:
        json_union_prop_query = union_prop_query

    json_union_prop_with_ref_query: Union[Unset, float, str]
    if isinstance(union_prop_with_ref_query, Unset):
        json_union_prop_with_ref_query = UNSET
    elif isinstance(union_prop_with_ref_query, AnEnum):
        json_union_prop_with_ref_query = UNSET
        if not isinstance(union_prop_with_ref_query, Unset):
            json_union_prop_with_ref_query = union_prop_with_ref_query.value

    else:
        json_union_prop_with_ref_query = union_prop_with_ref_query

    json_enum_prop_query: Union[Unset, str] = UNSET
    if not isinstance(enum_prop_query, Unset):
        json_enum_prop_query = enum_prop_query.value

    json_model_prop_query: Union[Unset, Dict[str, Any]] = UNSET
    if not isinstance(model_prop_query, Unset):
        json_model_prop_query = model_prop_query.to_dict()

    json_required_model_prop_query = required_model_prop_query.to_dict()

    json_nullable_model_prop_query: Union[Unset, None, Dict[str, Any]] = UNSET
    if not isinstance(nullable_model_prop_query, Unset):
        json_nullable_model_prop_query = nullable_model_prop_query.to_dict() if nullable_model_prop_query else None

    json_nullable_required_model_prop_query = (
        nullable_required_model_prop_query.to_dict() if nullable_required_model_prop_query else None
    )

    params: Dict[str, Any] = {
        "string_prop": string_prop_query,
        "not_required_not_nullable_datetime_prop": json_not_required_not_nullable_datetime_prop_query,
        "not_required_nullable_datetime_prop": json_not_required_nullable_datetime_prop_query,
        "required_not_nullable_datetime_prop": json_required_not_nullable_datetime_prop_query,
        "required_nullable_datetime_prop": json_required_nullable_datetime_prop_query,
        "date_prop": json_date_prop_query,
        "float_prop": float_prop_query,
        "int_prop": int_prop_query,
        "boolean_prop": boolean_prop_query,
        "list_prop": json_list_prop_query,
        "union_prop": json_union_prop_query,
        "union_prop_with_ref": json_union_prop_with_ref_query,
        "enum_prop": json_enum_prop_query,
    }
    if not isinstance(json_model_prop_query, Unset):
        params.update(json_model_prop_query)
    params.update(json_required_model_prop_query)
    if not isinstance(json_nullable_model_prop_query, Unset) and json_nullable_model_prop_query is not None:
        params.update(json_nullable_model_prop_query)
    if json_nullable_required_model_prop_query is not None:
        params.update(json_nullable_required_model_prop_query)
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = response.json()

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    string_prop_query: Union[Unset, str] = "the default string",
    not_required_not_nullable_datetime_prop_query: Union[Unset, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    not_required_nullable_datetime_prop_query: Union[Unset, None, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    required_not_nullable_datetime_prop_query: datetime.datetime = isoparse("1010-10-10T00:00:00"),
    required_nullable_datetime_prop_query: Optional[datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    date_prop_query: Union[Unset, datetime.date] = isoparse("1010-10-10").date(),
    float_prop_query: Union[Unset, float] = 3.14,
    int_prop_query: Union[Unset, int] = 7,
    boolean_prop_query: Union[Unset, bool] = False,
    list_prop_query: Union[Unset, List[AnEnum]] = UNSET,
    union_prop_query: Union[Unset, float, str] = "not a float",
    union_prop_with_ref_query: Union[AnEnum, Unset, float] = 0.6,
    enum_prop_query: Union[Unset, AnEnum] = UNSET,
    model_prop_query: Union[Unset, ModelWithUnionProperty] = UNSET,
    required_model_prop_query: ModelWithUnionProperty,
    nullable_model_prop_query: Union[Unset, None, ModelWithUnionProperty] = UNSET,
    nullable_required_model_prop_query: Optional[ModelWithUnionProperty],
) -> Response[Union[Any, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        string_prop_query=string_prop_query,
        not_required_not_nullable_datetime_prop_query=not_required_not_nullable_datetime_prop_query,
        not_required_nullable_datetime_prop_query=not_required_nullable_datetime_prop_query,
        required_not_nullable_datetime_prop_query=required_not_nullable_datetime_prop_query,
        required_nullable_datetime_prop_query=required_nullable_datetime_prop_query,
        date_prop_query=date_prop_query,
        float_prop_query=float_prop_query,
        int_prop_query=int_prop_query,
        boolean_prop_query=boolean_prop_query,
        list_prop_query=list_prop_query,
        union_prop_query=union_prop_query,
        union_prop_with_ref_query=union_prop_with_ref_query,
        enum_prop_query=enum_prop_query,
        model_prop_query=model_prop_query,
        required_model_prop_query=required_model_prop_query,
        nullable_model_prop_query=nullable_model_prop_query,
        nullable_required_model_prop_query=nullable_required_model_prop_query,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    string_prop_query: Union[Unset, str] = "the default string",
    not_required_not_nullable_datetime_prop_query: Union[Unset, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    not_required_nullable_datetime_prop_query: Union[Unset, None, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    required_not_nullable_datetime_prop_query: datetime.datetime = isoparse("1010-10-10T00:00:00"),
    required_nullable_datetime_prop_query: Optional[datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    date_prop_query: Union[Unset, datetime.date] = isoparse("1010-10-10").date(),
    float_prop_query: Union[Unset, float] = 3.14,
    int_prop_query: Union[Unset, int] = 7,
    boolean_prop_query: Union[Unset, bool] = False,
    list_prop_query: Union[Unset, List[AnEnum]] = UNSET,
    union_prop_query: Union[Unset, float, str] = "not a float",
    union_prop_with_ref_query: Union[AnEnum, Unset, float] = 0.6,
    enum_prop_query: Union[Unset, AnEnum] = UNSET,
    model_prop_query: Union[Unset, ModelWithUnionProperty] = UNSET,
    required_model_prop_query: ModelWithUnionProperty,
    nullable_model_prop_query: Union[Unset, None, ModelWithUnionProperty] = UNSET,
    nullable_required_model_prop_query: Optional[ModelWithUnionProperty],
) -> Optional[Union[Any, HTTPValidationError]]:
    """ """

    return sync_detailed(
        client=client,
        string_prop_query=string_prop_query,
        not_required_not_nullable_datetime_prop_query=not_required_not_nullable_datetime_prop_query,
        not_required_nullable_datetime_prop_query=not_required_nullable_datetime_prop_query,
        required_not_nullable_datetime_prop_query=required_not_nullable_datetime_prop_query,
        required_nullable_datetime_prop_query=required_nullable_datetime_prop_query,
        date_prop_query=date_prop_query,
        float_prop_query=float_prop_query,
        int_prop_query=int_prop_query,
        boolean_prop_query=boolean_prop_query,
        list_prop_query=list_prop_query,
        union_prop_query=union_prop_query,
        union_prop_with_ref_query=union_prop_with_ref_query,
        enum_prop_query=enum_prop_query,
        model_prop_query=model_prop_query,
        required_model_prop_query=required_model_prop_query,
        nullable_model_prop_query=nullable_model_prop_query,
        nullable_required_model_prop_query=nullable_required_model_prop_query,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    string_prop_query: Union[Unset, str] = "the default string",
    not_required_not_nullable_datetime_prop_query: Union[Unset, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    not_required_nullable_datetime_prop_query: Union[Unset, None, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    required_not_nullable_datetime_prop_query: datetime.datetime = isoparse("1010-10-10T00:00:00"),
    required_nullable_datetime_prop_query: Optional[datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    date_prop_query: Union[Unset, datetime.date] = isoparse("1010-10-10").date(),
    float_prop_query: Union[Unset, float] = 3.14,
    int_prop_query: Union[Unset, int] = 7,
    boolean_prop_query: Union[Unset, bool] = False,
    list_prop_query: Union[Unset, List[AnEnum]] = UNSET,
    union_prop_query: Union[Unset, float, str] = "not a float",
    union_prop_with_ref_query: Union[AnEnum, Unset, float] = 0.6,
    enum_prop_query: Union[Unset, AnEnum] = UNSET,
    model_prop_query: Union[Unset, ModelWithUnionProperty] = UNSET,
    required_model_prop_query: ModelWithUnionProperty,
    nullable_model_prop_query: Union[Unset, None, ModelWithUnionProperty] = UNSET,
    nullable_required_model_prop_query: Optional[ModelWithUnionProperty],
) -> Response[Union[Any, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        string_prop_query=string_prop_query,
        not_required_not_nullable_datetime_prop_query=not_required_not_nullable_datetime_prop_query,
        not_required_nullable_datetime_prop_query=not_required_nullable_datetime_prop_query,
        required_not_nullable_datetime_prop_query=required_not_nullable_datetime_prop_query,
        required_nullable_datetime_prop_query=required_nullable_datetime_prop_query,
        date_prop_query=date_prop_query,
        float_prop_query=float_prop_query,
        int_prop_query=int_prop_query,
        boolean_prop_query=boolean_prop_query,
        list_prop_query=list_prop_query,
        union_prop_query=union_prop_query,
        union_prop_with_ref_query=union_prop_with_ref_query,
        enum_prop_query=enum_prop_query,
        model_prop_query=model_prop_query,
        required_model_prop_query=required_model_prop_query,
        nullable_model_prop_query=nullable_model_prop_query,
        nullable_required_model_prop_query=nullable_required_model_prop_query,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    string_prop_query: Union[Unset, str] = "the default string",
    not_required_not_nullable_datetime_prop_query: Union[Unset, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    not_required_nullable_datetime_prop_query: Union[Unset, None, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    required_not_nullable_datetime_prop_query: datetime.datetime = isoparse("1010-10-10T00:00:00"),
    required_nullable_datetime_prop_query: Optional[datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    date_prop_query: Union[Unset, datetime.date] = isoparse("1010-10-10").date(),
    float_prop_query: Union[Unset, float] = 3.14,
    int_prop_query: Union[Unset, int] = 7,
    boolean_prop_query: Union[Unset, bool] = False,
    list_prop_query: Union[Unset, List[AnEnum]] = UNSET,
    union_prop_query: Union[Unset, float, str] = "not a float",
    union_prop_with_ref_query: Union[AnEnum, Unset, float] = 0.6,
    enum_prop_query: Union[Unset, AnEnum] = UNSET,
    model_prop_query: Union[Unset, ModelWithUnionProperty] = UNSET,
    required_model_prop_query: ModelWithUnionProperty,
    nullable_model_prop_query: Union[Unset, None, ModelWithUnionProperty] = UNSET,
    nullable_required_model_prop_query: Optional[ModelWithUnionProperty],
) -> Optional[Union[Any, HTTPValidationError]]:
    """ """

    return (
        await asyncio_detailed(
            client=client,
            string_prop_query=string_prop_query,
            not_required_not_nullable_datetime_prop_query=not_required_not_nullable_datetime_prop_query,
            not_required_nullable_datetime_prop_query=not_required_nullable_datetime_prop_query,
            required_not_nullable_datetime_prop_query=required_not_nullable_datetime_prop_query,
            required_nullable_datetime_prop_query=required_nullable_datetime_prop_query,
            date_prop_query=date_prop_query,
            float_prop_query=float_prop_query,
            int_prop_query=int_prop_query,
            boolean_prop_query=boolean_prop_query,
            list_prop_query=list_prop_query,
            union_prop_query=union_prop_query,
            union_prop_with_ref_query=union_prop_with_ref_query,
            enum_prop_query=enum_prop_query,
            model_prop_query=model_prop_query,
            required_model_prop_query=required_model_prop_query,
            nullable_model_prop_query=nullable_model_prop_query,
            nullable_required_model_prop_query=nullable_required_model_prop_query,
        )
    ).parsed
