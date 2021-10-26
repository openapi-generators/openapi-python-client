from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.http_validation_error import HTTPValidationError
from ...types import HTTP_CALL_LOGGER, UNSET, File, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    multipart_data: List[File],
    keep_alive: Union[Unset, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/tests/upload/multiple".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if keep_alive is not UNSET:
        headers["keep-alive"] = keep_alive

    multipart_multipart_data = []
    for multipart_data_item_data in multipart_data:
        multipart_data_item = multipart_data_item_data.to_tuple()

        multipart_multipart_data.append(multipart_data_item)

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "files": multipart_multipart_data,
        "verify": client.verify_ssl,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = response.json()

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, HTTPValidationError]]:
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
    multipart_data: List[File],
    keep_alive: Union[Unset, bool] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        multipart_data=multipart_data,
        keep_alive=keep_alive,
    )

    _log_before_call(kwargs=kwargs)
    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    multipart_data: List[File],
    keep_alive: Union[Unset, bool] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Upload several files in the same request"""

    return sync_detailed(
        client=client,
        multipart_data=multipart_data,
        keep_alive=keep_alive,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    multipart_data: List[File],
    keep_alive: Union[Unset, bool] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        multipart_data=multipart_data,
        keep_alive=keep_alive,
    )

    async with httpx.AsyncClient() as _client:
        _log_before_call(kwargs=kwargs)
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    multipart_data: List[File],
    keep_alive: Union[Unset, bool] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Upload several files in the same request"""

    return (
        await asyncio_detailed(
            client=client,
            multipart_data=multipart_data,
            keep_alive=keep_alive,
        )
    ).parsed
