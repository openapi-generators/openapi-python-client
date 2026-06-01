import asyncio as _asyncio
import json
from contextlib import asynccontextmanager, contextmanager
from unittest.mock import MagicMock

import httpx

from end_to_end_tests.functional_tests.helpers import (
    with_generated_client_fixture,
    with_generated_code_import,
    with_generated_code_imports,
)


def _make_mock_stream_response(status_code, lines):
    """Create a mock httpx.Response that supports iter_lines/aiter_lines for streaming."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = status_code
    mock_response.headers = {}
    mock_response.content = "\n".join(lines).encode()

    def iter_lines():
        for line in lines:
            yield line

    mock_response.iter_lines = iter_lines

    async def aiter_lines():
        for line in lines:
            yield line

    mock_response.aiter_lines = aiter_lines

    return mock_response


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
""")
@with_generated_code_imports(
    ".api.default.get_events.sync",
    ".models.GenerationEvent",
    ".models.CitationEvent",
    ".client.Client",
)
@with_generated_code_import(".api.default.get_events.asyncio", alias="asyncio_func")
class TestJsonlResponse:
    """Test that application/jsonl responses generate streaming client methods yielding parsed items per line"""

    def _make_jsonl_lines(self):
        return [
            json.dumps({"delta": "Hello"}),
            json.dumps({"citation_id": "ref-1", "url": "https://example.com"}),
            json.dumps({"delta": "World"}),
        ]

    def test_sync_yields_parsed_items(self, sync, GenerationEvent, CitationEvent, Client):
        """The sync function should yield parsed objects via streaming, one per JSONL line"""
        lines = self._make_jsonl_lines()
        mock_response = _make_mock_stream_response(200, lines)

        mock_httpx_client = MagicMock(spec=httpx.Client)
        mock_httpx_client.stream = MagicMock(return_value=contextmanager(lambda: (yield mock_response))())

        client = Client(base_url="https://api.example.com")
        client.set_httpx_client(mock_httpx_client)

        items = list(sync(client=client))

        assert len(items) == 3

        assert isinstance(items[0], GenerationEvent)
        assert items[0].delta == "Hello"

        assert isinstance(items[1], CitationEvent)
        assert items[1].citation_id == "ref-1"
        assert items[1].url == "https://example.com"

        assert isinstance(items[2], GenerationEvent)
        assert items[2].delta == "World"

    def test_sync_handles_empty_lines(self, sync, GenerationEvent, Client):
        """Empty lines in JSONL output should be skipped"""
        lines = [
            json.dumps({"delta": "Hello"}),
            "",
            json.dumps({"delta": "World"}),
            "",
        ]
        mock_response = _make_mock_stream_response(200, lines)

        mock_httpx_client = MagicMock(spec=httpx.Client)
        mock_httpx_client.stream = MagicMock(return_value=contextmanager(lambda: (yield mock_response))())

        client = Client(base_url="https://api.example.com")
        client.set_httpx_client(mock_httpx_client)

        items = list(sync(client=client))

        assert len(items) == 2
        assert isinstance(items[0], GenerationEvent)
        assert items[0].delta == "Hello"
        assert isinstance(items[1], GenerationEvent)
        assert items[1].delta == "World"

    def test_async_yields_parsed_items(self, asyncio_func, GenerationEvent, CitationEvent, Client):
        """The async function should yield parsed items via streaming for each JSONL line"""
        lines = self._make_jsonl_lines()
        mock_response = _make_mock_stream_response(200, lines)

        mock_async_client = MagicMock(spec=httpx.AsyncClient)
        mock_async_client.stream = MagicMock(
            return_value=asynccontextmanager(async_yield(mock_response))()
        )

        client = Client(base_url="https://api.example.com")
        client.set_async_httpx_client(mock_async_client)

        async def collect():
            return [item async for item in asyncio_func(client=client)]

        items = _asyncio.run(collect())

        assert len(items) == 3

        assert isinstance(items[0], GenerationEvent)
        assert items[0].delta == "Hello"

        assert isinstance(items[1], CitationEvent)
        assert items[1].citation_id == "ref-1"
        assert items[1].url == "https://example.com"

        assert isinstance(items[2], GenerationEvent)
        assert items[2].delta == "World"


def async_yield(value):
    """Helper to create an async context manager that yields a value."""
    async def _inner():
        yield value
    return _inner
