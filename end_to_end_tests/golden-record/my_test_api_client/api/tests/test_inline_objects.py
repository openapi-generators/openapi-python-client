from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.test_inline_objects_json_body import TestInlineObjectsJsonBody
from ...models.test_inline_objects_response_200 import TestInlineObjectsResponse200
from ...types import HTTP_CALL_LOGGER, Response


def _get_kwargs(
    *,
    client: Client,
    json_body: TestInlineObjectsJsonBody,
) -> Dict[str, Any]:
    url = "{}/tests/inline_objects".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "verify": client.verify_ssl,
    }


def _parse_response(*, response: httpx.Response) -> Optional[TestInlineObjectsResponse200]:
    if response.status_code == 200:
        response_200 = TestInlineObjectsResponse200.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[TestInlineObjectsResponse200]:
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
    json_body: TestInlineObjectsJsonBody,
) -> Response[TestInlineObjectsResponse200]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    _log_before_call(kwargs=kwargs)
    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: TestInlineObjectsJsonBody,
) -> Optional[TestInlineObjectsResponse200]:
    """ """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: TestInlineObjectsJsonBody,
) -> Response[TestInlineObjectsResponse200]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        _log_before_call(kwargs=kwargs)
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: TestInlineObjectsJsonBody,
) -> Optional[TestInlineObjectsResponse200]:
    """ """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
