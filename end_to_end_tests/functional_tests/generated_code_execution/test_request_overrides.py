from unittest.mock import MagicMock

import httpx
import pytest

from end_to_end_tests.functional_tests.helpers import (
    with_generated_client_fixture,
    with_generated_code_import,
)


SIMPLE_SPEC = """
paths:
  "/items":
    get:
      operationId: getItems
      responses:
        "200":
          description: Success
"""

SPEC_WITH_HEADER_PARAM = """
paths:
  "/items":
    get:
      operationId: getItems
      parameters:
        - name: X-Request-Id
          in: header
          required: true
          schema:
            type: string
      responses:
        "200":
          description: Success
"""


def _make_mock_client(Client):
    mock_httpx_client = MagicMock(spec=httpx.Client)
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.content = b""
    mock_response.headers = {}
    mock_httpx_client.request.return_value = mock_response
    client = Client(base_url="https://api.example.com")
    client.set_httpx_client(mock_httpx_client)
    return client, mock_httpx_client


@with_generated_client_fixture(SIMPLE_SPEC)
@with_generated_code_import(".api.default.get_items.sync_detailed")
@with_generated_code_import(".client.Client")
class TestPerRequestHeaders:
    def test_extra_headers_are_forwarded(self, sync_detailed, Client):
        client, mock_httpx = _make_mock_client(Client)
        sync_detailed(client=client, headers={"X-Trace-Id": "abc123"})
        call_kwargs = mock_httpx.request.call_args[1]
        assert call_kwargs["headers"]["X-Trace-Id"] == "abc123"

    def test_omitting_headers_does_not_inject_headers_key(self, sync_detailed, Client):
        client, mock_httpx = _make_mock_client(Client)
        sync_detailed(client=client)
        call_kwargs = mock_httpx.request.call_args[1]
        # No spec-defined headers and no override — headers key should be absent
        assert "headers" not in call_kwargs

    def test_multiple_extra_headers_are_all_forwarded(self, sync_detailed, Client):
        client, mock_httpx = _make_mock_client(Client)
        sync_detailed(client=client, headers={"X-A": "1", "X-B": "2"})
        call_kwargs = mock_httpx.request.call_args[1]
        assert call_kwargs["headers"]["X-A"] == "1"
        assert call_kwargs["headers"]["X-B"] == "2"


@with_generated_client_fixture(SPEC_WITH_HEADER_PARAM)
@with_generated_code_import(".api.default.get_items.sync_detailed")
@with_generated_code_import(".client.Client")
class TestPerRequestHeadersWithSpecHeaders:
    def test_caller_header_overrides_spec_header(self, sync_detailed, Client):
        client, mock_httpx = _make_mock_client(Client)
        sync_detailed(client=client, x_request_id="spec-value", headers={"X-Request-Id": "override"})
        call_kwargs = mock_httpx.request.call_args[1]
        assert call_kwargs["headers"]["X-Request-Id"] == "override"

    def test_caller_headers_merged_with_spec_headers(self, sync_detailed, Client):
        client, mock_httpx = _make_mock_client(Client)
        sync_detailed(client=client, x_request_id="spec-value", headers={"X-Extra": "extra"})
        call_kwargs = mock_httpx.request.call_args[1]
        assert call_kwargs["headers"]["X-Request-Id"] == "spec-value"
        assert call_kwargs["headers"]["X-Extra"] == "extra"


@with_generated_client_fixture(SIMPLE_SPEC)
@with_generated_code_import(".api.default.get_items.sync_detailed")
@with_generated_code_import(".client.Client")
class TestPerRequestTimeout:
    def test_timeout_override_is_forwarded(self, sync_detailed, Client):
        client, mock_httpx = _make_mock_client(Client)
        sync_detailed(client=client, timeout=httpx.Timeout(120.0))
        call_kwargs = mock_httpx.request.call_args[1]
        assert call_kwargs["timeout"] == httpx.Timeout(120.0)

    def test_timeout_none_disables_timeout(self, sync_detailed, Client):
        client, mock_httpx = _make_mock_client(Client)
        sync_detailed(client=client, timeout=None)
        call_kwargs = mock_httpx.request.call_args[1]
        assert call_kwargs["timeout"] is None

    def test_omitting_timeout_does_not_inject_timeout_key(self, sync_detailed, Client):
        client, mock_httpx = _make_mock_client(Client)
        sync_detailed(client=client)
        call_kwargs = mock_httpx.request.call_args[1]
        assert "timeout" not in call_kwargs


@with_generated_client_fixture(SIMPLE_SPEC)
@with_generated_code_import(".api.default.get_items.sync_detailed")
@with_generated_code_import(".client.Client")
class TestPerRequestAuth:
    def test_auth_override_is_forwarded(self, sync_detailed, Client):
        client, mock_httpx = _make_mock_client(Client)
        auth = httpx.BasicAuth("user", "pass")
        sync_detailed(client=client, auth=auth)
        call_kwargs = mock_httpx.request.call_args[1]
        assert call_kwargs["auth"] is auth

    def test_auth_none_disables_auth(self, sync_detailed, Client):
        client, mock_httpx = _make_mock_client(Client)
        sync_detailed(client=client, auth=None)
        call_kwargs = mock_httpx.request.call_args[1]
        assert call_kwargs["auth"] is None

    def test_omitting_auth_does_not_inject_auth_key(self, sync_detailed, Client):
        client, mock_httpx = _make_mock_client(Client)
        sync_detailed(client=client)
        call_kwargs = mock_httpx.request.call_args[1]
        assert "auth" not in call_kwargs
