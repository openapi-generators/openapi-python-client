import datetime
from dataclasses import asdict
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...models.an_enum import AnEnum
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: Dict[Any, Any],
    string_prop: Optional[str] = "the default string",
    datetime_prop: Optional[datetime.datetime] = datetime.datetime(1010, 10, 10, 0, 0),
    date_prop: Optional[datetime.date] = datetime.date(1010, 10, 10),
    float_prop: Optional[float] = 3.14,
    int_prop: Optional[int] = 7,
    boolean_prop: Optional[bool] = False,
    list_prop: Optional[List[AnEnum]] = None,
    union_prop: Optional[Union[Optional[float], Optional[str]]] = "not a float",
    enum_prop: Optional[AnEnum] = None,
) -> Dict[str, Any]:
    url = "{}/tests/defaults".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_datetime_prop = datetime_prop.isoformat() if datetime_prop else None

    json_date_prop = date_prop.isoformat() if date_prop else None

    if list_prop is None:
        json_list_prop = None
    else:
        json_list_prop = []
        for list_prop_item_data in list_prop:
            list_prop_item = list_prop_item_data.value

            json_list_prop.append(list_prop_item)

    if union_prop is None:
        json_union_prop: Optional[Union[Optional[float], Optional[str]]] = None
    elif isinstance(union_prop, float):
        json_union_prop = union_prop
    else:
        json_union_prop = union_prop

    json_enum_prop = enum_prop.value if enum_prop else None

    params: Dict[str, Any] = {}
    if string_prop is not None:
        params["string_prop"] = string_prop
    if datetime_prop is not None:
        params["datetime_prop"] = json_datetime_prop
    if date_prop is not None:
        params["date_prop"] = json_date_prop
    if float_prop is not None:
        params["float_prop"] = float_prop
    if int_prop is not None:
        params["int_prop"] = int_prop
    if boolean_prop is not None:
        params["boolean_prop"] = boolean_prop
    if list_prop is not None:
        params["list_prop"] = json_list_prop
    if union_prop is not None:
        params["union_prop"] = json_union_prop
    if enum_prop is not None:
        params["enum_prop"] = json_enum_prop

    json_json_body = json_body

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, HTTPValidationError]]:
    if response.status_code == 200:
        return None
    if response.status_code == 422:
        return HTTPValidationError.from_dict(cast(Dict[str, Any], response.json()))
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
    json_body: Dict[Any, Any],
    string_prop: Optional[str] = "the default string",
    datetime_prop: Optional[datetime.datetime] = datetime.datetime(1010, 10, 10, 0, 0),
    date_prop: Optional[datetime.date] = datetime.date(1010, 10, 10),
    float_prop: Optional[float] = 3.14,
    int_prop: Optional[int] = 7,
    boolean_prop: Optional[bool] = False,
    list_prop: Optional[List[AnEnum]] = None,
    union_prop: Optional[Union[Optional[float], Optional[str]]] = "not a float",
    enum_prop: Optional[AnEnum] = None,
) -> Response[Union[None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        string_prop=string_prop,
        datetime_prop=datetime_prop,
        date_prop=date_prop,
        float_prop=float_prop,
        int_prop=int_prop,
        boolean_prop=boolean_prop,
        list_prop=list_prop,
        union_prop=union_prop,
        enum_prop=enum_prop,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: Dict[Any, Any],
    string_prop: Optional[str] = "the default string",
    datetime_prop: Optional[datetime.datetime] = datetime.datetime(1010, 10, 10, 0, 0),
    date_prop: Optional[datetime.date] = datetime.date(1010, 10, 10),
    float_prop: Optional[float] = 3.14,
    int_prop: Optional[int] = 7,
    boolean_prop: Optional[bool] = False,
    list_prop: Optional[List[AnEnum]] = None,
    union_prop: Optional[Union[Optional[float], Optional[str]]] = "not a float",
    enum_prop: Optional[AnEnum] = None,
) -> Optional[Union[None, HTTPValidationError]]:
    """  """

    return sync_detailed(
        client=client,
        json_body=json_body,
        string_prop=string_prop,
        datetime_prop=datetime_prop,
        date_prop=date_prop,
        float_prop=float_prop,
        int_prop=int_prop,
        boolean_prop=boolean_prop,
        list_prop=list_prop,
        union_prop=union_prop,
        enum_prop=enum_prop,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: Dict[Any, Any],
    string_prop: Optional[str] = "the default string",
    datetime_prop: Optional[datetime.datetime] = datetime.datetime(1010, 10, 10, 0, 0),
    date_prop: Optional[datetime.date] = datetime.date(1010, 10, 10),
    float_prop: Optional[float] = 3.14,
    int_prop: Optional[int] = 7,
    boolean_prop: Optional[bool] = False,
    list_prop: Optional[List[AnEnum]] = None,
    union_prop: Optional[Union[Optional[float], Optional[str]]] = "not a float",
    enum_prop: Optional[AnEnum] = None,
) -> Response[Union[None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        string_prop=string_prop,
        datetime_prop=datetime_prop,
        date_prop=date_prop,
        float_prop=float_prop,
        int_prop=int_prop,
        boolean_prop=boolean_prop,
        list_prop=list_prop,
        union_prop=union_prop,
        enum_prop=enum_prop,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: Dict[Any, Any],
    string_prop: Optional[str] = "the default string",
    datetime_prop: Optional[datetime.datetime] = datetime.datetime(1010, 10, 10, 0, 0),
    date_prop: Optional[datetime.date] = datetime.date(1010, 10, 10),
    float_prop: Optional[float] = 3.14,
    int_prop: Optional[int] = 7,
    boolean_prop: Optional[bool] = False,
    list_prop: Optional[List[AnEnum]] = None,
    union_prop: Optional[Union[Optional[float], Optional[str]]] = "not a float",
    enum_prop: Optional[AnEnum] = None,
) -> Optional[Union[None, HTTPValidationError]]:
    """  """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            string_prop=string_prop,
            datetime_prop=datetime_prop,
            date_prop=date_prop,
            float_prop=float_prop,
            int_prop=int_prop,
            boolean_prop=boolean_prop,
            list_prop=list_prop,
            union_prop=union_prop,
            enum_prop=enum_prop,
        )
    ).parsed
