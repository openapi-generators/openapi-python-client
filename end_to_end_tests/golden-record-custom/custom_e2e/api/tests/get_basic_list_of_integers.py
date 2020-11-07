from typing import Optional

import httpx

Client = httpx.Client


def _parse_response(*, response: httpx.Response) -> Optional[List[int]]:
    if response.status_code == 200:
        return [int(item) for item in cast(List[int], response.json())]
    return None


def _build_response(*, response: httpx.Response) -> httpx.Response[List[int]]:
    return httpx.Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def httpx_request(
    *,
    client: Client,
) -> httpx.Response[List[int]]:

    response = client.request(
        "get",
        "/tests/basic_lists/integers",
    )

    return _build_response(response=response)
