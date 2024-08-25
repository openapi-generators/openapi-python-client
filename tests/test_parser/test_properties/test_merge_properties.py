from itertools import permutations

from attr import evolve

from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties.float import FloatProperty
from openapi_python_client.parser.properties.int import IntProperty
from openapi_python_client.parser.properties.merge_properties import merge_properties
from openapi_python_client.parser.properties.schemas import Class
from openapi_python_client.parser.properties.string import StringProperty

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
        boolean_property_factory(default="True"),
        int_property_factory(default="1"),
        float_property_factory(default="1.5"),
        string_property_factory(default=StringProperty.convert_value("x")),
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

    for prop1, prop2 in permutations(props, 2):
        if {prop1.__class__, prop2.__class__} == {IntProperty, FloatProperty}:
            continue  # the int+float case is covered in another test
        error = merge_properties(prop1, prop2)
        assert isinstance(error, PropertyError), f"Expected {type(prop1)} and {type(prop2)} to be incompatible"


def test_merge_int_with_float(int_property_factory, float_property_factory):
    int_prop = int_property_factory(description="desc1")
    float_prop = float_property_factory(default="2", description="desc2")

    assert merge_properties(int_prop, float_prop) == (
        evolve(int_prop, default=float_prop.default, description=float_prop.description)
    )
    assert merge_properties(float_prop, int_prop) == (evolve(int_prop, default=float_prop.default))

    float_prop_with_non_int_default = evolve(float_prop, default="2.5")
    error = merge_properties(int_prop, float_prop_with_non_int_default)
    assert isinstance(error, PropertyError), "Expected invalid default to error"
    assert error.detail == "Invalid int value: 2.5"


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
        boolean_property_factory(default="True", description=original_desc),
        int_property_factory(default="1", description=original_desc),
        float_property_factory(default="1.5", description=original_desc),
        string_property_factory(default=StringProperty.convert_value("x"), description=original_desc),
        model_property_factory(description=original_desc),
    ]
    any_prop = any_property_factory()
    for prop in props:
        assert merge_properties(any_prop, prop) == prop
        assert merge_properties(prop, any_prop) == prop


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
    string_prop = string_property_factory(default="A", description="desc1", example="example1")
    enum_prop = enum_property_factory(
        default="test.B",
        description="desc2",
        example="example2",
        values=values,
        value_type=str,
    )

    assert merge_properties(string_prop, enum_prop) == evolve(enum_prop, required=True)
    assert merge_properties(enum_prop, string_prop) == evolve(
        enum_prop,
        required=True,
        default="test.A",
        description=string_prop.description,
        example=string_prop.example,
    )


def test_merge_int_with_int_enum(int_property_factory, enum_property_factory):
    values = {"VALUE_1": 1, "VALUE_2": 2}
    int_prop = int_property_factory(default=1, description="desc1", example="example1")
    enum_prop = enum_property_factory(
        default="test.VALUE_1",
        description="desc2",
        example="example2",
        values=values,
        value_type=int,
    )

    assert merge_properties(int_prop, enum_prop) == evolve(enum_prop, required=True)
    assert merge_properties(enum_prop, int_prop) == evolve(
        enum_prop, required=True, description=int_prop.description, example=int_prop.example
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
            assert isinstance(merge_properties(prop, string_enum_prop), PropertyError)
            assert isinstance(merge_properties(string_enum_prop, prop), PropertyError)
        if not isinstance(prop, IntProperty):
            assert isinstance(merge_properties(prop, int_enum_prop), PropertyError)
            assert isinstance(merge_properties(int_enum_prop, prop), PropertyError)
