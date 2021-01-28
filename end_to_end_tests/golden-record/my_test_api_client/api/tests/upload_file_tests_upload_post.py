from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.body_upload_file_tests_upload_post import BodyUploadFileTestsUploadPost
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    multipart_data: BodyUploadFileTestsUploadPost,
    keep_alive: Union[Unset, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/tests/upload".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    if keep_alive is not UNSET:
        headers["keep-alive"] = keep_alive

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "files": multipart_data.to_dict(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = None

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    multipart_data: BodyUploadFileTestsUploadPost,
    keep_alive: Union[Unset, bool] = UNSET,
) -> Response[Union[None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        multipart_data=multipart_data,
        keep_alive=keep_alive,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    multipart_data: BodyUploadFileTestsUploadPost,
    keep_alive: Union[Unset, bool] = UNSET,
) -> Optional[Union[None, HTTPValidationError]]:
    """ Upload a file  """

    return sync_detailed(
        client=client,
        multipart_data=multipart_data,
        keep_alive=keep_alive,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    multipart_data: BodyUploadFileTestsUploadPost,
    keep_alive: Union[Unset, bool] = UNSET,
) -> Response[Union[None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        multipart_data=multipart_data,
        keep_alive=keep_alive,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    multipart_data: BodyUploadFileTestsUploadPost,
    keep_alive: Union[Unset, bool] = UNSET,
) -> Optional[Union[None, HTTPValidationError]]:
    """ Upload a file  """

    return (
        await asyncio_detailed(
            client=client,
            multipart_data=multipart_data,
            keep_alive=keep_alive,
        )
    ).parsed
