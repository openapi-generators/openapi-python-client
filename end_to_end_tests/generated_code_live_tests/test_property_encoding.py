
import datetime
import uuid
import pytest
from end_to_end_tests.end_to_end_test_helpers import (
    assert_model_decode_encode,
    with_generated_code_import,
    with_generated_client_fixture,
)


@with_generated_client_fixture(
"""
paths: {}
components:
  schemas:
    MyModel:
      type: object
      properties:
        req1: {"type": "string"}
        req2: {"type": "string"}
        opt: {"type": "string"}
      required: ["req1", "req2"]
    DerivedModel:
      allOf:
        - $ref: "#/components/schemas/MyModel"
        - type: object
          properties:
            req3: {"type": "string"}
          required: ["req3"]
""")
@with_generated_code_import(".models.MyModel")
@with_generated_code_import(".models.DerivedModel")
class TestRequiredAndOptionalProperties:
    def test_required_ok(self, MyModel, DerivedModel):
        assert_model_decode_encode(
            MyModel,
            {"req1": "a", "req2": "b"},
            MyModel(req1="a", req2="b"),
        )
        assert_model_decode_encode(
            DerivedModel,
            {"req1": "a", "req2": "b", "req3": "c"},
            DerivedModel(req1="a", req2="b", req3="c"),
        )

    def test_required_and_optional(self, MyModel, DerivedModel):
        assert_model_decode_encode(
            MyModel,
            {"req1": "a", "req2": "b", "opt": "c"},
            MyModel(req1="a", req2="b", opt="c"),
        )
        assert_model_decode_encode(
            DerivedModel,
            {"req1": "a", "req2": "b", "req3": "c", "opt": "d"},
            DerivedModel(req1="a", req2="b", req3="c", opt="d"),
        )

    def test_required_missing(self, MyModel, DerivedModel):
        with pytest.raises(KeyError):
            MyModel.from_dict({"requiredA": "a"})
        with pytest.raises(KeyError):
            MyModel.from_dict({"requiredB": "b"})
        with pytest.raises(KeyError):
            DerivedModel.from_dict({"requiredA": "a", "requiredB": "b"})


@with_generated_client_fixture(
"""
paths: {}
components:
  schemas:
    MyModel:
      type: object
      properties:
        booleanProp: {"type": "boolean"}
        stringProp: {"type": "string"}
        numberProp: {"type": "number"}
        intProp: {"type": "integer"}
        arrayOfStringsProp: {"type": "array", "items": {"type": "string"}}
        anyObjectProp: {"$ref": "#/components/schemas/AnyObject"}
        nullProp: {"type": "null"}
    AnyObject:
        type: object
""")
@with_generated_code_import(".models.MyModel")
@with_generated_code_import(".models.AnyObject")
class TestBasicModelProperties:
    def test_decode_encode(self, MyModel, AnyObject):
        json_data = {
            "booleanProp": True,
            "stringProp": "a",
            "numberProp": 1.5,
            "intProp": 2,
            "arrayOfStringsProp": ["b", "c"],
            "anyObjectProp": {"d": 3},
            "nullProp": None,
        }
        expected_any_object = AnyObject()
        expected_any_object.additional_properties = {"d": 3}
        assert_model_decode_encode(
            MyModel,
            json_data,
            MyModel(
                boolean_prop=True,
                string_prop="a",
                number_prop=1.5,
                int_prop=2,
                array_of_strings_prop=["b", "c"],
                any_object_prop = expected_any_object,
                null_prop=None,
            )
        )

    @pytest.mark.parametrize(
        "bad_data",
        ["a", True, 2, None],
    )
    def test_decode_error_not_object(self, bad_data, MyModel):
        with pytest.raises(Exception):
            # Exception is overly broad, but unfortunately in the current implementation, the error
            # being raised is AttributeError (because it tries to call bad_data.copy()) which isn't
            # very meaningful
            MyModel.from_dict(bad_data)


@with_generated_client_fixture(
"""
paths: {}
components:
  schemas:
    MyModel:
      type: object
      properties:
        dateProp: {"type": "string", "format": "date"}
        dateTimeProp: {"type": "string", "format": "date-time"}
        uuidProp: {"type": "string", "format": "uuid"}
""")
@with_generated_code_import(".models.MyModel")
class TestSpecialStringFormats:
    def test_date(self, MyModel):
        date_value = datetime.date.today()
        json_data = {"dateProp": date_value.isoformat()}
        assert_model_decode_encode(MyModel, json_data, MyModel(date_prop=date_value))

    def test_date_time(self, MyModel):
        date_time_value = datetime.datetime.now(datetime.timezone.utc)
        json_data = {"dateTimeProp": date_time_value.isoformat()}
        assert_model_decode_encode(MyModel, json_data, MyModel(date_time_prop=date_time_value))

    def test_uuid(self, MyModel):
        uuid_value = uuid.uuid1()
        json_data = {"uuidProp": str(uuid_value)}
        assert_model_decode_encode(MyModel, json_data, MyModel(uuid_prop=uuid_value))
