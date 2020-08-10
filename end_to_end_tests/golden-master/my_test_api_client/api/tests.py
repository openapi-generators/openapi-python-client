from dataclasses import asdict
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ..client import AuthenticatedClient, Client
from ..errors import ApiResponseError
from ..models.a_model import AModel
from ..models.an_enum import AnEnum
from ..models.body_upload_file_tests_upload_post import BodyUploadFileTestsUploadPost
from ..models.http_validation_error import HTTPValidationError


def get_user_list(
    *, client: Client, an_enum_value: List[AnEnum], some_date: Union[date, datetime],
) -> Union[
    List[AModel], HTTPValidationError,
]:

    """ Get a list of things  """
    url = "{}/tests/".format(client.base_url)

    json_an_enum_value = []
    for an_enum_value_item_data in an_enum_value:
        an_enum_value_item = an_enum_value_item_data.value

        json_an_enum_value.append(an_enum_value_item)

    if isinstance(some_date, date):
        json_some_date = some_date.isoformat()

    else:
        json_some_date = some_date.isoformat()

    params: Dict[str, Any] = {
        "an_enum_value": json_an_enum_value,
        "some_date": json_some_date,
    }

    response = httpx.get(url=url, headers=client.get_headers(), params=params,)

    if response.status_code == 200:
        return [AModel.from_dict(item) for item in cast(List[Dict[str, Any]], response.json())]
    if response.status_code == 422:
        return HTTPValidationError.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)


def upload_file_tests_upload_post(
    *, client: Client, multipart_data: BodyUploadFileTestsUploadPost,
) -> Union[
    None, HTTPValidationError,
]:

    """ Upload a file  """
    url = "{}/tests/upload".format(client.base_url)

    response = httpx.post(url=url, headers=client.get_headers(), files=multipart_data.to_dict(),)

    if response.status_code == 200:
        return None
    if response.status_code == 422:
        return HTTPValidationError.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)


def json_body_tests_json_body_post(
    *, client: Client, json_body: AModel,
) -> Union[
    None, HTTPValidationError,
]:

    """ Try sending a JSON body  """
    url = "{}/tests/json_body".format(client.base_url)

    json_json_body = json_body.to_dict()

    response = httpx.post(url=url, headers=client.get_headers(), json=json_json_body,)

    if response.status_code == 200:
        return None
    if response.status_code == 422:
        return HTTPValidationError.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)
