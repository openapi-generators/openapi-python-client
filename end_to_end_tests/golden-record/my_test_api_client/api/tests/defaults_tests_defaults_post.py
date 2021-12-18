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
    string_prop: str = "the default string",
    date_prop: datetime.date = isoparse("1010-10-10").date(),
    float_prop: float = 3.14,
    int_prop: int = 7,
    boolean_prop: bool = False,
    list_prop: List[AnEnum],
    union_prop: Union[float, str] = "not a float",
    union_prop_with_ref: Union[AnEnum, None, Unset, float] = 0.6,
    enum_prop: AnEnum,
    model_prop: ModelWithUnionProperty,
    required_model_prop: ModelWithUnionProperty,
) -> Dict[str, Any]:
    url = "{}/tests/defaults".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_date_prop = date_prop.isoformat()
    json_list_prop = []
    for list_prop_item_data in list_prop:
        list_prop_item = list_prop_item_data.value

        json_list_prop.append(list_prop_item)

    json_union_prop = union_prop

    json_union_prop_with_ref: Union[None, Unset, float, str]
    if isinstance(union_prop_with_ref, Unset):
        json_union_prop_with_ref = UNSET
    elif union_prop_with_ref is None:
        json_union_prop_with_ref = None
    elif isinstance(union_prop_with_ref, AnEnum):
        json_union_prop_with_ref = UNSET
        if not isinstance(union_prop_with_ref, Unset):
            json_union_prop_with_ref = union_prop_with_ref.value

    else:
        json_union_prop_with_ref = union_prop_with_ref

    json_enum_prop = enum_prop.value

    json_model_prop = model_prop.to_dict()

    json_required_model_prop = required_model_prop.to_dict()

    params: Dict[str, Any] = {
        "string_prop": string_prop,
        "date_prop": json_date_prop,
        "float_prop": float_prop,
        "int_prop": int_prop,
        "boolean_prop": boolean_prop,
        "list_prop": json_list_prop,
        "union_prop": json_union_prop,
        "union_prop_with_ref": json_union_prop_with_ref,
        "enum_prop": json_enum_prop,
    }
    params.update(json_model_prop)
    params.update(json_required_model_prop)
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
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
    string_prop: str = "the default string",
    date_prop: datetime.date = isoparse("1010-10-10").date(),
    float_prop: float = 3.14,
    int_prop: int = 7,
    boolean_prop: bool = False,
    list_prop: List[AnEnum],
    union_prop: Union[float, str] = "not a float",
    union_prop_with_ref: Union[AnEnum, None, Unset, float] = 0.6,
    enum_prop: AnEnum,
    model_prop: ModelWithUnionProperty,
    required_model_prop: ModelWithUnionProperty,
) -> Response[Union[Any, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        string_prop=string_prop,
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
    )

    response = httpx.post(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    string_prop: str = "the default string",
    date_prop: datetime.date = isoparse("1010-10-10").date(),
    float_prop: float = 3.14,
    int_prop: int = 7,
    boolean_prop: bool = False,
    list_prop: List[AnEnum],
    union_prop: Union[float, str] = "not a float",
    union_prop_with_ref: Union[AnEnum, None, Unset, float] = 0.6,
    enum_prop: AnEnum,
    model_prop: ModelWithUnionProperty,
    required_model_prop: ModelWithUnionProperty,
) -> Optional[Union[Any, HTTPValidationError]]:
    """ """

    return sync_detailed(
        client=client,
        string_prop=string_prop,
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
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    string_prop: str = "the default string",
    date_prop: datetime.date = isoparse("1010-10-10").date(),
    float_prop: float = 3.14,
    int_prop: int = 7,
    boolean_prop: bool = False,
    list_prop: List[AnEnum],
    union_prop: Union[float, str] = "not a float",
    union_prop_with_ref: Union[AnEnum, None, Unset, float] = 0.6,
    enum_prop: AnEnum,
    model_prop: ModelWithUnionProperty,
    required_model_prop: ModelWithUnionProperty,
) -> Response[Union[Any, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        string_prop=string_prop,
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
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    string_prop: str = "the default string",
    date_prop: datetime.date = isoparse("1010-10-10").date(),
    float_prop: float = 3.14,
    int_prop: int = 7,
    boolean_prop: bool = False,
    list_prop: List[AnEnum],
    union_prop: Union[float, str] = "not a float",
    union_prop_with_ref: Union[AnEnum, None, Unset, float] = 0.6,
    enum_prop: AnEnum,
    model_prop: ModelWithUnionProperty,
    required_model_prop: ModelWithUnionProperty,
) -> Optional[Union[Any, HTTPValidationError]]:
    """ """

    return (
        await asyncio_detailed(
            client=client,
            string_prop=string_prop,
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
        )
    ).parsed
