import httpx

from ...types import Response

Client = httpx.Client


def _build_response(*, response: httpx.Response) -> Response[None]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def httpx_request(
    *,
    client: Client,
) -> Response[None]:

    response = client.request(
        "get",
        "/tests/no_response",
    )

    return _build_response(response=response)
