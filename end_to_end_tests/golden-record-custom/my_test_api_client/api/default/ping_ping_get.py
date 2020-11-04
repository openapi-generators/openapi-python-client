from typing import Optional

import httpx

Client = httpx.Client


def _parse_response(*, response: httpx.Response) -> Optional[bool]:
    if response.status_code == 200:
        return bool(response.text)
    return None


def _build_response(*, response: httpx.Response) -> httpx.Response[bool]:
    return httpx.Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def httpx_request(
    *,
    client: Client,
) -> httpx.Response[bool]:

    response = client.request(
        "get",
        "/ping",
    )

    return _build_response(response=response)
