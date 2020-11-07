from typing import Optional

import httpx

from ...types import Response

Client = httpx.Client

from typing import List, cast


def _parse_response(*, response: httpx.Response) -> Optional[List[str]]:
    if response.status_code == 200:
        response_200 = cast(List[str], response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[str]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def httpx_request(
    *,
    client: Client,
) -> Response[List[str]]:

    response = client.request(
        "get",
        "/tests/basic_lists/strings",
    )

    return _build_response(response=response)
