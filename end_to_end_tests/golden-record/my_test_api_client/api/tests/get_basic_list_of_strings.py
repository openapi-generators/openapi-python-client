from typing import Any, Dict, List, Optional, cast

import httpx

from ...client import Client
from ...types import HTTP_CALL_LOGGER, Response


def _get_kwargs(
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/tests/basic_lists/strings".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "verify": client.verify_ssl,
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[str]]:
    if response.status_code == 200:
        response_200 = cast(List[str], response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[str]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def _log_before_call(*, kwargs: Dict[str, Any]) -> None:
    import json
    import urllib.parse

    url_full = kwargs["url"]

    if kwargs.get("params", None):
        url_full += "?" + urllib.parse.urlencode(kwargs["params"])
    HTTP_CALL_LOGGER.info(f"Calling GET '{url_full}'")
    if kwargs.get("files"):
        HTTP_CALL_LOGGER.debug(f"with files: {kwargs['files']}")
    elif kwargs.get("dict", kwargs.get("json", None)):
        dict_string = json.dumps(kwargs.get("dict", kwargs.get("json", None)), indent=4, sort_keys=True)
        HTTP_CALL_LOGGER.debug(f"with data:\n{dict_string}")
    headers_without_auth = dict(kwargs["cookies"])
    headers_without_auth.pop("Authorization", None)
    cookies, timeout = kwargs["cookies"], kwargs["timeout"]
    HTTP_CALL_LOGGER.debug(f"{headers_without_auth=}\n{cookies=}\n{timeout=}")


def sync_detailed(
    *,
    client: Client,
) -> Response[List[str]]:
    kwargs = _get_kwargs(
        client=client,
    )

    _log_before_call(kwargs=kwargs)
    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
) -> Optional[List[str]]:
    """Get a list of strings"""

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[List[str]]:
    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient() as _client:
        _log_before_call(kwargs=kwargs)
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
) -> Optional[List[str]]:
    """Get a list of strings"""

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
