import datetime
from dataclasses import asdict
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...errors import ApiResponseError
from ...models.a_model import AModel
from ...models.an_enum import AnEnum
from ...models.http_validation_error import HTTPValidationError


def _get_kwargs(
    *, client: Client, an_enum_value: List[AnEnum], some_date: Union[datetime.date, datetime.datetime],
) -> Dict[str, Any]:
    url = "{}/tests/".format(client.base_url)

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

    return {
        "url": url,
        "headers": headers,
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Union[
    List[AModel], HTTPValidationError,
]:
    if response.status_code == 200:
        return [AModel.from_dict(item) for item in cast(List[Dict[str, Any]], response.json())]
    if response.status_code == 422:
        return HTTPValidationError.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)


def sync(
    *, client: Client, an_enum_value: List[AnEnum], some_date: Union[datetime.date, datetime.datetime],
) -> Union[
    List[AModel], HTTPValidationError,
]:
    """ Get a list of things  """

    kwargs = _get_kwargs(client=client, an_enum_value=an_enum_value, some_date=some_date,)

    response = httpx.get(**kwargs,)

    return _parse_response(response=response)


async def asyncio(
    *, client: Client, an_enum_value: List[AnEnum], some_date: Union[datetime.date, datetime.datetime],
) -> Union[
    List[AModel], HTTPValidationError,
]:
    """ Get a list of things  """
    kwargs = _get_kwargs(client=client, an_enum_value=an_enum_value, some_date=some_date,)

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _parse_response(response=response)
