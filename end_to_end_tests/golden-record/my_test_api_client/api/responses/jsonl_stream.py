from collections.abc import AsyncGenerator
from typing import Any

import orjson

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.stream_event import StreamEvent


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/responses/jsonl-stream",
    }

    return _kwargs


async def stream(
    *,
    client: AuthenticatedClient | Client,
) -> AsyncGenerator[StreamEvent, None]:
    """JSONL Stream

     A streaming response, plus a documented error status the stream can end on instead.

    Raises:
        errors.UnexpectedStatus: If the server returns a status code that is not a documented
            success. A documented error response is parsed onto UnexpectedStatus.parsed. An
            undocumented status code raises only when Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AsyncGenerator[StreamEvent, None]
    """

    kwargs = _get_kwargs()

    async with client.get_async_httpx_client().stream(**kwargs) as response:
        if response.status_code == 200:
            async for _line in response.aiter_lines():
                if _line.strip():
                    _jsonl_data = orjson.loads(_line)
                    response_200_item = StreamEvent.from_dict(_jsonl_data)

                    yield response_200_item

        elif response.status_code == 422:
            await response.aread()
            response_422 = HTTPValidationError.from_dict(response.json())

            raise errors.UnexpectedStatus(
                response.status_code,
                response.content,
                parsed=response_422,
            )

        else:
            await response.aread()
            if client.raise_on_unexpected_status:
                raise errors.UnexpectedStatus(response.status_code, response.content)
