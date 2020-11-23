from typing import Optional

import httpx

from ...types import Response

Client = httpx.Client

from ...models.test_inline_objects_json_body import TestInlineObjects_JsonBody
from ...models.test_inline_objects_response_200 import TestInlineObjects_Response_200


def _parse_response(*, response: httpx.Response) -> Optional[TestInlineObjects_Response_200]:
    if response.status_code == 200:
        response_200 = TestInlineObjects_Response_200.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[TestInlineObjects_Response_200]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def httpx_request(
    *,
    client: Client,
    json_body: TestInlineObjects_JsonBody,
) -> Response[TestInlineObjects_Response_200]:

    json_json_body = json_body.to_dict()

    response = client.request(
        "post",
        "/tests/inline_objects",
        json=json_json_body,
    )

    return _build_response(response=response)
