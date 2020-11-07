from typing import Optional

import httpx

Client = httpx.Client

from io import BytesIO

from ...types import File


def _parse_response(*, response: httpx.Response) -> Optional[File]:
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.content))

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> httpx.Response[File]:
    return httpx.Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def httpx_request(
    *,
    client: Client,
) -> httpx.Response[File]:

    response = client.request(
        "get",
        "/tests/octet_stream",
    )

    return _build_response(response=response)
