
import datetime
import uuid
import pytest
from end_to_end_tests.end_to_end_test_helpers import (
    assert_bad_schema_warning,
    assert_model_decode_encode,
    inline_spec_should_cause_warnings,
    with_generated_client_fixture,
    with_generated_code_imports,
)


@with_generated_client_fixture(
"""
components:
  schemas:
    MyModel:
      type: object
      properties:
        booleanProp: {"type": "boolean", "default": true}
        stringProp: {"type": "string", "default": "a"}
        numberProp: {"type": "number", "default": 1.5}
        intProp: {"type": "integer", "default": 2}
        noneProp: {"type": "null", "default": null}
        anyPropWithString: {"default": "b"}
        anyPropWithInt: {"default": 3}
        booleanWithStringTrue1: {"type": "boolean", "default": "True"}
        booleanWithStringTrue2: {"type": "boolean", "default": "true"}
        booleanWithStringFalse1: {"type": "boolean", "default": "False"}
        booleanWithStringFalse2: {"type": "boolean", "default": "false"}
        intWithStringValue: {"type": "integer", "default": "4"}
        numberWithIntValue: {"type": "number", "default": 5}
        numberWithStringValue: {"type": "number", "default": "5.5"}
        noneWithStringValue: {"type": "null", "default": "None"}
""")
@with_generated_code_imports(".models.MyModel")
class TestDefaultValues:
    def test_defaults_in_initializer(self, MyModel, generated_client):
        instance = MyModel()
        assert instance == MyModel(
            boolean_prop=True,
            string_prop="a",
            number_prop=1.5,
            int_prop=2,
            any_prop_with_string="b",
            any_prop_with_int=3,
            boolean_with_string_true_1=True,
            boolean_with_string_true_2=True,
            boolean_with_string_false_1=False,
            boolean_with_string_false_2=False,
            int_with_string_value=4,
            number_with_int_value=5,
            number_with_string_value=5.5,
        )
        # Note, currently the default for a None property does not work as expected--
        # the initializer will default it to UNSET rather than None.


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
"""
        )

    def test_bad_boolean(self, warnings):
        assert_bad_schema_warning(warnings, "WithBadBoolean", "Invalid boolean value")

    def test_bad_int_as_string(self, warnings):
        assert_bad_schema_warning(warnings, "WithBadIntAsString", "Invalid int value")

    def test_bad_int_as_other(self, warnings):
        assert_bad_schema_warning(warnings, "WithBadIntAsOther", "Invalid int value")

    def test_bad_float_as_string(self, warnings):
        assert_bad_schema_warning(warnings, "WithBadFloatAsString", "Invalid float value")

    def test_bad_float_as_other(self, warnings):
        assert_bad_schema_warning(warnings, "WithBadFloatAsOther", "Cannot convert True to a float")
