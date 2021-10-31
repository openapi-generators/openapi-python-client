import datetime
from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.a_model import AModel
from ...models.an_enum import AnEnum
from ...models.an_enum_with_null import AnEnumWithNull
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: Client,
    an_enum_value: List[AnEnum],
    an_enum_value_with_null: List[Optional[AnEnumWithNull]],
    an_enum_value_with_only_null: List[None],
    some_date: Union[datetime.date, datetime.datetime],
) -> Dict[str, Any]:
    url = "{}/tests/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_an_enum_value = []
    for an_enum_value_item_data in an_enum_value:
        an_enum_value_item = an_enum_value_item_data.value

        json_an_enum_value.append(an_enum_value_item)

    json_an_enum_value_with_null = []
    for an_enum_value_with_null_item_data in an_enum_value_with_null:
        an_enum_value_with_null_item = (
            an_enum_value_with_null_item_data.value if an_enum_value_with_null_item_data else None
        )

        json_an_enum_value_with_null.append(an_enum_value_with_null_item)

    json_an_enum_value_with_only_null = an_enum_value_with_only_null

    if isinstance(some_date, datetime.date):
        json_some_date = some_date.isoformat()
    else:
        json_some_date = some_date.isoformat()

    params: Dict[str, Any] = {
        "an_enum_value": json_an_enum_value,
        "an_enum_value_with_null": json_an_enum_value_with_null,
        "an_enum_value_with_only_null": json_an_enum_value_with_only_null,
        "some_date": json_some_date,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[HTTPValidationError, List[AModel]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AModel.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if response.status_code == 423:
        response_423 = HTTPValidationError.from_dict(response.json())

        return response_423
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[HTTPValidationError, List[AModel]]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    an_enum_value: List[AnEnum],
    an_enum_value_with_null: List[Optional[AnEnumWithNull]],
    an_enum_value_with_only_null: List[None],
    some_date: Union[datetime.date, datetime.datetime],
) -> Response[Union[HTTPValidationError, List[AModel]]]:
    kwargs = _get_kwargs(
        client=client,
        an_enum_value=an_enum_value,
        an_enum_value_with_null=an_enum_value_with_null,
        an_enum_value_with_only_null=an_enum_value_with_only_null,
        some_date=some_date,
    )

    response = httpx.get(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    an_enum_value: List[AnEnum],
    an_enum_value_with_null: List[Optional[AnEnumWithNull]],
    an_enum_value_with_only_null: List[None],
    some_date: Union[datetime.date, datetime.datetime],
) -> Optional[Union[HTTPValidationError, List[AModel]]]:
    """Get a list of things"""

    return sync_detailed(
        client=client,
        an_enum_value=an_enum_value,
        an_enum_value_with_null=an_enum_value_with_null,
        an_enum_value_with_only_null=an_enum_value_with_only_null,
        some_date=some_date,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    an_enum_value: List[AnEnum],
    an_enum_value_with_null: List[Optional[AnEnumWithNull]],
    an_enum_value_with_only_null: List[None],
    some_date: Union[datetime.date, datetime.datetime],
) -> Response[Union[HTTPValidationError, List[AModel]]]:
    kwargs = _get_kwargs(
        client=client,
        an_enum_value=an_enum_value,
        an_enum_value_with_null=an_enum_value_with_null,
        an_enum_value_with_only_null=an_enum_value_with_only_null,
        some_date=some_date,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    an_enum_value: List[AnEnum],
    an_enum_value_with_null: List[Optional[AnEnumWithNull]],
    an_enum_value_with_only_null: List[None],
    some_date: Union[datetime.date, datetime.datetime],
) -> Optional[Union[HTTPValidationError, List[AModel]]]:
    """Get a list of things"""

    return (
        await asyncio_detailed(
            client=client,
            an_enum_value=an_enum_value,
            an_enum_value_with_null=an_enum_value_with_null,
            an_enum_value_with_only_null=an_enum_value_with_only_null,
            some_date=some_date,
        )
    ).parsed
