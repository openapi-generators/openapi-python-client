"""Path parameters must be URL-encoded before they are spliced into the path.

An unencoded value that contains `/`, `?`, `#` or a space does not just produce a wrong URL -- it
changes which resource is addressed, so a caller passing an id with a slash in it would silently hit
a different endpoint.

Assertions are on `httpx.Request.url.raw_path`, the bytes that go on the wire, so they cover both the
generator's encoding and httpx's own URL handling. `url.path` is the decoded form and would report
`item/with/slashes` as though nothing had been encoded.
"""

import pytest

from end_to_end_tests.functional_tests.helpers import (
    call_recording_requests,
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
@with_generated_code_import(".api.default.get_item_detail.request", alias="get_item_detail")
@with_generated_code_import(".client.Client")
class TestPathParameterEncoding:
    @pytest.mark.parametrize(
        ("item_id", "detail_id", "expected_raw_path"),
        [
            pytest.param(
                "item123",
                "detail456",
                b"/items/item123/details/detail456",
                id="normal chars are left alone",
            ),
            pytest.param(
                "item/with/slashes",
                "detail?with=query&chars",
                b"/items/item%2Fwith%2Fslashes/details/detail%3Fwith%3Dquery%26chars",
                id="reserved chars are encoded",
            ),
            pytest.param(
                "item with spaces",
                "detail with spaces",
                b"/items/item%20with%20spaces/details/detail%20with%20spaces",
                id="spaces are encoded",
            ),
            pytest.param(
                "item#1",
                "detail#id",
                b"/items/item%231/details/detail%23id",
                id="fragment chars are encoded",
            ),
        ],
    )
    def test_path_params_are_encoded(self, get_item_detail, Client, item_id, detail_id, expected_raw_path):
        requests = call_recording_requests(
            Client,
            get_item_detail,
            json={"id": "test"},
            item_id=item_id,
            detail_id=detail_id,
        )

        assert len(requests) == 1
        assert requests[0].url.raw_path == expected_raw_path
