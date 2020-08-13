import datetime
from dataclasses import asdict, field
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ..client import AuthenticatedClient, Client
from ..errors import ApiResponseError
from ..models.a_model import AModel
from ..models.an_enum import AnEnum
from ..models.body_upload_file_tests_upload_post import BodyUploadFileTestsUploadPost
from ..models.http_validation_error import HTTPValidationError


async def get_user_list(
    *, client: Client, an_enum_value: List[AnEnum], some_date: Union[datetime.date, datetime.datetime],
) -> Union[
    List[AModel], HTTPValidationError,
]:

    """ Get a list of things  """
    url = "{}/tests/".format(client.base_url,)

    headers: Dict[str, Any] = client.get_headers()

    json_an_enum_value = []
    for an_enum_value_item_data in an_enum_value:
        an_enum_value_item = an_enum_value_item_data.value

        json_an_enum_value.append(an_enum_value_item)

    if isinstance(some_date, datetime.date):
        json_some_date = some_date.isoformat()

    else:
        json_some_date = some_date.isoformat()

    params: Dict[str, Any] = {
        "an_enum_value": json_an_enum_value,
        "some_date": json_some_date,
    }

    async with httpx.AsyncClient() as _client:
        response = await _client.get(url=url, headers=headers, params=params,)

    if response.status_code == 200:
        return [AModel.from_dict(item) for item in cast(List[Dict[str, Any]], response.json())]
    if response.status_code == 422:
        return HTTPValidationError.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)


async def upload_file_tests_upload_post(
    *, client: Client, multipart_data: BodyUploadFileTestsUploadPost, keep_alive: Optional[bool] = None,
) -> Union[
    None, HTTPValidationError,
]:

    """ Upload a file  """
    url = "{}/tests/upload".format(client.base_url,)

    headers: Dict[str, Any] = client.get_headers()
    if keep_alive is not None:
        headers["keep-alive"] = keep_alive

    async with httpx.AsyncClient() as _client:
        response = await _client.post(url=url, headers=headers, files=multipart_data.to_dict(),)

    if response.status_code == 200:
        return None
    if response.status_code == 422:
        return HTTPValidationError.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)


async def json_body_tests_json_body_post(
    *, client: Client, json_body: AModel,
) -> Union[
    None, HTTPValidationError,
]:

    """ Try sending a JSON body  """
    url = "{}/tests/json_body".format(client.base_url,)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    async with httpx.AsyncClient() as _client:
        response = await _client.post(url=url, headers=headers, json=json_json_body,)

    if response.status_code == 200:
        return None
    if response.status_code == 422:
        return HTTPValidationError.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)


async def test_defaults_tests_test_defaults_post(
    *,
    client: Client,
    json_body: Dict[Any, Any],
    string_prop: Optional[str] = "the default string",
    datetime_prop: Optional[datetime.datetime] = datetime.datetime(1010, 10, 10, 0, 0),
    date_prop: Optional[datetime.date] = datetime.date(1010, 10, 10),
    float_prop: Optional[float] = 3.14,
    int_prop: Optional[int] = 7,
    boolean_prop: Optional[bool] = False,
    list_prop: Optional[List[AnEnum]] = field(
        default_factory=lambda: cast(Optional[List[AnEnum]], [AnEnum.FIRST_VALUE, AnEnum.SECOND_VALUE])
    ),
    union_prop: Optional[Union[Optional[float], Optional[str]]] = "not a float",
    enum_prop: Optional[AnEnum] = None,
) -> Union[
    None, HTTPValidationError,
]:

    """  """
    url = "{}/tests/test_defaults".format(client.base_url,)

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

    async with httpx.AsyncClient() as _client:
        response = await _client.post(url=url, headers=headers, json=json_json_body, params=params,)

    if response.status_code == 200:
        return None
    if response.status_code == 422:
        return HTTPValidationError.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)
