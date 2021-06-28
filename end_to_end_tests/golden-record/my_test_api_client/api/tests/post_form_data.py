from typing import Any, Dict

import httpx

from ...client import Client
from ...models.a_form_data import AFormData
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    form_data: AFormData,
) -> Dict[str, Any]:
    url = "{}/tests/post_form_data".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "data": form_data.to_dict(),
    }


def _build_response(*, response: httpx.Response) -> Response[None]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    *,
    client: Client,
    form_data: AFormData,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        form_data=form_data,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: Client,
    form_data: AFormData,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        form_data=form_data,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)
