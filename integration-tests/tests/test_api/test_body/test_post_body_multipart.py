from io import BytesIO
from typing import Any

import pytest

from integration_tests.api.body import post_body_multipart
from integration_tests.client import Client
from integration_tests.models.post_body_multipart_body import PostBodyMultipartBody
from integration_tests.models.post_body_multipart_response_200 import PostBodyMultipartResponse200
from integration_tests.types import File

files = [
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
]


def test(client: Client) -> None:
    a_string = "a test string"
    description = "super descriptive thing"

    response = post_body_multipart.sync_detailed(
        client=client,
        body=PostBodyMultipartBody(
            a_string=a_string,
            files=files,
            description=description,
        ),
    )

    content = response.parsed
    if not isinstance(content, PostBodyMultipartResponse200):
        raise AssertionError(f"Received status {response.status_code} from test server with payload: {content!r}")

    assert content.a_string == a_string
    assert content.description == description
    for i, file in enumerate(content.files):
        files[i].payload.seek(0)
        assert file.data == files[i].payload.read().decode()
        assert file.name == files[i].file_name
        assert file.content_type == files[i].mime_type


def test_custom_hooks() -> None:
    a_string = "a test string"
    description = "super descriptive thing"

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
        body=PostBodyMultipartBody(
            a_string=a_string,
            files=files,
            description=description,
        ),
    )

    assert request_hook_called
    assert response_hook_called


def test_context_manager(client: Client) -> None:
    a_string = "a test string"
    description = "super descriptive thing"

    with client as client:
        post_body_multipart.sync_detailed(
            client=client,
            body=PostBodyMultipartBody(
                a_string=a_string,
                files=files,
                description=description,
            ),
        )
        response = post_body_multipart.sync_detailed(
            client=client,
            body=PostBodyMultipartBody(
                a_string=a_string,
                files=files,
                description=description,
            ),
        )

    with pytest.raises(RuntimeError):
        post_body_multipart.sync_detailed(
            client=client,
            body=PostBodyMultipartBody(
                a_string=a_string,
                files=files,
                description=description,
            ),
        )

    content = response.parsed
    if not isinstance(content, PostBodyMultipartResponse200):
        raise AssertionError(f"Received status {response.status_code} from test server with payload: {content!r}")


@pytest.mark.asyncio
async def test_async(client: Client) -> None:
    a_string = "a test string"
    description = "super descriptive thing"

    response = await post_body_multipart.asyncio_detailed(
        client=client,
        body=PostBodyMultipartBody(
            a_string=a_string,
            files=files,
            description=description,
        ),
    )

    content = response.parsed
    if not isinstance(content, PostBodyMultipartResponse200):
        raise AssertionError(f"Received status {response.status_code} from test server with payload: {content!r}")

    assert content.a_string == a_string
    assert content.description == description
    for i, file in enumerate(content.files):
        files[i].payload.seek(0)
        assert file.data == files[i].payload.read().decode()
        assert file.name == files[i].file_name
        assert file.content_type == files[i].mime_type


@pytest.mark.asyncio
async def test_async_context_manager(client: Client) -> None:
    a_string = "a test string"
    description = "super descriptive thing"

    async with client as client:
        await post_body_multipart.asyncio_detailed(
            client=client,
            body=PostBodyMultipartBody(
                a_string=a_string,
                files=files,
                description=description,
            ),
        )
        response = await post_body_multipart.asyncio_detailed(
            client=client,
            body=PostBodyMultipartBody(
                a_string=a_string,
                files=files,
                description=description,
            ),
        )

    with pytest.raises(RuntimeError):
        await post_body_multipart.asyncio_detailed(
            client=client,
            body=PostBodyMultipartBody(
                a_string=a_string,
                files=files,
                description=description,
            ),
        )

    content = response.parsed
    if not isinstance(content, PostBodyMultipartResponse200):
        raise AssertionError(f"Received status {response.status_code} from test server with payload: {content!r}")

    assert content.a_string == a_string
    assert content.description == description
    for i, file in enumerate(content.files):
        files[i].payload.seek(0)
        assert file.data == files[i].payload.read().decode()
        assert file.name == files[i].file_name
        assert file.content_type == files[i].mime_type
