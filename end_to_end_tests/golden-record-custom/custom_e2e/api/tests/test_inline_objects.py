from typing import Optional

import httpx

from ...types import Response

Client = httpx.Client

from ...models.test_inline_objectsjson_body import TestInlineObjectsjsonBody
from ...models.test_inline_objectsresponse_200 import TestInlineObjectsresponse_200


def _parse_response(*, response: httpx.Response) -> Optional[TestInlineObjectsresponse_200]:
    if response.status_code == 200:
        response_200 = TestInlineObjectsresponse_200.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[TestInlineObjectsresponse_200]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def httpx_request(
    *,
    client: Client,
    json_body: TestInlineObjectsjsonBody,
) -> Response[TestInlineObjectsresponse_200]:

    json_json_body = json_body.to_dict()

    response = client.request(
        "post",
        "/tests/inline_objects",
        json=json_json_body,
    )

    return _build_response(response=response)
