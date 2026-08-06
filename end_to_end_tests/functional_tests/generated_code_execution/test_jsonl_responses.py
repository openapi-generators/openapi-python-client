"""An `application/jsonl` response generates `stream`, an async generator of parsed items.

This file previously drove `sync`/`asyncio`, which the fork no longer generates, and was skipped wholesale in
`conftest.py`. It now drives `stream` against a real `httpx.AsyncClient` over a `MockTransport`, which means the
error paths exercise the same `aread()`/`json()` a live response would.

The error path deliberately diverges from the non-streaming one: a documented non-2xx raises whether or not
`raise_on_unexpected_status` is set, because an async generator has nothing to hand back in its place -- suppressing
would silently produce an empty stream, which reads as "the server had nothing to say".
"""

import json

import pytest

from end_to_end_tests.functional_tests.helpers import (
    drain,
    with_generated_client_fixture,
    with_generated_code_import,
    with_generated_code_imports,
)

ERROR_BODY = {"message": "nope"}


@with_generated_client_fixture(
    """
components:
  schemas:
    GenerationEvent:
      type: object
      properties:
        delta:
          type: string
      required: ["delta"]
    CitationEvent:
      type: object
      properties:
        citation_id:
          type: string
        url:
          type: string
      required: ["citation_id", "url"]
    ApiError:
      type: object
      properties:
        message:
          type: string
      required: ["message"]
paths:
  "/events":
    get:
      operationId: getEvents
      responses:
        "200":
          description: Successful Response
          content:
            application/jsonl:
              itemSchema:
                anyOf:
                  - $ref: "#/components/schemas/GenerationEvent"
                  - $ref: "#/components/schemas/CitationEvent"
                title: StreamItem Get Events
        "422":
          description: Validation Error
          content:
            application/json:
              schema: {"$ref": "#/components/schemas/ApiError"}
  "/bare-events":
    get:
      operationId: getBareEvents
      responses:
        "200":
          description: Successful Response
          content:
            application/jsonl:
              itemSchema:
                $ref: "#/components/schemas/GenerationEvent"
        "503":
          description: Unavailable
"""
)
@with_generated_code_imports(
    ".models.GenerationEvent",
    ".models.CitationEvent",
    ".models.ApiError",
    ".client.Client",
    ".errors.UnexpectedStatus",
)
@with_generated_code_import(".api.default.get_events.stream", alias="stream_events")
@with_generated_code_import(".api.default.get_bare_events.stream", alias="stream_bare_events")
class TestJsonlResponse:
    """An `application/jsonl` response yields one parsed item per line."""

    def _lines(self):
        return [
            json.dumps({"delta": "Hello"}),
            json.dumps({"citation_id": "ref-1", "url": "https://example.com"}),
            json.dumps({"delta": "World"}),
        ]

    def test_yields_parsed_items(self, Client, stream_events, GenerationEvent, CitationEvent):
        items = drain(Client, stream_events, lines=self._lines())

        assert len(items) == 3

        assert isinstance(items[0], GenerationEvent)
        assert items[0].delta == "Hello"

        assert isinstance(items[1], CitationEvent)
        assert items[1].citation_id == "ref-1"
        assert items[1].url == "https://example.com"

        assert isinstance(items[2], GenerationEvent)
        assert items[2].delta == "World"

    def test_skips_empty_lines(self, Client, stream_events, GenerationEvent):
        lines = [json.dumps({"delta": "Hello"}), "", json.dumps({"delta": "World"}), ""]

        items = drain(Client, stream_events, lines=lines)

        assert [item.delta for item in items] == ["Hello", "World"]
        assert all(isinstance(item, GenerationEvent) for item in items)

    def test_documented_error_raises_with_parsed_body(self, Client, stream_events, ApiError, UnexpectedStatus):
        """The body used to be dropped: the branch read the response and raised with no `parsed`."""
        with pytest.raises(UnexpectedStatus) as exc_info:
            drain(Client, stream_events, status_code=422, json=ERROR_BODY)

        exc = exc_info.value
        assert exc.status_code == 422
        assert isinstance(exc.parsed, ApiError)
        assert exc.parsed.message == "nope"

    def test_documented_error_raises_even_with_raising_suppressed(self, Client, stream_events, UnexpectedStatus):
        """Unlike the non-streaming path -- there is no None to return from an async generator, and yielding nothing
        would hide the error completely."""
        with pytest.raises(UnexpectedStatus) as exc_info:
            drain(
                Client,
                stream_events,
                status_code=422,
                json=ERROR_BODY,
                raise_on_unexpected_status=False,
            )

        assert exc_info.value.parsed is not None

    def test_documented_error_without_a_body_has_no_parsed(self, Client, stream_bare_events, UnexpectedStatus):
        with pytest.raises(UnexpectedStatus) as exc_info:
            drain(Client, stream_bare_events, status_code=503)

        assert exc_info.value.status_code == 503
        assert exc_info.value.parsed is None

    def test_malformed_error_body_still_raises_the_status(self, Client, stream_events, UnexpectedStatus):
        """The streaming error branch shares `raise_error_response` with the non-streaming one, so it degrades the
        same way: a body that will not parse costs `.parsed`, never the status code."""
        with pytest.raises(UnexpectedStatus) as exc_info:
            drain(Client, stream_events, status_code=422, content=b"<html>502 Bad Gateway</html>")

        exc = exc_info.value
        assert exc.status_code == 422
        assert exc.content == b"<html>502 Bad Gateway</html>"
        assert exc.parsed is None

    def test_undocumented_status_raises_by_default(self, Client, stream_events, UnexpectedStatus):
        with pytest.raises(UnexpectedStatus) as exc_info:
            drain(Client, stream_events, status_code=500)

        assert exc_info.value.status_code == 500
        assert exc_info.value.parsed is None

    def test_undocumented_status_yields_nothing_when_suppressed(self, Client, stream_events):
        """The one place the flag still applies to a stream: with no schema for the status there is nothing to raise
        with, so the generator just ends."""
        assert drain(Client, stream_events, status_code=500, raise_on_unexpected_status=False) == []
