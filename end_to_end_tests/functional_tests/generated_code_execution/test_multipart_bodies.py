"""Execution tests for ``multipart/form-data`` request bodies.

Uploading a file through a generated client needs three separate things to hold, and
each one is a distinct failure mode that source-level golden-record comparison cannot
catch:

1. The binary property has to be recognised as one. OpenAPI 3.1 producers (FastAPI
   among them) describe an upload as ``{"type": "string", "contentMediaType":
   "application/octet-stream"}`` with no ``format: binary``, so a generator that keys
   only off ``format`` silently emits ``str``.
2. ``types.File`` has to be usable as a field type on the generated Pydantic models.
   It wraps a raw binary stream, which Pydantic cannot introspect, so without a core
   schema the model raises ``PydanticSchemaGenerationError`` at class-creation time and
   the module cannot even be imported.
3. ``to_multipart()`` has to produce parts that a real parser reads back as *files* --
   carrying a filename and the declared content type -- rather than as text fields.
   ``python_multipart`` is the parser FastAPI itself uses, so we assert against it.
4. Whatever Pydantic coerces into a ``File`` has to be sendable. A part with no
   filename is a text field as far as the server is concerned, and a missing content
   type is guessed from the extension -- ``mimetypes`` answers ``audio/x-wav`` for
   ``.wav``, which a server matching on ``audio/wav`` refuses. Neither can be inferred
   from bare bytes, so that input is rejected outright instead of failing at the
   server; a file-like input keeps the name it already has.

The scoping guard in :class:`TestJsonBodyBinaryPropertiesStayStrings` is the other half
of point 1: the exact same property schema means "a file" in a multipart body and "a
base64/latin-1 string" in a JSON body, so the mapping must be decided by the body's
content type, never by the property alone.
"""

import asyncio
from io import BytesIO
from typing import Any

import httpx
import pytest
import python_multipart
from pydantic import ValidationError

from end_to_end_tests.functional_tests.helpers import (
    with_generated_client_fixture,
    with_generated_code_import,
    with_generated_code_imports,
)

WAV_BYTES = b"RIFF\x00\x00\x00\x00WAVEfmt sample-audio-payload"


def parse_multipart(content_type: str, body: bytes) -> tuple[dict[str, bytes], dict[str, tuple[str, bytes]]]:
    """Parse a multipart body the way FastAPI does.

    Returns ``(fields, files)`` where ``fields`` maps a name to its raw value and
    ``files`` maps a name to ``(filename, content)``. A part only lands in ``files``
    when it carries a ``filename``, which is exactly the condition FastAPI uses to
    decide between ``UploadFile`` and ``str``.
    """
    fields: dict[str, bytes] = {}
    files: dict[str, tuple[str, bytes]] = {}

    def on_field(field: Any) -> None:
        fields[field.field_name.decode()] = field.value

    def on_file(file: Any) -> None:
        file.file_object.seek(0)
        files[file.field_name.decode()] = (file.file_name.decode(), file.file_object.read())

    python_multipart.parse_form({"Content-Type": content_type}, BytesIO(body), on_field, on_file)
    return fields, files


def part_headers(request: httpx.Request, name: str) -> str:
    """Return the raw header block of one part of an encoded multipart body.

    ``python_multipart`` normalises what it parses, so it cannot show whether the
    ``Content-Type`` header was emitted at all -- and that header is what the server
    matches on. This reads the bytes httpx actually put on the wire.
    """
    boundary = request.headers["content-type"].partition("boundary=")[2]
    for section in request.content.split(f"--{boundary}".encode()):
        headers = section.split(b"\r\n\r\n", 1)[0].decode()
        if f'name="{name}"' in headers:
            return headers
    raise AssertionError(f"no part named {name!r} in {request.content!r}")


def send_and_capture(Client: Any, endpoint: Any, **kwargs: Any) -> httpx.Request:
    """Run a generated endpoint against a mock transport and return the sent request."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, json={"text": "ok"})

    client = Client(base_url="https://example.com")
    client.set_async_httpx_client(
        httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://example.com")
    )
    asyncio.run(endpoint(client=client, **kwargs))
    return captured[0]


MULTIPART_SPEC_TEMPLATE = """
paths:
  "/transcribe":
    post:
      operationId: transcribeRecording
      requestBody:
        required: true
        content:
          multipart/form-data:
            schema:
              $ref: "#/components/schemas/BodyTranscribeRecording"
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                type: object
                properties:
                  text: {{type: string}}
components:
  schemas:
    BodyTranscribeRecording:
      type: object
      properties:
        audio_file:
{binary_property}
        language:
          type: string
      required: ["audio_file"]
