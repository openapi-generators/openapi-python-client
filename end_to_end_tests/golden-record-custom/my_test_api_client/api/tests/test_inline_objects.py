import httpx

Client = httpx.Client

from ...models.json_body import JsonBody


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
    json_body: JsonBody,
) -> httpx.Response[None]:

    json_json_body = json_body.to_dict()

    response = client.request(
        "post",
        "/tests/inline_objects",
        json=json_json_body,
    )

    return _build_response(response=response)
