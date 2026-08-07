from datetime import UTC, datetime, timedelta
from io import BytesIO
from typing import Any

import pytest

from integration_tests.api.body import post_body_multipart
from integration_tests.client import Client
from integration_tests.models import AnObject, PostBodyMultipartResponse200
from integration_tests.models.post_body_multipart_body import PostBodyMultipartBody
from integration_tests.types import File


def make_body() -> PostBodyMultipartBody:
    """A fresh body per test: the files are `BytesIO` payloads that get consumed on send."""
    return PostBodyMultipartBody(
        a_string="a test string",
        description="super descriptive thing",
        files=[
            File(
                payload=BytesIO(b"some file content"),
                file_name="cool_stuff.txt",
                mime_type="application/openapi-python-client",
            ),
            File(
                payload=BytesIO(b"more file content"),
                file_name=None,
                mime_type=None,
            ),
        ],
        times=[datetime.now(UTC) - timedelta(days=1), datetime.now(UTC)],
        objects=[
            AnObject(
                an_int=1,
                a_float=2.3,
            ),
            AnObject(
                an_int=4,
                a_float=5.6,
            ),
        ],
    )


def check_response(content: PostBodyMultipartResponse200, body: PostBodyMultipartBody) -> None:
    assert content.a_string == body.a_string
    assert content.description == body.description
    assert content.times == body.times
    assert content.objects == body.objects
    assert len(content.files) == len(body.files)
    for i, file in enumerate(content.files):
        body.files[i].payload.seek(0)
        assert file.data == body.files[i].payload.read().decode()
        assert file.name == body.files[i].file_name
        assert file.content_type == body.files[i].mime_type


async def test(client: Client) -> None:
    body = make_body()

    content = await post_body_multipart.request(
        client=client,
        body=body,
    )

    check_response(content, body)


async def test_detailed_response_carries_status_and_parsed(client: Client) -> None:
    """`_request_detailed` is the escape hatch for callers that need more than the parsed body."""
    body = make_body()

    response = await post_body_multipart._request_detailed(
        client=client,
        body=body,
    )

    assert response.status_code == 200
    assert response.parsed is not None
    check_response(response.parsed, body)


async def test_custom_hooks() -> None:
    """`httpx_args` reaches the underlying client.

    The hooks must be coroutines: endpoints go through `httpx.AsyncClient`, which awaits every
    event hook. A plain function is accepted at construction and only blows up on the first
    request, with `TypeError: 'NoneType' object can't be awaited`.
    """
    request_hook_called = False
    response_hook_called = False

    async def log_request(*_: Any, **__: Any) -> None:
        nonlocal request_hook_called
        request_hook_called = True

    async def log_response(*_: Any, **__: Any) -> None:
        nonlocal response_hook_called
        response_hook_called = True

    client = Client(
        "http://localhost:3000", httpx_args={"event_hooks": {"request": [log_request], "response": [log_response]}}
    )

    await post_body_multipart.request(
        client=client,
        body=make_body(),
    )

    assert request_hook_called
    assert response_hook_called


async def test_async_context_manager(client: Client) -> None:
    body = make_body()

    async with client as client:
        await post_body_multipart.request(
            client=client,
            body=make_body(),
        )
        content = await post_body_multipart.request(
            client=client,
            body=body,
        )

    with pytest.raises(RuntimeError):
        await post_body_multipart.request(
            client=client,
            body=make_body(),
        )

    check_response(content, body)
