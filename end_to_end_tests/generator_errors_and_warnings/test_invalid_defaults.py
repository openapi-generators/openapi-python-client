import pytest
from end_to_end_tests.end_to_end_test_helpers import (
    assert_bad_schema_warning,
    inline_spec_should_cause_warnings,
)


class TestInvalidDefaultValues:
    @pytest.fixture(scope="class")
    def warnings(self):
        return inline_spec_should_cause_warnings(
"""
components:
  schemas:
    WithBadBoolean:
      properties:
        badBoolean: {"type": "boolean", "default": "not a boolean"}
    WithBadIntAsString:
      properties:
        badInt: {"type": "integer", "default": "not an int"}
    WithBadIntAsOther:
      properties:
        badInt: {"type": "integer", "default": true}
    WithBadFloatAsString:
      properties:
        badInt: {"type": "number", "default": "not a number"}
    WithBadFloatAsOther:
      properties:
        badInt: {"type": "number", "default": true}
    WithBadDateAsString:
      properties:
        badDate: {"type": "string", "format": "date", "default": "xxx"}
    WithBadDateAsOther:
      properties:
        badDate: {"type": "string", "format": "date", "default": 3}
    WithBadDateTimeAsString:
      properties:
        badDate: {"type": "string", "format": "date-time", "default": "xxx"}
    WithBadDateTimeAsOther:
      properties:
        badDate: {"type": "string", "format": "date-time", "default": 3}
    WithBadUuidAsString:
      properties:
        badUuid: {"type": "string", "format": "uuid", "default": "xxx"}
    WithBadUuidAsOther:
      properties:
        badUuid: {"type": "string", "format": "uuid", "default": 3}
    WithBadEnum:
      properties:
        badEnum: {"type": "string", "enum": ["a", "b"], "default": "x"}
    GoodEnum:
      type: string
      enum: ["a", "b"]
    OverriddenEnumWithBadDefault:
      properties:
        badEnum:
          allOf:
            - $ref: "#/components/schemas/GoodEnum"
          default: "x"
    UnionWithNoValidDefault:
      properties:
        badBoolOrInt:
          anyOf:
            - type: boolean
            - type: integer
          default: "xxx"
"""
        )
    # Note, the null/None type, and binary strings (files), are not covered here due to a known bug:
    # https://github.com/openapi-generators/openapi-python-client/issues/1162

    @pytest.mark.parametrize(
        ("model_name", "message"),
        [
            ("WithBadBoolean", "Invalid boolean value"),
            ("WithBadIntAsString", "Invalid int value"),
            ("WithBadIntAsOther", "Invalid int value"),
            ("WithBadFloatAsString", "Invalid float value"),
            ("WithBadFloatAsOther", "Cannot convert True to a float"),
            ("WithBadDateAsString", "Invalid date"),
            ("WithBadDateAsOther", "Cannot convert 3 to a date"),
            ("WithBadDateTimeAsString", "Invalid datetime"),
            ("WithBadDateTimeAsOther", "Cannot convert 3 to a datetime"),
            ("WithBadUuidAsString", "Invalid UUID value"),
            ("WithBadUuidAsOther", "Invalid UUID value"),
            ("WithBadEnum", "Value x is not valid for enum"),
            ("OverriddenEnumWithBadDefault", "Value x is not valid for enum"),
            ("UnionWithNoValidDefault", "Invalid int value"),
        ]
    )
    def test_bad_default_warning(self, model_name, message, warnings):
        assert_bad_schema_warning(warnings, model_name, message)
