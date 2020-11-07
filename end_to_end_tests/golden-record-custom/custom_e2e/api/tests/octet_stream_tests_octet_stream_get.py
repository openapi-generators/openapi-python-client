from typing import Optional

import httpx

Client = httpx.Client


def _parse_response(*, response: httpx.Response) -> Optional[bytes]:
    if response.status_code == 200:
        return bytes(response.content)
    return None


def _build_response(*, response: httpx.Response) -> httpx.Response[bytes]:
    return httpx.Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def httpx_request(
    *,
    client: Client,
) -> httpx.Response[bytes]:

    response = client.request(
        "get",
        "/tests/octet_stream",
    )

    return _build_response(response=response)
