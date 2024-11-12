import datetime
from typing import Any, ForwardRef, Union
import uuid
import pytest
from end_to_end_tests.end_to_end_test_helpers import (
    assert_model_decode_encode,
    assert_model_property_type_hint,
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
@with_generated_code_imports(
    ".models.MyModel",
    ".models.DerivedModel",
    ".types.Unset",
)
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
            MyModel.from_dict({"req1": "a"})
        with pytest.raises(KeyError):
            MyModel.from_dict({"req2": "b"})
        with pytest.raises(KeyError):
            DerivedModel.from_dict({"req1": "a", "req2": "b"})

    def test_type_hints(self, MyModel, Unset):
        assert_model_property_type_hint(MyModel, "req1", str)
        assert_model_property_type_hint(MyModel, "opt", Union[str, Unset])


@with_generated_client_fixture(
"""
components:
  schemas:
    MyModel:
      type: object
      properties:
        booleanProp: {"type": "boolean"}
        stringProp: {"type": "string"}
        numberProp: {"type": "number"}
        intProp: {"type": "integer"}
        anyObjectProp: {"$ref": "#/components/schemas/AnyObject"}
        nullProp: {"type": "null"}
        anyProp: {}
    AnyObject:
        type: object
""")
@with_generated_code_imports(
    ".models.MyModel",
    ".models.AnyObject",
    ".types.Unset",
)
class TestBasicModelProperties:
    def test_decode_encode(self, MyModel, AnyObject):
        json_data = {
            "booleanProp": True,
            "stringProp": "a",
            "numberProp": 1.5,
            "intProp": 2,
            "anyObjectProp": {"d": 3},
            "nullProp": None,
            "anyProp": "e"
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
                any_object_prop = expected_any_object,
                null_prop=None,
                any_prop="e",
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

    def test_type_hints(self, MyModel, Unset):
        assert_model_property_type_hint(MyModel, "boolean_prop", Union[bool, Unset])
        assert_model_property_type_hint(MyModel, "string_prop", Union[str, Unset])
        assert_model_property_type_hint(MyModel, "number_prop", Union[float, Unset])
        assert_model_property_type_hint(MyModel, "int_prop", Union[int, Unset])
        assert_model_property_type_hint(MyModel, "any_object_prop", Union[ForwardRef("AnyObject"), Unset])
        assert_model_property_type_hint(MyModel, "null_prop", Union[None, Unset])
        assert_model_property_type_hint(MyModel, "any_prop", Union[Any, Unset])


@with_generated_client_fixture(
"""
components:
  schemas:
    MyModel:
      type: object
      properties:
        dateProp: {"type": "string", "format": "date"}
        dateTimeProp: {"type": "string", "format": "date-time"}
        uuidProp: {"type": "string", "format": "uuid"}
        unknownFormatProp: {"type": "string", "format": "weird"}
""")
@with_generated_code_imports(
    ".models.MyModel",
    ".types.Unset",
)
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

    def test_unknown_format(self, MyModel):
        json_data = {"unknownFormatProp": "whatever"}
        assert_model_decode_encode(MyModel, json_data, MyModel(unknown_format_prop="whatever"))

    def test_type_hints(self, MyModel, Unset):
        assert_model_property_type_hint(MyModel, "date_prop", Union[datetime.date, Unset])
        assert_model_property_type_hint(MyModel, "date_time_prop", Union[datetime.datetime, Unset])
        assert_model_property_type_hint(MyModel, "uuid_prop", Union[uuid.UUID, Unset])
        assert_model_property_type_hint(MyModel, "unknown_format_prop", Union[str, Unset])
