import datetime
from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import HTTP_CALL_LOGGER, UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    not_null_required: datetime.datetime,
    null_required: Union[Unset, None, datetime.datetime] = UNSET,
    null_not_required: Union[Unset, None, datetime.datetime] = UNSET,
    not_null_not_required: Union[Unset, None, datetime.datetime] = UNSET,
) -> Dict[str, Any]:
    url = "{}/location/query/optionality".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_not_null_required = not_null_required.isoformat()

    json_null_required: Union[Unset, None, str] = UNSET
    if not isinstance(null_required, Unset):
        json_null_required = null_required.isoformat() if null_required else None

    json_null_not_required: Union[Unset, None, str] = UNSET
    if not isinstance(null_not_required, Unset):
        json_null_not_required = null_not_required.isoformat() if null_not_required else None

    json_not_null_not_required: Union[Unset, None, str] = UNSET
    if not isinstance(not_null_not_required, Unset):
        json_not_null_not_required = not_null_not_required.isoformat() if not_null_not_required else None

    params: Dict[str, Any] = {
        "not_null_required": json_not_null_required,
        "null_required": json_null_required,
        "null_not_required": json_null_not_required,
        "not_null_not_required": json_not_null_not_required,
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
    *,
    client: Client,
    not_null_required: datetime.datetime,
    null_required: Union[Unset, None, datetime.datetime] = UNSET,
    null_not_required: Union[Unset, None, datetime.datetime] = UNSET,
    not_null_not_required: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[Any]:
    kwargs = _get_kwargs(
        client=client,
        not_null_required=not_null_required,
        null_required=null_required,
        null_not_required=null_not_required,
        not_null_not_required=not_null_not_required,
    )

    _log_before_call(kwargs=kwargs)
    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: Client,
    not_null_required: datetime.datetime,
    null_required: Union[Unset, None, datetime.datetime] = UNSET,
    null_not_required: Union[Unset, None, datetime.datetime] = UNSET,
    not_null_not_required: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[Any]:
    kwargs = _get_kwargs(
        client=client,
        not_null_required=not_null_required,
        null_required=null_required,
        null_not_required=null_not_required,
        not_null_not_required=not_null_not_required,
    )

    async with httpx.AsyncClient() as _client:
        _log_before_call(kwargs=kwargs)
        response = await _client.get(**kwargs)

    return _build_response(response=response)
