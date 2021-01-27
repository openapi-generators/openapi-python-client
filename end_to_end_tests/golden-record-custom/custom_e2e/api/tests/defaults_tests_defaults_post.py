from typing import Optional

import httpx

from ...types import Response

Client = httpx.Client

import datetime
from typing import Dict, List, Union

from dateutil.parser import isoparse

from ...models.an_enum import AnEnum
from ...models.http_validation_error import HTTPValidationError
from ...models.model_with_union_property import ModelWithUnionProperty
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
    union_prop_with_ref: Union[Unset, float, AnEnum] = 0.6,
    enum_prop: Union[Unset, AnEnum] = UNSET,
    model_prop: Union[ModelWithUnionProperty, Unset] = UNSET,
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

    json_model_prop: Union[Unset, Dict[str, Any]] = UNSET
    if not isinstance(model_prop, Unset):
        json_model_prop = model_prop.to_dict()

    params: Dict[str, Any] = {}
    if not isinstance(string_prop, Unset) and string_prop is not None:
        params["string_prop"] = string_prop
    if not isinstance(json_datetime_prop, Unset) and json_datetime_prop is not None:
        params["datetime_prop"] = json_datetime_prop
    if not isinstance(json_date_prop, Unset) and json_date_prop is not None:
        params["date_prop"] = json_date_prop
    if not isinstance(float_prop, Unset) and float_prop is not None:
        params["float_prop"] = float_prop
    if not isinstance(int_prop, Unset) and int_prop is not None:
        params["int_prop"] = int_prop
    if not isinstance(boolean_prop, Unset) and boolean_prop is not None:
        params["boolean_prop"] = boolean_prop
    if not isinstance(json_list_prop, Unset) and json_list_prop is not None:
        params["list_prop"] = json_list_prop
    if not isinstance(json_union_prop, Unset) and json_union_prop is not None:
        params["union_prop"] = json_union_prop
    if not isinstance(json_union_prop_with_ref, Unset) and json_union_prop_with_ref is not None:
        params["union_prop_with_ref"] = json_union_prop_with_ref
    if not isinstance(json_enum_prop, Unset) and json_enum_prop is not None:
        params["enum_prop"] = json_enum_prop
    if not isinstance(json_model_prop, Unset) and json_model_prop is not None:
        params.update(json_model_prop)

    response = client.request(
        "post",
        "/tests/defaults",
        params=params,
    )

    return _build_response(response=response)