"""


def with_transcribe_client(binary_property: str):
    """Build the transcribe client for one way of spelling the binary part."""
    spec = MULTIPART_SPEC_TEMPLATE.format(binary_property=binary_property)

    def _decorator(cls):
        cls = with_generated_code_import(
            ".api.default.transcribe_recording._request_detailed", alias="request_detailed"
        )(cls)
        cls = with_generated_code_imports(".models.BodyTranscribeRecording", ".types.File", ".client.Client")(cls)
        return with_generated_client_fixture(spec)(cls)

    return _decorator


class MultipartBodyContract:
    """Assertions that must hold for every way a spec can describe a binary part."""

    def test_binary_property_is_a_file(self, BodyTranscribeRecording, File):
        assert BodyTranscribeRecording.model_fields["audio_file"].annotation is File

    def test_non_binary_property_is_untouched(self, BodyTranscribeRecording):
        assert BodyTranscribeRecording.model_fields["language"].annotation is not None
        assert "str" in str(BodyTranscribeRecording.model_fields["language"].annotation)

    def test_file_field_round_trips_without_coercion(self, BodyTranscribeRecording, File):
        payload = BytesIO(WAV_BYTES)
        audio = File(payload=payload, file_name="audio.wav", mime_type="audio/wav")
        body = BodyTranscribeRecording(audio_file=audio)

        # Pydantic must hand back the very same File -- re-wrapping it would detach the
        # caller's stream, and copying it would re-read an already-consumed one.
        assert body.audio_file is audio
        assert body.audio_file.payload is payload

    def test_to_multipart_emits_file_tuple(self, BodyTranscribeRecording, File):
        body = BodyTranscribeRecording(
            audio_file=File(payload=BytesIO(WAV_BYTES), file_name="audio.wav", mime_type="audio/wav"),
            language="sv",
        )
        parts = dict(body.to_multipart())

        assert parts["audio_file"][0] == "audio.wav"
        assert parts["audio_file"][2] == "audio/wav"
        assert parts["language"] == (None, b"sv", "text/plain")

    def test_endpoint_sends_parsable_multipart(self, Client, request_detailed, BodyTranscribeRecording, File):
        body = BodyTranscribeRecording(
            audio_file=File(payload=BytesIO(WAV_BYTES), file_name="audio.wav", mime_type="audio/wav"),
            language="sv",
        )
        request = send_and_capture(Client, request_detailed, body=body)

        content_type = request.headers["content-type"]
        assert content_type.startswith("multipart/form-data; boundary=")

        fields, files = parse_multipart(content_type, request.content)

        # The upload must arrive as a file part. Without a filename python_multipart
        # reports it as a plain field and FastAPI rejects the request with a 422.
        assert "audio_file" in files, f"audio_file was parsed as a text field, not a file: {fields}"
        assert files["audio_file"] == ("audio.wav", WAV_BYTES)
        assert fields["language"] == b"sv"

    def test_encoded_part_carries_filename_and_content_type(
        self, Client, request_detailed, BodyTranscribeRecording, File
    ):
        """Both headers have to reach the wire, and neither may be left to inference.

        Without ``filename`` the part is a text field, not a file. And ``Content-Type``
        cannot be left off either: httpx would guess it from the extension, and
        ``mimetypes`` answers ``audio/x-wav`` for ``.wav``, which a server matching on
        ``audio/wav`` rejects.
        """
        body = BodyTranscribeRecording(
            audio_file=File(payload=BytesIO(WAV_BYTES), file_name="audio.wav", mime_type="audio/wav")
        )
        headers = part_headers(send_and_capture(Client, request_detailed, body=body), "audio_file")

        assert 'filename="audio.wav"' in headers
        assert "Content-Type: audio/wav" in headers

    def test_bare_bytes_are_rejected_with_an_actionable_message(self, BodyTranscribeRecording):
        """``Body(audio_file=b"...")`` is the obvious thing to write and cannot work.

        The resulting part would have no filename and no content type, so the server
        rejects it -- far from the line that caused it. Name both fields here instead.
        """
        with pytest.raises(ValidationError) as exc_info:
            BodyTranscribeRecording(audio_file=WAV_BYTES)

        message = str(exc_info.value)
        assert "file name" in message
        assert "content type" in message

    def test_declared_boundary_matches_the_encoded_body(self, Client, request_detailed, BodyTranscribeRecording, File):
        """The generator pins ``boundary=+++`` in the header; httpx must encode with it.

        If httpx picked its own boundary instead, the header and the body would disagree
        and every upload would fail to parse server-side.
        """
        body = BodyTranscribeRecording(
            audio_file=File(payload=BytesIO(WAV_BYTES), file_name="audio.wav", mime_type="audio/wav")
        )
        request = send_and_capture(Client, request_detailed, body=body)

        boundary = request.headers["content-type"].partition("boundary=")[2]
        assert boundary, "no boundary in Content-Type"
        assert request.content.startswith(f"--{boundary}".encode())


@with_transcribe_client("          type: string\n          contentMediaType: application/octet-stream")
class TestMultipartBodyDescribedWithContentMediaType(MultipartBodyContract):
    """The OpenAPI 3.1 / FastAPI shape: ``contentMediaType``, no ``format``."""


@with_transcribe_client("          type: string\n          format: binary")
class TestMultipartBodyDescribedWithBinaryFormat(MultipartBodyContract):
    """The OpenAPI 3.0 shape: ``format: binary``."""


@with_transcribe_client(
    "          type: string\n          format: binary\n          contentMediaType: application/octet-stream"
)
class TestMultipartBodyDescribedWithBoth(MultipartBodyContract):
    """Both annotations present -- the two rules must agree, not double-apply."""


@with_generated_client_fixture(
    """
