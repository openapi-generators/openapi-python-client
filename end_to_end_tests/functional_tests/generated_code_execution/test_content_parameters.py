from unittest.mock import MagicMock

import httpx

from end_to_end_tests.functional_tests.helpers import (
    with_generated_client_fixture,
    with_generated_code_import,
)


@with_generated_client_fixture(
"""
paths:
  "/items/{item_id}":
    get:
      operationId: getItem
      parameters:
        - name: item_id
          in: path
          required: true
          content:
            application/json:
              schema:
                type: string
                enum: [a, b, c]
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                type: string
""")
@with_generated_code_import(".api.default.get_item.sync_detailed")
@with_generated_code_import(".client.Client")
class TestContentOnlyPathParameters:
    def test_content_only_path_parameter_generates_callable_endpoint(self, sync_detailed, Client):
        mock_httpx_client = MagicMock(spec=httpx.Client)
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = "ok"
        mock_response.content = b'"ok"'
        mock_response.headers = {}
        mock_httpx_client.request.return_value = mock_response

        client = Client(base_url="https://api.example.com")
        client.set_httpx_client(mock_httpx_client)

        response = sync_detailed(item_id="a", client=client)

        mock_httpx_client.request.assert_called_once()
        call_kwargs = mock_httpx_client.request.call_args[1]
        assert call_kwargs["url"] == "/items/a"
        assert response.parsed == "ok"
