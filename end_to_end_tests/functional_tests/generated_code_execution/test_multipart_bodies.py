import email.parser
import email.policy
import io

import httpx2

from end_to_end_tests.functional_tests.helpers import (
    with_generated_client_fixture,
    with_generated_code_imports,
)

# Content that would end the part early if the request used a fixed "+++" boundary
FILE_CONTENT = b"first line\r\n--+++\r\nstill the same file\r\n"


def _send_and_capture(Client, sync_detailed, body) -> httpx2.Request:
    sent: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        request.read()
        sent.append(request)
        return httpx2.Response(200)

    client = Client(base_url="http://test", httpx_args={"transport": httpx2.MockTransport(handler)})
    sync_detailed(client=client, body=body)
    assert len(sent) == 1
    return sent[0]


def _parse_parts(request: httpx2.Request) -> dict[str, bytes]:
    content_type = request.headers["content-type"]
    assert content_type.startswith("multipart/form-data; boundary=")
    message = email.parser.BytesParser(policy=email.policy.HTTP).parsebytes(
        b"Content-Type: " + content_type.encode() + b"\r\n\r\n" + request.content
    )
    return {
        part.get_param("name", header="content-disposition"): part.get_payload(decode=True)
        for part in message.iter_parts()
    }


@with_generated_client_fixture(
    """
paths:
  /upload:
    post:
      operationId: upload
      requestBody:
        required: true
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                file: {type: string, format: binary}
      responses:
        "200": {description: OK}
"""
)
@with_generated_code_imports(
    ".api.default.upload.sync_detailed",
    ".client.Client",
    ".models.UploadBody",
    ".types.File",
)
class TestSingleMultipartBody:
    def test_file_content_is_not_split_by_boundary(self, sync_detailed, Client, UploadBody, File):
        body = UploadBody(file=File(payload=io.BytesIO(FILE_CONTENT), file_name="a.txt"))

        request = _send_and_capture(Client, sync_detailed, body)

        assert _parse_parts(request) == {"file": FILE_CONTENT}


@with_generated_client_fixture(
    """
paths:
  /upload:
    post:
      operationId: upload
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                name: {type: string}
          multipart/form-data:
            schema:
              type: object
              properties:
                file: {type: string, format: binary}
      responses:
        "200": {description: OK}
"""
)
@with_generated_code_imports(
    ".api.default.upload.sync_detailed",
    ".client.Client",
    ".models.UploadJsonBody",
    ".models.UploadFilesBody",
    ".types.File",
)
class TestMultipartBodyAmongSeveralBodies:
    def test_file_content_is_not_split_by_boundary(self, sync_detailed, Client, UploadJsonBody, UploadFilesBody, File):
        body = UploadFilesBody(file=File(payload=io.BytesIO(FILE_CONTENT), file_name="a.txt"))

        request = _send_and_capture(Client, sync_detailed, body)

        assert _parse_parts(request) == {"file": FILE_CONTENT}

    def test_json_body_still_sets_its_content_type(self, sync_detailed, Client, UploadJsonBody, UploadFilesBody, File):
        request = _send_and_capture(Client, sync_detailed, UploadJsonBody(name="a"))

        assert request.headers["content-type"] == "application/json"
        assert request.content == b'{"name":"a"}'