paths:
  "/upload":
    post:
      operationId: uploadOptional
      requestBody:
        content:
          multipart/form-data:
            schema:
              $ref: "#/components/schemas/UploadBody"
      responses:
        "200":
          description: Success
components:
  schemas:
    UploadBody:
      type: object
      properties:
        required_file:
          type: string
          contentMediaType: application/octet-stream
        optional_file:
          type: string
          contentMediaType: application/octet-stream
      required: ["required_file"]
"""
)
@with_generated_code_imports(".models.UploadBody", ".types.File")
class TestOptionalFileParts:
    def test_unset_optional_file_is_omitted(self, UploadBody, File):
        body = UploadBody(required_file=File(payload=BytesIO(b"a"), file_name="a.bin"))
        assert [name for name, _ in body.to_multipart()] == ["required_file"]

    def test_set_optional_file_is_included(self, UploadBody, File):
        body = UploadBody(
            required_file=File(payload=BytesIO(b"a"), file_name="a.bin"),
            optional_file=File(payload=BytesIO(b"b"), file_name="b.bin"),
        )
        assert [name for name, _ in body.to_multipart()] == ["required_file", "optional_file"]


@with_generated_client_fixture(
    """
paths:
  "/download":
    get:
      operationId: download
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DownloadResponse"
components:
  schemas:
    DownloadResponse:
      type: object
      properties:
        data:
          type: string
          format: binary
        attachments:
          type: array
          items:
            type: string
            format: binary
"""
)
@with_generated_code_imports(".models.DownloadResponse", ".types.File")
class TestBinaryPropertiesOutsideMultipartBodies:
    """``File`` also shows up in plain models and in responses.

    A fix scoped to multipart bodies alone leaves these broken, and because
    ``models/__init__.py`` imports every model eagerly, one such model makes the whole
    generated package unimportable.
    """

    def test_model_with_file_property_imports(self, DownloadResponse, File):
        assert DownloadResponse.model_fields["data"].annotation is not None

    def test_file_property_accepts_a_file(self, DownloadResponse, File):
        response = DownloadResponse(data=File(payload=BytesIO(b"bytes")))
        assert isinstance(response.data, File)

    def test_list_of_files(self, DownloadResponse, File):
        response = DownloadResponse(attachments=[File(payload=BytesIO(b"one")), File(payload=BytesIO(b"two"))])
        assert [attachment.payload.getvalue() for attachment in response.attachments] == [b"one", b"two"]

    def test_raw_bytes_are_rejected(self, DownloadResponse):
        """Bare bytes carry neither a file name nor a content type, so coercing them
        would build a File that cannot be uploaded. Fail here, with both fields named,
        rather than in the server's 422."""
        with pytest.raises(ValidationError) as exc_info:
            DownloadResponse.from_dict({"data": b"raw"})

        message = str(exc_info.value)
        assert "file name" in message
        assert "content type" in message

    def test_non_binary_input_is_rejected(self, DownloadResponse):
        with pytest.raises(ValidationError):
            DownloadResponse.from_dict({"data": 123})

    def test_dict_round_trip(self, DownloadResponse, File):
        """``from_dict`` has to accept what ``to_dict`` produced."""
        original = DownloadResponse(data=File(payload=BytesIO(b"audio"), file_name="a.wav", mime_type="audio/wav"))
        restored = DownloadResponse.from_dict(original.to_dict())

        assert restored.data.file_name == "a.wav"
        assert restored.data.mime_type == "audio/wav"
        # The payload has no JSON form, so only the metadata survives the trip.
        assert restored.data.payload.read() == b""

    def test_unknown_mapping_keys_are_rejected(self, DownloadResponse):
        with pytest.raises(ValidationError):
            DownloadResponse.from_dict({"data": {"file_name": "a.wav", "payload": "raw"}})

    def test_file_like_keeps_its_name(self, DownloadResponse, tmp_path):
        """An open file already knows what it is called; dropping that leaves a nameless
        part, which a server reads as a text field instead of a file."""
        path = tmp_path / "recording.wav"
        path.write_bytes(WAV_BYTES)

        with path.open("rb") as stream:
            response = DownloadResponse(data=stream)

        # The basename only -- the full path would leak the caller's directory layout.
        assert response.data.file_name == "recording.wav"

    def test_nameless_stream_is_allowed(self, DownloadResponse):
        """A stream with no ``name`` (a BytesIO) still validates; there is simply
        nothing to preserve."""
        assert DownloadResponse(data=BytesIO(b"x")).data.file_name is None

    def test_to_dict_emits_metadata_and_leaves_the_stream_unread(self, DownloadResponse, File):
        """Serialising must never drain the payload -- it is usually about to be uploaded."""
        payload = BytesIO(b"audio-bytes")
        response = DownloadResponse(data=File(payload=payload, file_name="a.wav", mime_type="audio/wav"))

        assert response.to_dict() == {"data": {"file_name": "a.wav", "mime_type": "audio/wav"}}
        assert payload.read() == b"audio-bytes"

    def test_python_mode_dump_returns_the_file(self, DownloadResponse, File):
        file = File(payload=BytesIO(b"x"), file_name="a.wav")
        assert DownloadResponse(data=file).model_dump()["data"] is file

    def test_models_package_imports(self, generated_client):
        """The eager re-export in ``models/__init__.py`` must not blow up."""
        generated_client.import_module(".models")


