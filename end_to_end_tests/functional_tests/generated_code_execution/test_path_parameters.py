from unittest.mock import MagicMock

import httpx
import pytest

from end_to_end_tests.functional_tests.helpers import (
    with_generated_client_fixture,
    with_generated_code_import,
)


@with_generated_client_fixture(
"""
paths:
  "/items/{item_id}/details/{detail_id}":
    get:
      operationId: getItemDetail
      parameters:
        - name: item_id
          in: path
          required: true
          schema:
            type: string
        - name: detail_id
          in: path
          required: true
          schema:
            type: string
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: string
""")
@with_generated_code_import(".api.default.get_item_detail.sync_detailed")
@with_generated_code_import(".client.Client")
class TestPathParameterEncoding:
    """Test that path parameters are properly URL-encoded"""

    def test_path_params_with_normal_chars_work(self, sync_detailed, Client):
        """Test that normal alphanumeric path parameters still work correctly"""
        mock_httpx_client = MagicMock(spec=httpx.Client)
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "test"}
        mock_response.content = b'{"id": "test"}'
        mock_response.headers = {}
        mock_httpx_client.request.return_value = mock_response

        client = Client(base_url="https://api.example.com")
        client.set_httpx_client(mock_httpx_client)

        sync_detailed(
            item_id="item123",
            detail_id="detail456",
            client=client,
        )

        mock_httpx_client.request.assert_called_once()
        call_kwargs = mock_httpx_client.request.call_args[1]

        # Normal characters should remain unchanged
        expected_url = "/items/item123/details/detail456"
        assert call_kwargs["url"] == expected_url

    def test_path_params_with_reserved_chars_are_encoded(self, sync_detailed, Client):
        """Test that path parameters with reserved characters are properly URL-encoded"""
        # Create a mock httpx client
        mock_httpx_client = MagicMock(spec=httpx.Client)
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "test"}
        mock_response.content = b'{"id": "test"}'
        mock_response.headers = {}
        mock_httpx_client.request.return_value = mock_response

        # Create a client with the mock httpx client
        client = Client(base_url="https://api.example.com")
        client.set_httpx_client(mock_httpx_client)

        # Call the endpoint with path parameters containing reserved characters
        sync_detailed(
            item_id="item/with/slashes",
            detail_id="detail?with=query&chars",
            client=client,
        )

        # Verify the request was made with properly encoded URL
        mock_httpx_client.request.assert_called_once()
        call_kwargs = mock_httpx_client.request.call_args[1]

        # The URL should have encoded slashes and query characters
        expected_url = "/items/item%2Fwith%2Fslashes/details/detail%3Fwith%3Dquery%26chars"
        assert call_kwargs["url"] == expected_url

    def test_path_params_with_spaces_are_encoded(self, sync_detailed, Client):
        """Test that path parameters with spaces are properly URL-encoded"""
        mock_httpx_client = MagicMock(spec=httpx.Client)
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "test"}
        mock_response.content = b'{"id": "test"}'
        mock_response.headers = {}
        mock_httpx_client.request.return_value = mock_response

        client = Client(base_url="https://api.example.com")
        client.set_httpx_client(mock_httpx_client)

        sync_detailed(
            item_id="item with spaces",
            detail_id="detail with spaces",
            client=client,
        )

        mock_httpx_client.request.assert_called_once()
        call_kwargs = mock_httpx_client.request.call_args[1]

        # Spaces should be encoded as %20
        expected_url = "/items/item%20with%20spaces/details/detail%20with%20spaces"
        assert call_kwargs["url"] == expected_url

    def test_path_params_with_hash_are_encoded(self, sync_detailed, Client):
        """Test that path parameters with hash/fragment characters are properly URL-encoded"""
        mock_httpx_client = MagicMock(spec=httpx.Client)
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "test"}
        mock_response.content = b'{"id": "test"}'
        mock_response.headers = {}
        mock_httpx_client.request.return_value = mock_response

        client = Client(base_url="https://api.example.com")
        client.set_httpx_client(mock_httpx_client)

        sync_detailed(
            item_id="item#1",
            detail_id="detail#id",
            client=client,
        )

        mock_httpx_client.request.assert_called_once()
        call_kwargs = mock_httpx_client.request.call_args[1]

        # Hash should be encoded as %23
        expected_url = "/items/item%231/details/detail%23id"
        assert call_kwargs["url"] == expected_url
