from dataclasses import asdict
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...errors import ApiResponseError


def _get_kwargs(*, client: Client,) -> Dict[str, Any]:
    url = "{}/tests/test_octet_stream".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    return {
        "url": url,
        "headers": headers,
    }


def _parse_response(*, response: httpx.Response) -> bytes:

    if response.status_code == 200:
        return bytes(response.content)
    else:
        raise ApiResponseError(response=response)


def sync(*, client: Client,) -> bytes:

    """  """

    kwargs = _get_kwargs(client=client,)

    response = httpx.get(**kwargs,)

    return _parse_response(response=response)


async def asyncio(*, client: Client,) -> bytes:

    """  """
    kwargs = _get_kwargs(client=client,)

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _parse_response(response=response)
