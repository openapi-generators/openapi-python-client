from typing import Optional

import httpx

from ...types import Response

Client = httpx.Client

from typing import Dict

from ...models.an_int_enum import AnIntEnum
from ...models.http_validation_error import HTTPValidationError


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = None

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def httpx_request(
    *,
    client: Client,
    int_enum: AnIntEnum,
) -> Response[Union[None, HTTPValidationError]]:

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
