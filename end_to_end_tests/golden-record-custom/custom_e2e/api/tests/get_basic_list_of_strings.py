from typing import Optional

import httpx

Client = httpx.Client


def _parse_response(*, response: httpx.Response) -> Optional[List[str]]:
    if response.status_code == 200:
        return [str(item) for item in cast(List[str], response.json())]
    return None


def _build_response(*, response: httpx.Response) -> httpx.Response[List[str]]:
    return httpx.Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def httpx_request(
    *,
    client: Client,
) -> httpx.Response[List[str]]:

    response = client.request(
        "get",
        "/tests/basic_lists/strings",
    )

    return _build_response(response=response)
