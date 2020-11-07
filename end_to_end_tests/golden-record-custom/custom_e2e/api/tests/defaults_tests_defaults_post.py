from typing import Optional

import httpx

from ...types import Response

Client = httpx.Client

import datetime
from typing import Dict, List, Union

from dateutil.parser import isoparse

from ...models.an_enum import AnEnum
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Unset


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


def httpx_request(
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
    enum_prop: Union[Unset, AnEnum] = UNSET,
) -> Response[Union[None, HTTPValidationError]]:

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
    elif isinstance(union_prop, float):
        json_union_prop = union_prop
    else:
        json_union_prop = union_prop

    json_enum_prop: Union[Unset, AnEnum] = UNSET
    if not isinstance(enum_prop, Unset):
        json_enum_prop = enum_prop.value

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
    if enum_prop is not UNSET:
        params["enum_prop"] = json_enum_prop

    response = client.request(
        "post",
        "/tests/defaults",
        params=params,
    )

    return _build_response(response=response)
