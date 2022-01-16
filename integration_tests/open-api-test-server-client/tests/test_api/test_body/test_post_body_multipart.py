from io import BytesIO

from open_api_test_server_client import Client
from open_api_test_server_client.api.body import post_body_multipart
from open_api_test_server_client.models import PostBodyMultipartMultipartData, PostBodyMultipartResponse200
from open_api_test_server_client.types import File


def test():
    client = Client("http://localhost:3000")

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
        raise AssertionError(
            f"Received status {response.status_code} from test server with payload: {content!r}"
        )

    assert content.a_string == a_string
    assert content.file_name == file_name
    assert content.file_content_type == mime_type
    assert content.file_data.encode() == payload
    assert content.description == description
