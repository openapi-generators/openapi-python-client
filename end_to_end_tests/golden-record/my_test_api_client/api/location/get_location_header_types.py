from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    boolean_header: Union[Unset, bool] = UNSET,
    string_header: Union[Unset, str] = UNSET,
    number_header: Union[Unset, float] = UNSET,
    integer_header: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/location/header/types".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(boolean_header, Unset):
        headers["Boolean-Header"] = "true" if boolean_header else "false"

    if not isinstance(string_header, Unset):
        headers["String-Header"] = string_header

    if not isinstance(number_header, Unset):
        headers["Number-Header"] = str(number_header)

    if not isinstance(integer_header, Unset):
        headers["Integer-Header"] = str(integer_header)

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
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
    boolean_header: Union[Unset, bool] = UNSET,
    string_header: Union[Unset, str] = UNSET,
    number_header: Union[Unset, float] = UNSET,
    integer_header: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """
    Args:
        boolean_header (Union[Unset, bool]):
        string_header (Union[Unset, str]):
        number_header (Union[Unset, float]):
        integer_header (Union[Unset, int]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        boolean_header=boolean_header,
        string_header=string_header,
        number_header=number_header,
        integer_header=integer_header,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: Client,
    boolean_header: Union[Unset, bool] = UNSET,
    string_header: Union[Unset, str] = UNSET,
    number_header: Union[Unset, float] = UNSET,
    integer_header: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """
    Args:
        boolean_header (Union[Unset, bool]):
        string_header (Union[Unset, str]):
        number_header (Union[Unset, float]):
        integer_header (Union[Unset, int]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        boolean_header=boolean_header,
        string_header=string_header,
        number_header=number_header,
        integer_header=integer_header,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
