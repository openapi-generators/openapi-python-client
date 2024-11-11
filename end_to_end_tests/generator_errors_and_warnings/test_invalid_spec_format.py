import pytest
from end_to_end_tests.end_to_end_test_helpers import (
    assert_bad_schema_warning,
    inline_spec_should_cause_warnings,
    inline_spec_should_fail,
)


class TestInvalidSpecFormats:
    def test_missing_openapi_version(self):
        result = inline_spec_should_fail(
"""
info:
  title: My API
  version: "1.0"
paths: {}
""",
            add_missing_sections=False,
        )
        for text in ["Failed to parse OpenAPI document", "1 validation error", "openapi"]:
            assert text in result.output

    def test_missing_title(self):
        result = inline_spec_should_fail(
"""
info:
  version: "1.0"
openapi: "3.1.0"
paths: {}
""",
            add_missing_sections=False,
        )
        for text in ["Failed to parse OpenAPI document", "1 validation error", "title"]:
            assert text in result.output

    def test_missing_version(self):
        result = inline_spec_should_fail(
"""
info:
  title: My API
openapi: "3.1.0"
paths: {}
""",
            add_missing_sections=False,
        )
        for text in ["Failed to parse OpenAPI document", "1 validation error", "version"]:
            assert text in result.output

    def test_missing_paths(self):
        result = inline_spec_should_fail(
"""
info:
  title: My API
  version: "1.0"
openapi: "3.1.0"
""",
            add_missing_sections=False,
        )
        for text in ["Failed to parse OpenAPI document", "1 validation error", "paths"]:
            assert text in result.output

    def test_swagger_unsupported(self):
        result = inline_spec_should_fail(
"""
swagger: "2.0"
info:
  title: My API
  version: "1.0"
openapi: "3.1"
paths: {}
components: {}
""",
            add_missing_sections=False,
        )
        assert "You may be trying to use a Swagger document; this is not supported by this project." in result.output
