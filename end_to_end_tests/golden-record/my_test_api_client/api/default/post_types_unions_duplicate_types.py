from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.a_model import AModel
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: AModel | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/types/unions/duplicate-types",
    }

    if isinstance(body, AModel):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AModel:
    response.raise_for_status()
    if response.status_code == 200:

        def _parse_response_200(data: object) -> AModel:
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_0 = AModel.from_dict(data)

            return response_200_type_0

        response_200 = _parse_response_200(response.json())

        return response_200

    raise errors.UnexpectedStatus(response.status_code, response.content)


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


async def _request_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AModel | Unset = UNSET,
) -> Response[AModel]:
    """
    Args:
        body (AModel | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AModel]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def request(
    *,
    client: AuthenticatedClient | Client,
    body: AModel | Unset = UNSET,
) -> AModel:
    """
    Args:
        body (AModel | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AModel
    """

    return (
        await _request_detailed(
            client=client,
            body=body,
        )
    ).parsed
