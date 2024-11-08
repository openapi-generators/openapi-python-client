
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
        dateProp: {"type": "string", "format": "date", "default": "2024-01-02"}
        dateTimeProp: {"type": "string", "format": "date-time", "default": "2024-01-02T03:04:05Z"}
        uuidProp: {"type": "string", "format": "uuid", "default": "07EF8B4D-AA09-4FFA-898D-C710796AFF41"}
        anyPropWithString: {"default": "b"}
        anyPropWithInt: {"default": 3}
        booleanWithStringTrue1: {"type": "boolean", "default": "True"}
        booleanWithStringTrue2: {"type": "boolean", "default": "true"}
        booleanWithStringFalse1: {"type": "boolean", "default": "False"}
        booleanWithStringFalse2: {"type": "boolean", "default": "false"}
        intWithStringValue: {"type": "integer", "default": "4"}
        numberWithIntValue: {"type": "number", "default": 5}
        numberWithStringValue: {"type": "number", "default": "5.5"}
        stringWithNumberValue: {"type": "string", "default": 6}
        stringConst: {"type": "string", "const": "always", "default": "always"}
""")
@with_generated_code_imports(".models.MyModel")
class TestSimpleDefaults:
    # Note, the null/None type is not covered here due to a known bug:
    # https://github.com/openapi-generators/openapi-python-client/issues/1162
    def test_defaults_in_initializer(self, MyModel):
        instance = MyModel()
        assert instance == MyModel(
            boolean_prop=True,
            string_prop="a",
            number_prop=1.5,
            int_prop=2,
            date_prop=datetime.date(2024, 1, 2),
            date_time_prop=datetime.datetime(2024, 1, 2, 3, 4, 5, tzinfo=datetime.timezone.utc),
            uuid_prop=uuid.UUID("07EF8B4D-AA09-4FFA-898D-C710796AFF41"),
            any_prop_with_string="b",
            any_prop_with_int=3,
            boolean_with_string_true_1=True,
            boolean_with_string_true_2=True,
            boolean_with_string_false_1=False,
            boolean_with_string_false_2=False,
            int_with_string_value=4,
            number_with_int_value=5,
            number_with_string_value=5.5,
            string_with_number_value="6",
            string_const="always",
        )



@with_generated_client_fixture(
"""
components:
  schemas:
    MyEnum:
      type: string
      enum: ["a", "b"]
    MyModel:
      type: object
      properties:
        enumProp:
          allOf:
            - $ref: "#/components/schemas/MyEnum"
          default: "a"

""")
@with_generated_code_imports(".models.MyEnum", ".models.MyModel")
class TestEnumDefaults:
    def test_enum_default(self, MyEnum, MyModel):
        assert MyModel().enum_prop == MyEnum.A


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
        ]
    )
    def test_bad_default_warning(self, model_name, message, warnings):
        assert_bad_schema_warning(warnings, model_name, message)
