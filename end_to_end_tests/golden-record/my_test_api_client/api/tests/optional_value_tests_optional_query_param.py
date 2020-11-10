from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    query_param: Union[Unset, List[str]] = UNSET,
) -> Dict[str, Any]:
    url = "{}/tests/optional_query_param/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_query_param: Union[Unset, List[Any]] = UNSET
    if not isinstance(query_param, Unset):
        json_query_param = query_param

    params: Dict[str, Any] = {}
    if query_param is not UNSET:
        params["query_param"] = json_query_param

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = None

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    query_param: Union[Unset, List[str]] = UNSET,
) -> Response[Union[None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        query_param=query_param,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    query_param: Union[Unset, List[str]] = UNSET,
) -> Optional[Union[None, HTTPValidationError]]:
    """ Test optional query parameters """

    return sync_detailed(
        client=client,
        query_param=query_param,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    query_param: Union[Unset, List[str]] = UNSET,
) -> Response[Union[None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        query_param=query_param,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    query_param: Union[Unset, List[str]] = UNSET,
) -> Optional[Union[None, HTTPValidationError]]:
    """ Test optional query parameters """

    return (
        await asyncio_detailed(
            client=client,
            query_param=query_param,
        )
    ).parsed
