from typing import Optional

import httpx

Client = httpx.Client

from ...models.json_body import JsonBody
from ...models.response_200 import Response_200


def _parse_response(*, response: httpx.Response) -> Optional[Response_200]:
    if response.status_code == 200:
        response_200 = Response_200.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> httpx.Response[Response_200]:
    return httpx.Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def httpx_request(
    *,
    client: Client,
    json_body: JsonBody,
) -> httpx.Response[Response_200]:

    json_json_body = json_body.to_dict()

    response = client.request(
        "post",
        "/tests/inline_objects",
        json=json_json_body,
    )

    return _build_response(response=response)
