from unittest.mock import MagicMock

import httpx
import pytest

from end_to_end_tests.functional_tests.helpers import (
    with_generated_client_fixture,
    with_generated_code_imports,
)


@with_generated_client_fixture(
    """
paths:
  /organizations/{organization}/resources/{resource_id}:
    get:
      operationId: getResource
      parameters:
        - name: organization
          in: path
          required: true
          schema:
            type: string
        - name: resource_id
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
"""
)
@with_generated_code_imports(
    ".api.default.get_resource.sync_detailed",
    ".client.Client",
)
class TestPathParameterEncoding:
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
            organization="org/with/slashes",
            resource_id="id?with=query&chars",
            client=client,
        )

        # Verify the request was made with properly encoded URL
        mock_httpx_client.request.assert_called_once()
        call_kwargs = mock_httpx_client.request.call_args[1]

        # The URL should have encoded slashes and query characters
        expected_url = "/organizations/org%2Fwith%2Fslashes/resources/id%3Fwith%3Dquery%26chars"
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
            organization="org with spaces",
            resource_id="id with spaces",
            client=client,
        )

        mock_httpx_client.request.assert_called_once()
        call_kwargs = mock_httpx_client.request.call_args[1]

        # Spaces should be encoded as %20
        expected_url = "/organizations/org%20with%20spaces/resources/id%20with%20spaces"
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
            organization="org#1",
            resource_id="resource#id",
            client=client,
        )

        mock_httpx_client.request.assert_called_once()
        call_kwargs = mock_httpx_client.request.call_args[1]

        # Hash should be encoded as %23
        expected_url = "/organizations/org%231/resources/resource%23id"
        assert call_kwargs["url"] == expected_url

    def test_path_params_normal_chars_still_work(self, sync_detailed, Client):
        """Test that normal path parameters without special characters still work"""
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
            organization="my-org",
            resource_id="resource-123",
            client=client,
        )

        mock_httpx_client.request.assert_called_once()
        call_kwargs = mock_httpx_client.request.call_args[1]

        # Normal characters (alphanumeric, hyphens) should still be encoded but look the same
        expected_url = "/organizations/my-org/resources/resource-123"
        assert call_kwargs["url"] == expected_url
