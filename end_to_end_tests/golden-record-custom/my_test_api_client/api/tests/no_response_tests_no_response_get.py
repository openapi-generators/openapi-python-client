import httpx

Client = httpx.Client


def _build_response(*, response: httpx.Response) -> httpx.Response[None]:
    return httpx.Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def httpx_request(
    *,
    client: Client,
) -> httpx.Response[None]:

    response = client.request(
        "get",
        "/tests/no_response",
    )

    return _build_response(response=response)
