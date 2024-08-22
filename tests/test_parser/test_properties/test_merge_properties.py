import pytest
from attr import evolve

from openapi_python_client.parser.properties import StringProperty
from openapi_python_client.parser.properties.float import FloatProperty
from openapi_python_client.parser.properties.int import IntProperty
from openapi_python_client.parser.properties.merge_properties import merge_properties
from openapi_python_client.parser.properties.schemas import Class

MODULE_NAME = "openapi_python_client.parser.properties.merge_properties"


def test_merge_basic_attributes_same_type(
    boolean_property_factory,
    int_property_factory,
    float_property_factory,
    string_property_factory,
    list_property_factory,
    model_property_factory,
):
    basic_props = [
        boolean_property_factory(default=True),
        int_property_factory(default=1),
        float_property_factory(default=1.5),
        string_property_factory(default="x"),
        list_property_factory(),
        model_property_factory(),
    ]
    for basic_prop in basic_props:
        with_required = evolve(basic_prop, required=True)
        assert merge_properties(basic_prop, with_required) == with_required
        assert merge_properties(with_required, basic_prop) == with_required
        without_default = evolve(basic_prop, default=None)
        assert merge_properties(basic_prop, without_default) == basic_prop
        assert merge_properties(without_default, basic_prop) == basic_prop
        with_desc1 = evolve(basic_prop, description="desc1")
        with_desc2 = evolve(basic_prop, description="desc2")
        assert merge_properties(basic_prop, with_desc1) == with_desc1
        assert merge_properties(with_desc1, basic_prop) == with_desc1
        assert merge_properties(with_desc1, with_desc2) == with_desc2


def test_incompatible_types(
    boolean_property_factory,
    int_property_factory,
    float_property_factory,
    string_property_factory,
    list_property_factory,
    model_property_factory,
):
    props = [
        boolean_property_factory(default=True),
        int_property_factory(default=1),
        float_property_factory(default=1.5),
        string_property_factory(default="x"),
        list_property_factory(),
        model_property_factory(),
    ]
    for i, prop1 in enumerate(props):
        for j, prop2 in enumerate(props):
            if i != j:
                if {prop1.__class__, prop2.__class__} == {IntProperty, FloatProperty}:
                    continue  # the int+float case is covered in another test
                with pytest.raises(ValueError) as excinfo:
                    merge_properties(prop1, prop2)
                assert "incompatible types" in excinfo.value.args[0]


def test_merge_int_with_float(int_property_factory, float_property_factory):
    int_prop = int_property_factory(description="desc1")
    float_prop = float_property_factory(default=2, description="desc2")

    assert merge_properties(int_prop, float_prop) == (
        evolve(int_prop, default=float_prop.default, description=float_prop.description)
    )
    assert merge_properties(float_prop, int_prop) == (evolve(int_prop, default=float_prop.default))

    float_prop_with_non_int_default = evolve(float_prop, default=2.5)
    with pytest.raises(ValueError) as excinfo:
        merge_properties(int_prop, float_prop_with_non_int_default)
    assert "default value" in excinfo.value.args[0]


def test_merge_with_any(
    any_property_factory,
    boolean_property_factory,
    int_property_factory,
    float_property_factory,
    string_property_factory,
    model_property_factory,
):
    original_desc = "description"
    props = [
        boolean_property_factory(default=True, description=original_desc),
        int_property_factory(default=1, description=original_desc),
        float_property_factory(default=1.5, description=original_desc),
        string_property_factory(default="x", description=original_desc),
        model_property_factory(description=original_desc),
    ]
    any_prop = any_property_factory()
    for prop in props:
        expected_result = evolve(prop, description=original_desc, default=prop.default)
        assert merge_properties(any_prop, prop) == expected_result
        assert merge_properties(prop, any_prop) == expected_result


def test_merge_string_max_length(string_property_factory):
    prop_with_no_max = string_property_factory()
    prop_with_max_1 = evolve(prop_with_no_max, max_length=1)
    prop_with_max_5 = evolve(prop_with_no_max, max_length=5)

    assert merge_properties(prop_with_no_max, prop_with_max_1) == prop_with_max_1
    assert merge_properties(prop_with_max_1, prop_with_no_max) == prop_with_max_1

    assert merge_properties(prop_with_max_1, prop_with_max_5) == prop_with_max_1
    assert merge_properties(prop_with_max_5, prop_with_max_1) == prop_with_max_1


