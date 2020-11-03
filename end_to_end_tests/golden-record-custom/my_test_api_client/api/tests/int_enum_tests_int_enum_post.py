from typing import Optional

import httpx

Client = httpx.Client

from typing import Dict, cast

from ...models.an_int_enum import AnIntEnum
from ...models.http_validation_error import HTTPValidationError


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, HTTPValidationError]]:
    if response.status_code == 200:
        return None
    if response.status_code == 422:
        return HTTPValidationError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> httpx.Response[Union[None, HTTPValidationError]]:
    return httpx.Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def httpx_request(
    *,
    client: Client,
    int_enum: AnIntEnum,
) -> httpx.Response[Union[None, HTTPValidationError]]:

    json_int_enum = int_enum.value

    params: Dict[str, Any] = {
        "int_enum": json_int_enum,
    }

    response = client.request(
        "post",
        "/tests/int_enum",
        params=params,
    )

    return _build_response(response=response)
