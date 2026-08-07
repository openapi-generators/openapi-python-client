from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.demo_entity_input import DemoEntityInput
from ...models.demo_entity_output import DemoEntityOutput
from ...types import Response, dump_json__for_transport


def _get_kwargs(
    *,
    body: DemoEntityInput,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/naming/duplicate-title",
    }

    _kwargs["content"] = dump_json__for_transport(body)

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DemoEntityOutput:
    if response.status_code == 200:
        response_200 = DemoEntityOutput.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return cast(DemoEntityOutput, None)


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DemoEntityOutput]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


async def _request_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: DemoEntityInput,
) -> Response[DemoEntityOutput]:
    """
    Args:
        body (DemoEntityInput):

    Raises:
        errors.UnexpectedStatus: If the server returns a status code that is not a documented
            success and Client.raise_on_unexpected_status is True. A documented error response is
            parsed onto UnexpectedStatus.parsed. With the flag set to False, those statuses return
            None instead of raising.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DemoEntityOutput]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def request(
    *,
    client: AuthenticatedClient | Client,
    body: DemoEntityInput,
) -> DemoEntityOutput:
    """
    Args:
        body (DemoEntityInput):

    Raises:
        errors.UnexpectedStatus: If the server returns a status code that is not a documented
            success and Client.raise_on_unexpected_status is True. A documented error response is
            parsed onto UnexpectedStatus.parsed. With the flag set to False, those statuses return
            None instead of raising.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DemoEntityOutput
    """

    return (
        await _request_detailed(
            client=client,
            body=body,
        )
    ).parsed