@with_generated_client_fixture(
    """
paths:
  "/store":
    post:
      operationId: store
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/StoreBody"
      responses:
        "200":
          description: Success
components:
  schemas:
    StoreBody:
      type: object
      properties:
        blob:
          type: string
          contentMediaType: application/octet-stream
      required: ["blob"]
"""
)
@with_generated_code_imports(".models.StoreBody")
class TestJsonBodyBinaryPropertiesStayStrings:
    """``contentMediaType`` must only mean "file" inside a multipart body.

    FastAPI emits the identical property schema for a ``bytes`` field on a JSON body,
    where the value really is transported as a string. Mapping those to ``File`` would
    produce a body that cannot be JSON-serialised at all.
    """

    def test_binary_property_in_json_body_is_a_string(self, StoreBody):
        assert StoreBody.model_fields["blob"].annotation is str

    def test_json_body_serialises(self, StoreBody):
        assert StoreBody(blob="aGVsbG8=").to_dict() == {"blob": "aGVsbG8="}


@with_generated_client_fixture(
    """
paths:
  "/multipart-file":
    post:
      operationId: demoFileUpload
      parameters:
        - in: query
          name: id_parameter
          required: false
          schema:
            anyOf:
              - type: string
              - type: "null"
        - in: query
          name: foo_param
          required: false
          schema:
            anyOf:
              - type: string
              - type: "null"
      requestBody:
        required: true
        content:
          multipart/form-data:
            schema:
              $ref: "#/components/schemas/BodyDemoFileUpload"
      responses:
        "200":
          description: Successful Response
          content:
            application/json:
              schema: {}
components:
  schemas:
    BodyDemoFileUpload:
      type: object
      properties:
        audio_file:
          type: string
          contentMediaType: application/octet-stream
      required: ["audio_file"]
"""
)
@with_generated_code_imports(".models.BodyDemoFileUpload", ".types.File", ".client.Client")
@with_generated_code_import(".api.default.demo_file_upload.request", alias="upload")
class TestUploadEndpointReturningNothing:
    """A FastAPI route annotated ``-> None`` alongside query parameters.

    FastAPI describes that response as an empty schema, which the generator resolves to
    ``Any``. The public ``request`` function must still exist: it is the only public name
    in the module, so gating it on having a body to parse leaves the endpoint uncallable.
    """

    def test_public_request_function_exists(self, upload):
        assert callable(upload)

    def test_upload_with_query_parameters(self, Client, upload, BodyDemoFileUpload, File):
        body = BodyDemoFileUpload(
            audio_file=File(payload=BytesIO(WAV_BYTES), file_name="audio.wav", mime_type="audio/wav")
        )
        sent = send_and_capture(Client, upload, body=body, id_parameter="abc", foo_param="xyz")

        assert dict(sent.url.params) == {"id_parameter": "abc", "foo_param": "xyz"}
        _, files = parse_multipart(sent.headers["content-type"], sent.content)
        assert files["audio_file"] == ("audio.wav", WAV_BYTES)

    def test_omitted_query_parameters_are_dropped(self, Client, upload, BodyDemoFileUpload, File):
        body = BodyDemoFileUpload(audio_file=File(payload=BytesIO(WAV_BYTES), file_name="audio.wav"))
        sent = send_and_capture(Client, upload, body=body)

        assert dict(sent.url.params) == {}
