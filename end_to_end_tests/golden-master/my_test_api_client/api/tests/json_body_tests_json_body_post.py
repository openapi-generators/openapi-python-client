from dataclasses import asdict
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...errors import ApiResponseError
from ...models.a_model import AModel
from ...models.http_validation_error import HTTPValidationError


def _get_kwargs(*, client: Client, json_body: AModel,) -> Dict[str, Any]:
    url = "{}/tests/json_body".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "json": json_json_body,
    }


def _parse_response(
    *, response: httpx.Response
) -> Union[
    None, HTTPValidationError,
]:
    if response.status_code == 200:
        return None
    if response.status_code == 422:
        return HTTPValidationError.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)


def sync(
    *, client: Client, json_body: AModel,
) -> Union[
    None, HTTPValidationError,
]:
    """ Try sending a JSON body  """

    kwargs = _get_kwargs(client=client, json_body=json_body,)

    response = httpx.post(**kwargs,)

    return _parse_response(response=response)


async def asyncio(
    *, client: Client, json_body: AModel,
) -> Union[
    None, HTTPValidationError,
]:
    """ Try sending a JSON body  """
    kwargs = _get_kwargs(client=client, json_body=json_body,)

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _parse_response(response=response)
