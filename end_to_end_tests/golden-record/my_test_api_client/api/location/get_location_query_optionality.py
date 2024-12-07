import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    not_null_required: datetime.datetime,
    null_required: Union[None, datetime.datetime],
    null_not_required: Union[None, Unset, datetime.datetime] = UNSET,
    not_null_not_required: Union[Unset, datetime.datetime] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_not_null_required = not_null_required.isoformat()
    params["not_null_required"] = json_not_null_required

    json_null_required: Union[None, str]
    if isinstance(null_required, datetime.datetime):
        json_null_required = null_required.isoformat()
    else:
        json_null_required = null_required
    params["null_required"] = json_null_required

    json_null_not_required: Union[None, Unset, str]
    if isinstance(null_not_required, Unset):
        json_null_not_required = UNSET
    elif isinstance(null_not_required, datetime.datetime):
        json_null_not_required = null_not_required.isoformat()
    else:
        json_null_not_required = null_not_required
    params["null_not_required"] = json_null_not_required

    json_not_null_not_required: Union[Unset, str] = UNSET
    if not isinstance(not_null_not_required, Unset):
        json_not_null_not_required = not_null_not_required.isoformat()
    params["not_null_not_required"] = json_not_null_not_required

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/location/query/optionality",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == 200:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    not_null_required: datetime.datetime,
    null_required: Union[None, datetime.datetime],
    null_not_required: Union[None, Unset, datetime.datetime] = UNSET,
    not_null_not_required: Union[Unset, datetime.datetime] = UNSET,
) -> Response[Any]:
    """
    Args:
        not_null_required (datetime.datetime):
        null_required (Union[None, datetime.datetime]):
        null_not_required (Union[None, Unset, datetime.datetime]):
        not_null_not_required (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        not_null_required=not_null_required,
        null_required=null_required,
        null_not_required=null_not_required,
        not_null_not_required=not_null_not_required,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    not_null_required: datetime.datetime,
    null_required: Union[None, datetime.datetime],
    null_not_required: Union[None, Unset, datetime.datetime] = UNSET,
    not_null_not_required: Union[Unset, datetime.datetime] = UNSET,
) -> Response[Any]:
    """
    Args:
        not_null_required (datetime.datetime):
        null_required (Union[None, datetime.datetime]):
        null_not_required (Union[None, Unset, datetime.datetime]):
        not_null_not_required (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        not_null_required=not_null_required,
        null_required=null_required,
        null_not_required=null_not_required,
        not_null_not_required=not_null_not_required,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
