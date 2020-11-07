from typing import Optional

import httpx

Client = httpx.Client


def _parse_response(*, response: httpx.Response) -> Optional[List[bool]]:
    if response.status_code == 200:
        return [bool(item) for item in cast(List[bool], response.json())]
    return None


def _build_response(*, response: httpx.Response) -> httpx.Response[List[bool]]:
    return httpx.Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def httpx_request(
    *,
    client: Client,
) -> httpx.Response[List[bool]]:

    response = client.request(
        "get",
        "/tests/basic_lists/booleans",
    )

    return _build_response(response=response)
