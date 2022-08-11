from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.building_search_results import BuildingSearchResults
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    page: int = 0,
    page_size: int = 100,
    sort: Union[Unset, None, List[str]] = UNSET,
    filter_: Union[Unset, None, str] = "",
) -> Dict[str, Any]:
    url = "{}/v1/buildings".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["page"] = page

    params["page-size"] = page_size

    json_sort: Union[Unset, None, List[str]] = UNSET
    if not isinstance(sort, Unset):
        if sort is None:
            json_sort = None
        else:
            json_sort = sort

    params["sort"] = json_sort

    params["filter"] = filter_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[BuildingSearchResults]:
    if response.status_code == 200:
        response_200 = BuildingSearchResults.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[BuildingSearchResults]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    page: int = 0,
    page_size: int = 100,
    sort: Union[Unset, None, List[str]] = UNSET,
    filter_: Union[Unset, None, str] = "",
) -> Response[BuildingSearchResults]:
    """Search for sorted and paged Buildings

     Search for sorted and paged buildings

    Args:
        page (int):
        page_size (int):  Default: 100.
        sort (Union[Unset, None, List[str]]):
        filter_ (Union[Unset, None, str]):  Default: ''.

    Returns:
        Response[BuildingSearchResults]
    """

    kwargs = _get_kwargs(
        client=client,
        page=page,
        page_size=page_size,
        sort=sort,
        filter_=filter_,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    page: int = 0,
    page_size: int = 100,
    sort: Union[Unset, None, List[str]] = UNSET,
    filter_: Union[Unset, None, str] = "",
) -> Optional[BuildingSearchResults]:
    """Search for sorted and paged Buildings

     Search for sorted and paged buildings

    Args:
        page (int):
        page_size (int):  Default: 100.
        sort (Union[Unset, None, List[str]]):
        filter_ (Union[Unset, None, str]):  Default: ''.

    Returns:
        Response[BuildingSearchResults]
    """

    return sync_detailed(
        client=client,
        page=page,
        page_size=page_size,
        sort=sort,
        filter_=filter_,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page: int = 0,
    page_size: int = 100,
    sort: Union[Unset, None, List[str]] = UNSET,
    filter_: Union[Unset, None, str] = "",
) -> Response[BuildingSearchResults]:
    """Search for sorted and paged Buildings

     Search for sorted and paged buildings

    Args:
        page (int):
        page_size (int):  Default: 100.
        sort (Union[Unset, None, List[str]]):
        filter_ (Union[Unset, None, str]):  Default: ''.

    Returns:
        Response[BuildingSearchResults]
    """

    kwargs = _get_kwargs(
        client=client,
        page=page,
        page_size=page_size,
        sort=sort,
        filter_=filter_,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    page: int = 0,
    page_size: int = 100,
    sort: Union[Unset, None, List[str]] = UNSET,
    filter_: Union[Unset, None, str] = "",
) -> Optional[BuildingSearchResults]:
    """Search for sorted and paged Buildings

     Search for sorted and paged buildings

    Args:
        page (int):
        page_size (int):  Default: 100.
        sort (Union[Unset, None, List[str]]):
        filter_ (Union[Unset, None, str]):  Default: ''.

    Returns:
        Response[BuildingSearchResults]
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            page_size=page_size,
            sort=sort,
            filter_=filter_,
        )
    ).parsed
