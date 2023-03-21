import datetime
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx
from dateutil.parser import isoparse

from ... import errors
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
    model_prop: "ModelWithUnionProperty",
    required_model_prop: "ModelWithUnionProperty",
) -> Dict[str, Any]:
    url = "{}/tests/defaults".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["string_prop"] = string_prop

    json_date_prop = date_prop.isoformat()
    params["date_prop"] = json_date_prop

    params["float_prop"] = float_prop

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

    params["union_prop_with_ref"] = json_union_prop_with_ref

    json_enum_prop = enum_prop.value

    params["enum_prop"] = json_enum_prop

    json_model_prop = model_prop.to_dict()

    params.update(json_model_prop)

    json_required_model_prop = required_model_prop.to_dict()

    params.update(json_required_model_prop)

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(Any, response.json())
        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
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
    model_prop: "ModelWithUnionProperty",
    required_model_prop: "ModelWithUnionProperty",
) -> Response[Union[Any, HTTPValidationError]]:
    """Defaults

    Args:
        string_prop (str):  Default: 'the default string'.
        date_prop (datetime.date):  Default: isoparse('1010-10-10').date().
        float_prop (float):  Default: 3.14.
        int_prop (int):  Default: 7.
        boolean_prop (bool):
        list_prop (List[AnEnum]):
        union_prop (Union[float, str]):  Default: 'not a float'.
        union_prop_with_ref (Union[AnEnum, None, Unset, float]):  Default: 0.6.
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

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


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
    model_prop: "ModelWithUnionProperty",
    required_model_prop: "ModelWithUnionProperty",
) -> Optional[Union[Any, HTTPValidationError]]:
    """Defaults

    Args:
        string_prop (str):  Default: 'the default string'.
        date_prop (datetime.date):  Default: isoparse('1010-10-10').date().
        float_prop (float):  Default: 3.14.
        int_prop (int):  Default: 7.
        boolean_prop (bool):
        list_prop (List[AnEnum]):
        union_prop (Union[float, str]):  Default: 'not a float'.
        union_prop_with_ref (Union[AnEnum, None, Unset, float]):  Default: 0.6.
        enum_prop (AnEnum): For testing Enums in all the ways they can be used
        model_prop (ModelWithUnionProperty):
        required_model_prop (ModelWithUnionProperty):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

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
    model_prop: "ModelWithUnionProperty",
    required_model_prop: "ModelWithUnionProperty",
) -> Response[Union[Any, HTTPValidationError]]:
    """Defaults

    Args:
        string_prop (str):  Default: 'the default string'.
        date_prop (datetime.date):  Default: isoparse('1010-10-10').date().
        float_prop (float):  Default: 3.14.
        int_prop (int):  Default: 7.
        boolean_prop (bool):
        list_prop (List[AnEnum]):
        union_prop (Union[float, str]):  Default: 'not a float'.
        union_prop_with_ref (Union[AnEnum, None, Unset, float]):  Default: 0.6.
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
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


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
    model_prop: "ModelWithUnionProperty",
    required_model_prop: "ModelWithUnionProperty",
) -> Optional[Union[Any, HTTPValidationError]]:
    """Defaults

    Args:
        string_prop (str):  Default: 'the default string'.
        date_prop (datetime.date):  Default: isoparse('1010-10-10').date().
        float_prop (float):  Default: 3.14.
        int_prop (int):  Default: 7.
        boolean_prop (bool):
        list_prop (List[AnEnum]):
        union_prop (Union[float, str]):  Default: 'not a float'.
        union_prop_with_ref (Union[AnEnum, None, Unset, float]):  Default: 0.6.
        enum_prop (AnEnum): For testing Enums in all the ways they can be used
        model_prop (ModelWithUnionProperty):
        required_model_prop (ModelWithUnionProperty):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

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
