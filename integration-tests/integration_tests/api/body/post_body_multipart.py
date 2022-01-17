from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.post_body_multipart_multipart_data import PostBodyMultipartMultipartData
from ...models.post_body_multipart_response_200 import PostBodyMultipartResponse200
from ...models.public_error import PublicError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    multipart_data: PostBodyMultipartMultipartData,
) -> Dict[str, Any]:
    url = "{}/body/multipart".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "files": multipart_multipart_data,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[PostBodyMultipartResponse200, PublicError]]:
    if response.status_code == 200:
        response_200 = PostBodyMultipartResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = PublicError.from_dict(response.json())

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[PostBodyMultipartResponse200, PublicError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    multipart_data: PostBodyMultipartMultipartData,
) -> Response[Union[PostBodyMultipartResponse200, PublicError]]:
    """
    Args:
        multipart_data (PostBodyMultipartMultipartData):

    Returns:
        Response[Union[PostBodyMultipartResponse200, PublicError]]
    """

    kwargs = _get_kwargs(
        client=client,
        multipart_data=multipart_data,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    multipart_data: PostBodyMultipartMultipartData,
) -> Optional[Union[PostBodyMultipartResponse200, PublicError]]:
    """
    Args:
        multipart_data (PostBodyMultipartMultipartData):

    Returns:
        Response[Union[PostBodyMultipartResponse200, PublicError]]
    """

    return sync_detailed(
        client=client,
        multipart_data=multipart_data,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    multipart_data: PostBodyMultipartMultipartData,
) -> Response[Union[PostBodyMultipartResponse200, PublicError]]:
    """
    Args:
        multipart_data (PostBodyMultipartMultipartData):

    Returns:
        Response[Union[PostBodyMultipartResponse200, PublicError]]
    """

    kwargs = _get_kwargs(
        client=client,
        multipart_data=multipart_data,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    multipart_data: PostBodyMultipartMultipartData,
) -> Optional[Union[PostBodyMultipartResponse200, PublicError]]:
    """
    Args:
        multipart_data (PostBodyMultipartMultipartData):

    Returns:
        Response[Union[PostBodyMultipartResponse200, PublicError]]
    """

    return (
        await asyncio_detailed(
            client=client,
            multipart_data=multipart_data,
        )
    ).parsed
