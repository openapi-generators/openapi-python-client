from typing import Optional

import httpx

from ...types import Response

Client = httpx.Client

import datetime
from typing import Dict, List, Union

from ...models.a_model import AModel
from ...models.an_enum import AnEnum
from ...models.http_validation_error import HTTPValidationError


def _parse_response(*, response: httpx.Response) -> Optional[Union[List[AModel], HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = []
        for response_200_item_data in response.json():
            response_200_item = AModel.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[List[AModel], HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def httpx_request(
    *,
    client: Client,
    an_enum_value: List[AnEnum],
    some_date: Union[datetime.date, datetime.datetime],
) -> Response[Union[List[AModel], HTTPValidationError]]:

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

    response = client.request(
        "get",
        "/tests/",
        params=params,
    )

    return _build_response(response=response)
