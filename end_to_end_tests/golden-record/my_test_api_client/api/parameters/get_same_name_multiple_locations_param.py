from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import HTTP_CALL_LOGGER, UNSET, Response, Unset


def _get_kwargs(
    param_path: str,
    *,
    client: Client,
    param_query: Union[Unset, None, str] = UNSET,
    param_header: Union[Unset, str] = UNSET,
    param_cookie: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/same-name-multiple-locations/{param}".format(client.base_url, param=param_path)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if param_header is not UNSET:
        headers["param"] = param_header

    if param_cookie is not UNSET:
        cookies["param"] = param_cookie

    params: Dict[str, Any] = {
        "param": param_query,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
        "verify": client.verify_ssl,
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
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
    param_path: str,
    *,
    client: Client,
    param_query: Union[Unset, None, str] = UNSET,
    param_header: Union[Unset, str] = UNSET,
    param_cookie: Union[Unset, str] = UNSET,
) -> Response[Any]:
    kwargs = _get_kwargs(
        param_path=param_path,
        client=client,
        param_query=param_query,
        param_header=param_header,
        param_cookie=param_cookie,
    )

    _log_before_call(kwargs=kwargs)
    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    param_path: str,
    *,
    client: Client,
    param_query: Union[Unset, None, str] = UNSET,
    param_header: Union[Unset, str] = UNSET,
    param_cookie: Union[Unset, str] = UNSET,
) -> Response[Any]:
    kwargs = _get_kwargs(
        param_path=param_path,
        client=client,
        param_query=param_query,
        param_header=param_header,
        param_cookie=param_cookie,
    )

    async with httpx.AsyncClient() as _client:
        _log_before_call(kwargs=kwargs)
        response = await _client.get(**kwargs)

    return _build_response(response=response)