def test_merge_string_pattern(string_property_factory):
    prop_with_no_pattern = string_property_factory()
    prop_with_pattern1a = evolve(prop_with_no_pattern, pattern="pattern1")
    prop_with_pattern1b = evolve(prop_with_no_pattern, pattern="pattern1")  # deliberately identical pattern
    prop_with_pattern2 = evolve(prop_with_no_pattern, pattern="pattern2")

    assert merge_properties(prop_with_no_pattern, prop_with_pattern1a) == prop_with_pattern1a
    assert merge_properties(prop_with_pattern1a, prop_with_no_pattern) == prop_with_pattern1a

    assert merge_properties(prop_with_pattern1a, prop_with_pattern1b) == prop_with_pattern1a

    with pytest.raises(ValueError) as excinfo:
        merge_properties(prop_with_pattern1a, prop_with_pattern2)
    assert "regex patterns" in excinfo.value.args[0]


def test_merge_enums(enum_property_factory, config):
    enum_with_fewer_values = enum_property_factory(
        description="desc1",
        values={"A": "A", "B": "B"},
        value_type=str,
    )
    enum_with_more_values = enum_property_factory(
        example="example2",
        values={"A": "A", "B": "B", "C": "C"},
        value_type=str,
    )
    # Setting class_info separately because it doesn't get initialized by the constructor - we want
    # to make sure the right enum class name gets used in the merged property
    enum_with_fewer_values.class_info = Class.from_string(string="FewerValuesEnum", config=config)
    enum_with_more_values.class_info = Class.from_string(string="MoreValuesEnum", config=config)

    assert merge_properties(enum_with_fewer_values, enum_with_more_values) == evolve(
        enum_with_more_values,
        values=enum_with_fewer_values.values,
        class_info=enum_with_fewer_values.class_info,
        description=enum_with_fewer_values.description,
    )
    assert merge_properties(enum_with_more_values, enum_with_fewer_values) == evolve(
        enum_with_fewer_values,
        example=enum_with_more_values.example,
    )


def test_merge_string_with_string_enum(string_property_factory, enum_property_factory):
    values = {"A": "A", "B": "B"}
    string_prop = string_property_factory(default="default1", description="desc1", example="example1")
    enum_prop = enum_property_factory(
        default="default2",
        description="desc2",
        example="example2",
        values=values,
        value_type=str,
    )

    assert merge_properties(string_prop, enum_prop) == evolve(enum_prop, required=True)
    assert merge_properties(enum_prop, string_prop) == evolve(
        enum_prop,
        required=True,
        default=string_prop.default,
        description=string_prop.description,
        example=string_prop.example,
    )


def test_merge_int_with_int_enum(int_property_factory, enum_property_factory):
    values = {"VALUE_1": 1, "VALUE_2": 2}
    int_prop = int_property_factory(default=100, description="desc1", example="example1")
    enum_prop = enum_property_factory(
        default=200,
        description="desc2",
        example="example2",
        values=values,
        value_type=int,
    )

    assert merge_properties(int_prop, enum_prop) == evolve(enum_prop, required=True)
    assert merge_properties(enum_prop, int_prop) == evolve(
        enum_prop, required=True, default=int_prop.default, description=int_prop.description, example=int_prop.example
    )


def test_merge_with_incompatible_enum(
    boolean_property_factory,
    int_property_factory,
    float_property_factory,
    string_property_factory,
    enum_property_factory,
    model_property_factory,
):
    props = [
        boolean_property_factory(),
        int_property_factory(),
        float_property_factory(),
        string_property_factory(),
        model_property_factory(),
    ]
    string_enum_prop = enum_property_factory(value_type=str)
    int_enum_prop = enum_property_factory(value_type=int)
    for prop in props:
        if not isinstance(prop, StringProperty):
            with pytest.raises(ValueError):
                merge_properties(prop, string_enum_prop)
            with pytest.raises(ValueError):
                merge_properties(string_enum_prop, prop)
        if not isinstance(prop, IntProperty):
            with pytest.raises(ValueError):
                merge_properties(prop, int_enum_prop)
            with pytest.raises(ValueError):
                merge_properties(int_enum_prop, prop)
