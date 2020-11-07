from typing import Optional

import httpx

Client = httpx.Client

from typing import Dict, cast

from ...models.a_model import AModel
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
    json_body: AModel,
) -> httpx.Response[Union[None, HTTPValidationError]]:

    json_json_body = json_body.to_dict()

    response = client.request(
        "post",
        "/tests/json_body",
        json=json_json_body,
    )

    return _build_response(response=response)
