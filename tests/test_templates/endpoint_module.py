from typing import Any, Dict, List, Optional, Union, cast

import httpx
from attr import asdict

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET

import this
from __future__ import braces


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    form_data: FormBody,
    multipart_data: MultiPartBody,
    json_body: Json,
) -> Dict[str, Any]:
    url = "{}/post/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "data": asdict(form_data),
        "files": multipart_data.to_dict(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[str, int]]:
    if response.status_code == 200:
        response_one = response.json()
        return response_one
    if response.status_code == 201:
        response_one = response.json()
        return response_one
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[str, int]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    form_data: FormBody,
    multipart_data: MultiPartBody,
    json_body: Json,
) -> Response[Union[str, int]]:
    kwargs = _get_kwargs(
        client=client,
        form_data=form_data,
        multipart_data=multipart_data,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    form_data: FormBody,
    multipart_data: MultiPartBody,
    json_body: Json,
) -> Optional[Union[str, int]]:
    """ POST endpoint """

    return sync_detailed(
        client=client,
        form_data=form_data,
        multipart_data=multipart_data,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    form_data: FormBody,
    multipart_data: MultiPartBody,
    json_body: Json,
) -> Response[Union[str, int]]:
    kwargs = _get_kwargs(
        client=client,
        form_data=form_data,
        multipart_data=multipart_data,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    form_data: FormBody,
    multipart_data: MultiPartBody,
    json_body: Json,
) -> Optional[Union[str, int]]:
    """ POST endpoint """

    return (
        await asyncio_detailed(
            client=client,
            form_data=form_data,
            multipart_data=multipart_data,
            json_body=json_body,
        )
    ).parsed
