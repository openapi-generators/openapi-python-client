from datetime import datetime, timedelta, timezone
from io import BytesIO
from typing import Any, Union

import pytest

from integration_tests.api.body import post_body_multipart
from integration_tests.client import Client
from integration_tests.models import AnObject, PublicError
from integration_tests.models.post_body_multipart_body import PostBodyMultipartBody
from integration_tests.models.post_body_multipart_response_200 import PostBodyMultipartResponse200
from integration_tests.types import File, Response

body = PostBodyMultipartBody(
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
    times=[datetime.now(timezone.utc) - timedelta(days=1), datetime.now(timezone.utc)],
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


def check_response(response: Response[Union[PostBodyMultipartResponse200, PublicError]]) -> None:
    content = response.parsed
    if not isinstance(content, PostBodyMultipartResponse200):
        raise AssertionError(f"Received status {response.status_code} from test server with payload: {content!r}")

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


def test(client: Client) -> None:
    response = post_body_multipart.sync_detailed(
        client=client,
        body=body,
    )

    check_response(response)


def test_custom_hooks() -> None:
    request_hook_called = False
    response_hook_called = False

    def log_request(*_: Any, **__: Any) -> None:
        nonlocal request_hook_called
        request_hook_called = True

    def log_response(*_: Any, **__: Any) -> None:
        nonlocal response_hook_called
        response_hook_called = True

    client = Client(
        "http://localhost:3000", httpx_args={"event_hooks": {"request": [log_request], "response": [log_response]}}
    )

    post_body_multipart.sync_detailed(
        client=client,
        body=body,
    )

    assert request_hook_called
    assert response_hook_called


def test_context_manager(client: Client) -> None:
    with client as client:
        post_body_multipart.sync_detailed(
            client=client,
            body=body,
        )
        response = post_body_multipart.sync_detailed(
            client=client,
            body=body,
        )

    with pytest.raises(RuntimeError):
        post_body_multipart.sync_detailed(
            client=client,
            body=body,
        )

    check_response(response)


@pytest.mark.asyncio
async def test_async(client: Client) -> None:
    response = await post_body_multipart.asyncio_detailed(
        client=client,
        body=body,
    )

    check_response(response)


@pytest.mark.asyncio
async def test_async_context_manager(client: Client) -> None:
    async with client as client:
        await post_body_multipart.asyncio_detailed(
            client=client,
            body=body,
        )
        response = await post_body_multipart.asyncio_detailed(
            client=client,
            body=body,
        )

    with pytest.raises(RuntimeError):
        await post_body_multipart.asyncio_detailed(
            client=client,
            body=body,
        )

    check_response(response)
