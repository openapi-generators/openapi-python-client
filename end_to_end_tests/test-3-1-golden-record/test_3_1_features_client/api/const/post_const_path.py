from http import HTTPStatus
from typing import Any, Dict, Literal, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_const_path_json_body import PostConstPathJsonBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
    path: Literal["this goes in the path"],
    *,
    json_body: PostConstPathJsonBody,
    required_query: Literal["this always goes in the query"],
    optional_query: Union[Literal["this sometimes goes in the query"], Unset] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    params["required query"] = required_query

    params["optional query"] = optional_query

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/const/{path}".format(
            path=path,
        ),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Literal["Why have a fixed response? I dunno"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(Literal["Why have a fixed response? I dunno"], response.json())
        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Literal["Why have a fixed response? I dunno"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    path: Literal["this goes in the path"],
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: PostConstPathJsonBody,
    required_query: Literal["this always goes in the query"],
    optional_query: Union[Literal["this sometimes goes in the query"], Unset] = UNSET,
) -> Response[Literal["Why have a fixed response? I dunno"]]:
    """
    Args:
        path (Literal['this goes in the path']):
        required_query (Literal['this always goes in the query']):
        optional_query (Union[Literal['this sometimes goes in the query'], Unset]):
        json_body (PostConstPathJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Literal['Why have a fixed response? I dunno']]
    """

    kwargs = _get_kwargs(
        path=path,
        json_body=json_body,
        required_query=required_query,
        optional_query=optional_query,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    path: Literal["this goes in the path"],
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: PostConstPathJsonBody,
    required_query: Literal["this always goes in the query"],
    optional_query: Union[Literal["this sometimes goes in the query"], Unset] = UNSET,
) -> Optional[Literal["Why have a fixed response? I dunno"]]:
    """
    Args:
        path (Literal['this goes in the path']):
        required_query (Literal['this always goes in the query']):
        optional_query (Union[Literal['this sometimes goes in the query'], Unset]):
        json_body (PostConstPathJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Literal['Why have a fixed response? I dunno']
    """

    return sync_detailed(
        path=path,
        client=client,
        json_body=json_body,
        required_query=required_query,
        optional_query=optional_query,
    ).parsed


async def asyncio_detailed(
    path: Literal["this goes in the path"],
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: PostConstPathJsonBody,
    required_query: Literal["this always goes in the query"],
    optional_query: Union[Literal["this sometimes goes in the query"], Unset] = UNSET,
) -> Response[Literal["Why have a fixed response? I dunno"]]:
    """
    Args:
        path (Literal['this goes in the path']):
        required_query (Literal['this always goes in the query']):
        optional_query (Union[Literal['this sometimes goes in the query'], Unset]):
        json_body (PostConstPathJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Literal['Why have a fixed response? I dunno']]
    """

    kwargs = _get_kwargs(
        path=path,
        json_body=json_body,
        required_query=required_query,
        optional_query=optional_query,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    path: Literal["this goes in the path"],
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: PostConstPathJsonBody,
    required_query: Literal["this always goes in the query"],
    optional_query: Union[Literal["this sometimes goes in the query"], Unset] = UNSET,
) -> Optional[Literal["Why have a fixed response? I dunno"]]:
    """
    Args:
        path (Literal['this goes in the path']):
        required_query (Literal['this always goes in the query']):
        optional_query (Union[Literal['this sometimes goes in the query'], Unset]):
        json_body (PostConstPathJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Literal['Why have a fixed response? I dunno']
    """

    return (
        await asyncio_detailed(
            path=path,
            client=client,
            json_body=json_body,
            required_query=required_query,
            optional_query=optional_query,
        )
    ).parsed