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
    string_prop: Union[Unset, None, str] = "the default string",
    datetime_prop: Union[Unset, None, datetime.datetime] = isoparse("1010-10-10T00:00:00"),
    date_prop: Union[Unset, None, datetime.date] = isoparse("1010-10-10").date(),
    float_prop: Union[Unset, None, float] = 3.14,
    int_prop: Union[Unset, None, int] = 7,
    boolean_prop: Union[Unset, None, bool] = False,
    list_prop: Union[Unset, None, List[AnEnum]] = None,
    union_prop: Union[Unset, None, float, str] = "not a float",
    union_prop_with_ref: Union[Unset, None, float, AnEnum] = 0.6,
    enum_prop: Union[Unset, None, AnEnum] = None,
) -> Response[Union[None, HTTPValidationError]]:

    json_datetime_prop: Union[Unset, str] = UNSET
    if not isinstance(datetime_prop, Unset) and datetime_prop is not None:
        json_datetime_prop = datetime_prop.isoformat()

    json_date_prop: Union[Unset, str] = UNSET
    if not isinstance(date_prop, Unset) and date_prop is not None:
        json_date_prop = date_prop.isoformat()

    json_list_prop: Union[Unset, List[Any]] = UNSET
    if not isinstance(list_prop, Unset) and list_prop is not None:
        json_list_prop = []
        for list_prop_item_data in list_prop:
            list_prop_item = list_prop_item_data.value

            json_list_prop.append(list_prop_item)

    json_union_prop: Union[Unset, float, str]
    if isinstance(union_prop, Unset) or union_prop is None:
        json_union_prop = UNSET
    else:
        json_union_prop = union_prop

    json_union_prop_with_ref: Union[Unset, float, AnEnum]
    if isinstance(union_prop_with_ref, Unset) or union_prop_with_ref is None:
        json_union_prop_with_ref = UNSET
    elif isinstance(union_prop_with_ref, AnEnum):
        json_union_prop_with_ref = UNSET
        if not isinstance(union_prop_with_ref, Unset):
            json_union_prop_with_ref = union_prop_with_ref

    else:
        json_union_prop_with_ref = union_prop_with_ref

    json_enum_prop: Union[Unset, AnEnum] = UNSET
    if not isinstance(enum_prop, Unset) and enum_prop is not None:
        json_enum_prop = enum_prop

    params: Dict[str, Any] = {}
    if string_prop is not UNSET and string_prop is not None:
        params["string_prop"] = string_prop
    if datetime_prop is not UNSET and datetime_prop is not None:
        params["datetime_prop"] = json_datetime_prop
    if date_prop is not UNSET and date_prop is not None:
        params["date_prop"] = json_date_prop
    if float_prop is not UNSET and float_prop is not None:
        params["float_prop"] = float_prop
    if int_prop is not UNSET and int_prop is not None:
        params["int_prop"] = int_prop
    if boolean_prop is not UNSET and boolean_prop is not None:
        params["boolean_prop"] = boolean_prop
    if list_prop is not UNSET and list_prop is not None:
        params["list_prop"] = json_list_prop
    if union_prop is not UNSET and union_prop is not None:
        params["union_prop"] = json_union_prop
    if union_prop_with_ref is not UNSET and union_prop_with_ref is not None:
        params["union_prop_with_ref"] = json_union_prop_with_ref
    if enum_prop is not UNSET and enum_prop is not None:
        params["enum_prop"] = json_enum_prop

    response = client.request(
        "post",
        "/tests/defaults",
        params=params,
    )

    return _build_response(response=response)
