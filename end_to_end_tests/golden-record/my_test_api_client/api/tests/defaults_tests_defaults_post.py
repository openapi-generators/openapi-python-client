import datetime
from typing import Any, Dict, List, Optional, Union

import httpx
from dateutil.parser import isoparse

from ...client import Client
from ...models.an_enum import AnEnum
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    string_prop: Union[Unset, str] = "the default string",
    datetime_prop: Union[Unset, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    date_prop: Union[Unset, datetime.date] = isoparse("1010-10-10").date(),
    float_prop: Union[Unset, float] = 3.14,
    int_prop: Union[Unset, int] = 7,
    boolean_prop: Union[Unset, bool] = False,
    list_prop: Union[Unset, List[AnEnum]] = UNSET,
    union_prop: Union[Unset, float, str] = "not a float",
    union_prop_with_ref: Union[Unset, float, AnEnum] = 0.6,
    enum_prop: Union[Unset, AnEnum] = UNSET,
) -> Dict[str, Any]:
    url = "{}/tests/defaults".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_datetime_prop: Union[Unset, str] = UNSET
    if not isinstance(datetime_prop, Unset):
        json_datetime_prop = datetime_prop.isoformat()

    json_date_prop: Union[Unset, str] = UNSET
    if not isinstance(date_prop, Unset):
        json_date_prop = date_prop.isoformat()

    json_list_prop: Union[Unset, List[Any]] = UNSET
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

    json_union_prop_with_ref: Union[Unset, float, AnEnum]
    if isinstance(union_prop_with_ref, Unset):
        json_union_prop_with_ref = UNSET
    elif isinstance(union_prop_with_ref, AnEnum):
        json_union_prop_with_ref = UNSET
        if not isinstance(union_prop_with_ref, Unset):
            json_union_prop_with_ref = union_prop_with_ref

    else:
        json_union_prop_with_ref = union_prop_with_ref

    json_enum_prop: Union[Unset, AnEnum] = UNSET
    if not isinstance(enum_prop, Unset):
        json_enum_prop = enum_prop

    params: Dict[str, Any] = {}
    if string_prop is not UNSET:
        params["string_prop"] = string_prop
    if datetime_prop is not UNSET:
        params["datetime_prop"] = json_datetime_prop
    if date_prop is not UNSET:
        params["date_prop"] = json_date_prop
    if float_prop is not UNSET:
        params["float_prop"] = float_prop
    if int_prop is not UNSET:
        params["int_prop"] = int_prop
    if boolean_prop is not UNSET:
        params["boolean_prop"] = boolean_prop
    if list_prop is not UNSET:
        params["list_prop"] = json_list_prop
    if union_prop is not UNSET:
        params["union_prop"] = json_union_prop
    if union_prop_with_ref is not UNSET:
        params["union_prop_with_ref"] = json_union_prop_with_ref
    if enum_prop is not UNSET:
        params["enum_prop"] = json_enum_prop

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
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
    datetime_prop: Union[Unset, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    date_prop: Union[Unset, datetime.date] = isoparse("1010-10-10").date(),
    float_prop: Union[Unset, float] = 3.14,
    int_prop: Union[Unset, int] = 7,
    boolean_prop: Union[Unset, bool] = False,
    list_prop: Union[Unset, List[AnEnum]] = UNSET,
    union_prop: Union[Unset, float, str] = "not a float",
    union_prop_with_ref: Union[Unset, float, AnEnum] = 0.6,
    enum_prop: Union[Unset, AnEnum] = UNSET,
) -> Response[Union[None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        string_prop=string_prop,
        datetime_prop=datetime_prop,
        date_prop=date_prop,
        float_prop=float_prop,
        int_prop=int_prop,
        boolean_prop=boolean_prop,
        list_prop=list_prop,
        union_prop=union_prop,
        union_prop_with_ref=union_prop_with_ref,
        enum_prop=enum_prop,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    string_prop: Union[Unset, str] = "the default string",
    datetime_prop: Union[Unset, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    date_prop: Union[Unset, datetime.date] = isoparse("1010-10-10").date(),
    float_prop: Union[Unset, float] = 3.14,
    int_prop: Union[Unset, int] = 7,
    boolean_prop: Union[Unset, bool] = False,
    list_prop: Union[Unset, List[AnEnum]] = UNSET,
    union_prop: Union[Unset, float, str] = "not a float",
    union_prop_with_ref: Union[Unset, float, AnEnum] = 0.6,
    enum_prop: Union[Unset, AnEnum] = UNSET,
) -> Optional[Union[None, HTTPValidationError]]:
    """  """

    return sync_detailed(
        client=client,
        string_prop=string_prop,
        datetime_prop=datetime_prop,
        date_prop=date_prop,
        float_prop=float_prop,
        int_prop=int_prop,
        boolean_prop=boolean_prop,
        list_prop=list_prop,
        union_prop=union_prop,
        union_prop_with_ref=union_prop_with_ref,
        enum_prop=enum_prop,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    string_prop: Union[Unset, str] = "the default string",
    datetime_prop: Union[Unset, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    date_prop: Union[Unset, datetime.date] = isoparse("1010-10-10").date(),
    float_prop: Union[Unset, float] = 3.14,
    int_prop: Union[Unset, int] = 7,
    boolean_prop: Union[Unset, bool] = False,
    list_prop: Union[Unset, List[AnEnum]] = UNSET,
    union_prop: Union[Unset, float, str] = "not a float",
    union_prop_with_ref: Union[Unset, float, AnEnum] = 0.6,
    enum_prop: Union[Unset, AnEnum] = UNSET,
) -> Response[Union[None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        string_prop=string_prop,
        datetime_prop=datetime_prop,
        date_prop=date_prop,
        float_prop=float_prop,
        int_prop=int_prop,
        boolean_prop=boolean_prop,
        list_prop=list_prop,
        union_prop=union_prop,
        union_prop_with_ref=union_prop_with_ref,
        enum_prop=enum_prop,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    string_prop: Union[Unset, str] = "the default string",
    datetime_prop: Union[Unset, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    date_prop: Union[Unset, datetime.date] = isoparse("1010-10-10").date(),
    float_prop: Union[Unset, float] = 3.14,
    int_prop: Union[Unset, int] = 7,
    boolean_prop: Union[Unset, bool] = False,
    list_prop: Union[Unset, List[AnEnum]] = UNSET,
    union_prop: Union[Unset, float, str] = "not a float",
    union_prop_with_ref: Union[Unset, float, AnEnum] = 0.6,
    enum_prop: Union[Unset, AnEnum] = UNSET,
) -> Optional[Union[None, HTTPValidationError]]:
    """  """

    return (
        await asyncio_detailed(
            client=client,
            string_prop=string_prop,
            datetime_prop=datetime_prop,
            date_prop=date_prop,
            float_prop=float_prop,
            int_prop=int_prop,
            boolean_prop=boolean_prop,
            list_prop=list_prop,
            union_prop=union_prop,
            union_prop_with_ref=union_prop_with_ref,
            enum_prop=enum_prop,
        )
    ).parsed
