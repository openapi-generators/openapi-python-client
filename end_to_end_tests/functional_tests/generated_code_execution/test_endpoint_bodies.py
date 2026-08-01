"""Functional tests for request body handling."""

import pytest

from end_to_end_tests.functional_tests.helpers import (
    with_generated_client_fixture,
    with_generated_code_import,
    with_generated_code_imports,
)

_DUPLICATE_CONTENT_TYPES_SPEC = """
components:
  schemas:
    MyBody:
      type: object
      properties:
        name:
          type: string
      required:
        - name
paths:
  /my-endpoint:
    post:
      operationId: my_endpoint
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MyBody'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/MyBody'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/MyBody'
      responses:
        '200':
          description: Success
"""


@with_generated_client_fixture(_DUPLICATE_CONTENT_TYPES_SPEC)
@with_generated_code_imports(
    ".models.MyBody",
)
@with_generated_code_import(".api.default.my_endpoint._get_kwargs", alias="get_kwargs")
class TestDuplicateContentTypesUseSameRef:
    """When all content types in a requestBody reference the same $ref schema,
    the generated code should use a body_content_type parameter for dispatch
    instead of isinstance checks (which would all pass for the same type)."""

    def test_defaults_to_json(self, MyBody, get_kwargs):
        """Without specifying body_content_type, the default content type (first in spec) is used."""
        body = MyBody(name="test")
        result = get_kwargs(body=body)
        assert "json" in result, "Expected JSON body by default"
        assert result.get("headers", {}).get("Content-Type") == "application/json"

    def test_form_urlencoded(self, MyBody, get_kwargs):
        """Passing body_content_type='application/x-www-form-urlencoded' sends form data."""
        body = MyBody(name="test")
        result = get_kwargs(body=body, body_content_type="application/x-www-form-urlencoded")
        assert "data" in result, "Expected form-urlencoded body"
        assert result.get("headers", {}).get("Content-Type") == "application/x-www-form-urlencoded"

    def test_multipart(self, MyBody, get_kwargs):
        """Passing body_content_type='multipart/form-data' sends multipart data."""
        body = MyBody(name="test")
        result = get_kwargs(body=body, body_content_type="multipart/form-data")
        assert "files" in result, "Expected multipart body"

    def test_json_and_multipart_are_exclusive(self, MyBody, get_kwargs):
        """JSON and multipart dispatches must be mutually exclusive (not both applied)."""
        body = MyBody(name="test")
        json_result = get_kwargs(body=body, body_content_type="application/json")
        assert "files" not in json_result
        assert "data" not in json_result

        multipart_result = get_kwargs(body=body, body_content_type="multipart/form-data")
        assert "json" not in multipart_result
        assert "data" not in multipart_result
