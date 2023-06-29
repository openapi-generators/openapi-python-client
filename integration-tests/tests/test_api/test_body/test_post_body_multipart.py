from io import BytesIO

import httpx
import pytest

from integration_tests.api.body import post_body_multipart
from integration_tests.client import Client
from integration_tests.models.post_body_multipart_multipart_data import PostBodyMultipartMultipartData
from integration_tests.models.post_body_multipart_response_200 import PostBodyMultipartResponse200
from integration_tests.types import File


def test(client: Client) -> None:
    a_string = "a test string"
    payload = b"some file content"
    file_name = "cool_stuff.txt"
    mime_type = "application/openapi-python-client"
    description = "super descriptive thing"

    response = post_body_multipart.sync_detailed(
        client=client,
        multipart_data=PostBodyMultipartMultipartData(
            a_string=a_string,
            file=File(
                payload=BytesIO(payload),
                file_name=file_name,
                mime_type=mime_type,
            ),
            description=description,
        ),
    )

    content = response.parsed
    if not isinstance(content, PostBodyMultipartResponse200):
        raise AssertionError(f"Received status {response.status_code} from test server with payload: {content!r}")

    assert content.a_string == a_string
    assert content.file_name == file_name
    assert content.file_content_type == mime_type
    assert content.file_data.encode() == payload
    assert content.description == description

def test_context_manager(client: Client) -> None:
    a_string = "a test string"
    payload = b"some file content"
    file_name = "cool_stuff.txt"
    mime_type = "application/openapi-python-client"
    description = "super descriptive thing"

    with client as client:
        post_body_multipart.sync_detailed(
            client=client,
            multipart_data=PostBodyMultipartMultipartData(
                a_string=a_string,
                file=File(
                    payload=BytesIO(payload),
                    file_name=file_name,
                    mime_type=mime_type,
                ),
                description=description,
            ),
        )
        response = post_body_multipart.sync_detailed(
            client=client,
            multipart_data=PostBodyMultipartMultipartData(
                a_string=a_string,
                file=File(
                    payload=BytesIO(payload),
                    file_name=file_name,
                    mime_type=mime_type,
                ),
                description=description,
            ),
        )

    with pytest.raises(RuntimeError):
        post_body_multipart.sync_detailed(
            client=client,
            multipart_data=PostBodyMultipartMultipartData(
                a_string=a_string,
                file=File(
                    payload=BytesIO(payload),
                    file_name=file_name,
                    mime_type=mime_type,
                ),
                description=description,
            ),
        )

    content = response.parsed
    if not isinstance(content, PostBodyMultipartResponse200):
        raise AssertionError(f"Received status {response.status_code} from test server with payload: {content!r}")

    assert content.a_string == a_string
    assert content.file_name == file_name
    assert content.file_content_type == mime_type
    assert content.file_data.encode() == payload
    assert content.description == description


@pytest.mark.asyncio
async def test_async(client: Client) -> None:
    a_string = "a test string"
    payload = b"some file content"
    file_name = "cool_stuff.txt"
    mime_type = "application/openapi-python-client"
    description = "super descriptive thing"

    response = await post_body_multipart.asyncio_detailed(
        client=client,
        multipart_data=PostBodyMultipartMultipartData(
            a_string=a_string,
            file=File(
                payload=BytesIO(payload),
                file_name=file_name,
                mime_type=mime_type,
            ),
            description=description,
        ),
    )

    content = response.parsed
    if not isinstance(content, PostBodyMultipartResponse200):
        raise AssertionError(f"Received status {response.status_code} from test server with payload: {content!r}")

    assert content.a_string == a_string
    assert content.file_name == file_name
    assert content.file_content_type == mime_type
    assert content.file_data.encode() == payload
    assert content.description == description

@pytest.mark.asyncio
async def test_async_context_manager(client: Client) -> None:
    a_string = "a test string"
    payload = b"some file content"
    file_name = "cool_stuff.txt"
    mime_type = "application/openapi-python-client"
    description = "super descriptive thing"

    async with client as client:
        await post_body_multipart.asyncio_detailed(
            client=client,
            multipart_data=PostBodyMultipartMultipartData(
                a_string=a_string,
                file=File(
                    payload=BytesIO(payload),
                    file_name=file_name,
                    mime_type=mime_type,
                ),
                description=description,
            ),
        )
        response = await post_body_multipart.asyncio_detailed(
            client=client,
            multipart_data=PostBodyMultipartMultipartData(
                a_string=a_string,
                file=File(
                    payload=BytesIO(payload),
                    file_name=file_name,
                    mime_type=mime_type,
                ),
                description=description,
            ),
        )

    with pytest.raises(RuntimeError):
        await post_body_multipart.asyncio_detailed(
            client=client,
            multipart_data=PostBodyMultipartMultipartData(
                a_string=a_string,
                file=File(
                    payload=BytesIO(payload),
                    file_name=file_name,
                    mime_type=mime_type,
                ),
                description=description,
            ),
        )

    content = response.parsed
    if not isinstance(content, PostBodyMultipartResponse200):
        raise AssertionError(f"Received status {response.status_code} from test server with payload: {content!r}")

    assert content.a_string == a_string
    assert content.file_name == file_name
    assert content.file_content_type == mime_type
    assert content.file_data.encode() == payload
    assert content.description == description
