from typing import Optional

import httpx

from ...types import Response

Client = httpx.Client


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None]]:
    if response.status_code == 200:
        response_200 = None

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def httpx_request(
    *,
    client: Client,
    my_token: str,
) -> Response[Union[None, None]]:

    response = client.request(
        "get",
        "/auth/token_with_cookie",
    )

    return _build_response(response=response)
