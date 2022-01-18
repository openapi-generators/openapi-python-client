import datetime
from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    not_null_required: datetime.datetime,
    null_required: Union[Unset, None, datetime.datetime] = UNSET,
    null_not_required: Union[Unset, None, datetime.datetime] = UNSET,
    not_null_not_required: Union[Unset, None, datetime.datetime] = UNSET,
) -> Dict[str, Any]:
    url = "{}/location/query/optionality".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_not_null_required = not_null_required.isoformat()

    params["not_null_required"] = json_not_null_required

    json_null_required: Union[Unset, None, str] = UNSET
    if not isinstance(null_required, Unset):
        json_null_required = null_required.isoformat() if null_required else None

    params["null_required"] = json_null_required

    json_null_not_required: Union[Unset, None, str] = UNSET
    if not isinstance(null_not_required, Unset):
        json_null_not_required = null_not_required.isoformat() if null_not_required else None

    params["null_not_required"] = json_null_not_required

    json_not_null_not_required: Union[Unset, None, str] = UNSET
    if not isinstance(not_null_not_required, Unset):
        json_not_null_not_required = not_null_not_required.isoformat() if not_null_not_required else None

    params["not_null_not_required"] = json_not_null_not_required

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    *,
    client: Client,
    not_null_required: datetime.datetime,
    null_required: Union[Unset, None, datetime.datetime] = UNSET,
    null_not_required: Union[Unset, None, datetime.datetime] = UNSET,
    not_null_not_required: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[Any]:
    """
    Args:
        not_null_required (datetime.datetime):
        null_required (Union[Unset, None, datetime.datetime]):
        null_not_required (Union[Unset, None, datetime.datetime]):
        not_null_not_required (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        not_null_required=not_null_required,
        null_required=null_required,
        null_not_required=null_not_required,
        not_null_not_required=not_null_not_required,
    )

    response = httpx.request(
        verify=client.verify_ssl,
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
    """
    Args:
        not_null_required (datetime.datetime):
        null_required (Union[Unset, None, datetime.datetime]):
        null_not_required (Union[Unset, None, datetime.datetime]):
        not_null_not_required (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        not_null_required=not_null_required,
        null_required=null_required,
        null_not_required=null_not_required,
        not_null_not_required=not_null_not_required,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
