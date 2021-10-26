from typing import Any, Dict

import httpx

from ...client import Client
from ...models.a_form_data import AFormData
from ...types import HTTP_CALL_LOGGER, Response


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
    HTTP_CALL_LOGGER.info(f"Calling POST '{url_full}'")
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
    form_data: AFormData,
) -> Response[Any]:
    kwargs = _get_kwargs(
        client=client,
        form_data=form_data,
    )

    _log_before_call(kwargs=kwargs)
    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: Client,
    form_data: AFormData,
) -> Response[Any]:
    kwargs = _get_kwargs(
        client=client,
        form_data=form_data,
    )

    async with httpx.AsyncClient() as _client:
        _log_before_call(kwargs=kwargs)
        response = await _client.post(**kwargs)

    return _build_response(response=response)
