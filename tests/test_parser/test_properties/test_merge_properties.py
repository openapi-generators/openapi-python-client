from itertools import permutations

import pytest
from attr import evolve

from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties.float import FloatProperty
from openapi_python_client.parser.properties.int import IntProperty
from openapi_python_client.parser.properties.merge_properties import merge_properties
from openapi_python_client.parser.properties.model_property import ModelDetails, ModelProperty
from openapi_python_client.parser.properties.protocol import Value
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
    config,
):
    basic_props = [
        boolean_property_factory(default=Value(python_code="True", raw_value="True")),
        int_property_factory(default=Value("1", 1)),
        float_property_factory(default=Value("1.5", 1.5)),
        string_property_factory(default=StringProperty.convert_value("x")),
        list_property_factory(),
        model_property_factory(required_properties=[], optional_properties=[]),
    ]
    for basic_prop in basic_props:
        with_required = evolve(basic_prop, required=True)
        assert merge_properties(basic_prop, with_required, "", config) == with_required
        assert merge_properties(with_required, basic_prop, "", config) == with_required
        without_default = evolve(basic_prop, default=None)
        assert merge_properties(basic_prop, without_default, "", config) == basic_prop
        assert merge_properties(without_default, basic_prop, "", config) == basic_prop
        with_desc1 = evolve(basic_prop, description="desc1")
        with_desc2 = evolve(basic_prop, description="desc2")
        assert merge_properties(basic_prop, with_desc1, "", config) == with_desc1
        assert merge_properties(with_desc1, basic_prop, "", config) == with_desc1
        assert merge_properties(with_desc1, with_desc2, "", config) == with_desc2


def test_incompatible_types(
    boolean_property_factory,
    int_property_factory,
    float_property_factory,
    string_property_factory,
    list_property_factory,
    model_property_factory,
    config,
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
        error = merge_properties(prop1, prop2, "", config)
        assert isinstance(error, PropertyError), f"Expected {type(prop1)} and {type(prop2)} to be incompatible"


def test_merge_int_with_float(int_property_factory, float_property_factory, config):
    int_prop = int_property_factory(description="desc1")
    float_prop = float_property_factory(default=Value("2", 2), description="desc2")

    assert merge_properties(int_prop, float_prop, "", config) == (
        evolve(int_prop, default=Value("2", 2), description=float_prop.description)
    )
    assert merge_properties(float_prop, int_prop, "", config) == evolve(int_prop, default=Value("2", 2))

    float_prop_with_non_int_default = evolve(float_prop, default=Value("2.5", 2.5))
    error = merge_properties(int_prop, float_prop_with_non_int_default, "", config)
    assert isinstance(error, PropertyError), "Expected invalid default to error"
    assert error.detail == "Invalid int value: 2.5"


def test_merge_with_any(
    any_property_factory,
    boolean_property_factory,
    int_property_factory,
    float_property_factory,
    string_property_factory,
    model_property_factory,
    config,
):
    original_desc = "description"
    props = [
        boolean_property_factory(default=Value("True", "True"), description=original_desc),
        int_property_factory(default=Value("1", "1"), description=original_desc),
        float_property_factory(default=Value("1.5", "1.5"), description=original_desc),
        string_property_factory(default=StringProperty.convert_value("x"), description=original_desc),
        model_property_factory(description=original_desc),
    ]
    any_prop = any_property_factory()
    for prop in props:
        assert merge_properties(any_prop, prop, "", config) == prop
        assert merge_properties(prop, any_prop, "", config) == prop


@pytest.mark.parametrize("literal_enums", (False, True))
def test_merge_enums(literal_enums, enum_property_factory, literal_enum_property_factory, config):
    if literal_enums:
        enum_with_fewer_values = literal_enum_property_factory(
            description="desc1",
            values={"A", "B"},
            value_type=str,
        )
        enum_with_more_values = literal_enum_property_factory(
            example="example2",
            values={"A", "B", "C"},
            value_type=str,
        )
    else:
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

    assert merge_properties(enum_with_fewer_values, enum_with_more_values, "", config) == evolve(
        enum_with_more_values,
        values=enum_with_fewer_values.values,
        class_info=enum_with_fewer_values.class_info,
        description=enum_with_fewer_values.description,
    )
    assert merge_properties(enum_with_more_values, enum_with_fewer_values, "", config) == evolve(
        enum_with_fewer_values,
        example=enum_with_more_values.example,
    )


@pytest.mark.parametrize("literal_enums", (False, True))
def test_merge_string_with_string_enum(
    literal_enums, string_property_factory, enum_property_factory, literal_enum_property_factory, config
):
    string_prop = string_property_factory(default=Value("A", "A"), description="desc1", example="example1")
    enum_prop = (
        literal_enum_property_factory(
            default=Value("'B'", "B"),
            description="desc2",
            example="example2",
            values={"A", "B"},
            value_type=str,
        )
        if literal_enums
        else enum_property_factory(
            default=Value("test.B", "B"),
            description="desc2",
            example="example2",
            values={"A": "A", "B": "B"},
            value_type=str,
        )
    )

    assert merge_properties(string_prop, enum_prop, "", config) == evolve(enum_prop, required=True)
    assert merge_properties(enum_prop, string_prop, "", config) == evolve(
        enum_prop,
        required=True,
        default=Value("'A'" if literal_enums else "test.A", "A"),
        description=string_prop.description,
        example=string_prop.example,
    )


@pytest.mark.parametrize("literal_enums", (False, True))
def test_merge_int_with_int_enum(
    literal_enums, int_property_factory, enum_property_factory, literal_enum_property_factory, config
):
    int_prop = int_property_factory(default=Value("1", 1), description="desc1", example="example1")
    enum_prop = (
        literal_enum_property_factory(
            default=Value("1", 1),
            description="desc2",
            example="example2",
            values={1, 2},
            value_type=int,
        )
        if literal_enums
        else enum_property_factory(
            default=Value("test.VALUE_1", 1),
            description="desc2",
            example="example2",
            values={"VALUE_1": 1, "VALUE_2": 2},
            value_type=int,
        )
    )

    assert merge_properties(int_prop, enum_prop, "", config) == evolve(enum_prop, required=True)
    assert merge_properties(enum_prop, int_prop, "", config) == evolve(
        enum_prop, required=True, description=int_prop.description, example=int_prop.example
    )


@pytest.mark.parametrize("literal_enums", (False, True))
def test_merge_with_incompatible_enum(
    literal_enums,
    boolean_property_factory,
    int_property_factory,
    float_property_factory,
    string_property_factory,
    enum_property_factory,
    literal_enum_property_factory,
    model_property_factory,
    config,
):
    props = [
        boolean_property_factory(),
        int_property_factory(),
        float_property_factory(),
        string_property_factory(),
        model_property_factory(),
        enum_property_factory(values={"INCOMPATIBLE": "INCOMPATIBLE"}),
        literal_enum_property_factory(values={"INCOMPATIBLE"}),
    ]
    string_enum_prop = (
        literal_enum_property_factory(value_type=str, values={"A"})
        if literal_enums
        else enum_property_factory(value_type=str, values={"A": "A"})
    )
    int_enum_prop = (
        literal_enum_property_factory(value_type=int, values={1})
        if literal_enums
        else enum_property_factory(value_type=int, values={"VALUE_1": 1})
    )
    for prop in props:
        if not isinstance(prop, StringProperty):
            assert isinstance(merge_properties(prop, string_enum_prop, "", config), PropertyError)
            assert isinstance(merge_properties(string_enum_prop, prop, "", config), PropertyError)
        if not isinstance(prop, IntProperty):
            assert isinstance(merge_properties(prop, int_enum_prop, "", config), PropertyError)
            assert isinstance(merge_properties(int_enum_prop, prop, "", config), PropertyError)


def test_merge_string_with_formatted_string(
    date_property_factory,
    date_time_property_factory,
    file_property_factory,
    string_property_factory,
    config,
):
    string_prop = string_property_factory(description="a plain string")
    string_prop_with_invalid_default = string_property_factory(
        default=StringProperty.convert_value("plain string value")
    )
    formatted_props = [
        date_property_factory(description="a date"),
        date_time_property_factory(description="a datetime"),
        file_property_factory(description="a file"),
    ]
    for formatted_prop in formatted_props:
        merged1 = merge_properties(string_prop, formatted_prop, "", config)
        assert isinstance(merged1, formatted_prop.__class__)
        assert merged1.description == formatted_prop.description

        merged2 = merge_properties(formatted_prop, string_prop, "", config)
        assert isinstance(merged2, formatted_prop.__class__)
        assert merged2.description == string_prop.description

        assert isinstance(merge_properties(string_prop_with_invalid_default, formatted_prop, "", config), PropertyError)
        assert isinstance(merge_properties(formatted_prop, string_prop_with_invalid_default, "", config), PropertyError)


def test_merge_lists(int_property_factory, list_property_factory, string_property_factory, config):
    string_prop_1 = string_property_factory(description="desc1")
    string_prop_2 = string_property_factory(example="desc2")
    int_prop = int_property_factory()
    list_prop_1 = list_property_factory(inner_property=string_prop_1)
    list_prop_2 = list_property_factory(inner_property=string_prop_2)
    list_prop_3 = list_property_factory(inner_property=int_prop)

    assert merge_properties(list_prop_1, list_prop_2, "", config) == evolve(
        list_prop_1, inner_property=merge_properties(string_prop_1, string_prop_2, "", config)
    )

    assert isinstance(merge_properties(list_prop_1, list_prop_3, "", config), PropertyError)


def test_merge_related_models(model_property_factory, string_property_factory, config):
    base_model = model_property_factory(
        name="BaseModel",
        details=ModelDetails(
            required_properties=[
                string_property_factory(name="req_1", description="base description"),
            ],
            optional_properties=[
                string_property_factory(name="opt_1"),
            ],
        ),
        description="desc_1",
        example="example_1",
        class_info=Class.from_string(string="BaseModel", config=config),
    )
    extension_model = model_property_factory(
        name="ExtensionModel",
        details=ModelDetails(
            required_properties=[
                string_property_factory(name="req_1", description="extended description"),
                string_property_factory(name="req_2"),
            ],
            optional_properties=[
                string_property_factory(name="opt_1"),
                string_property_factory(name="opt_2"),
            ],
        ),
        description="desc_2",
        class_info=Class.from_string(string="DerivedModel", config=config),
    )

    assert merge_properties(base_model, extension_model, "", config) == evolve(
        extension_model, example=base_model.example
    )
    assert merge_properties(extension_model, base_model, "", config) == evolve(
        extension_model, description=base_model.description, example=base_model.example
    )


def test_merge_unrelated_models(model_property_factory, string_property_factory, config):
    model_1 = model_property_factory(
        name="propName",
        details=ModelDetails(
            required_properties=[
                string_property_factory(name="req_1", required=True),
            ],
            optional_properties=[
                string_property_factory(name="opt_1", required=False),
            ],
        ),
        description="desc_1",
        example="example_1",
        class_info=Class.from_string(string="Model1", config=config),
    )
    model_2 = model_property_factory(
        name="propName",
        details=ModelDetails(
            required_properties=[
                string_property_factory(name="req_1", required=True),
                string_property_factory(name="req_2", required=True),
            ],
            optional_properties=[
                string_property_factory(name="opt_2", required=False),
            ],
        ),
        description="desc_2",
        class_info=Class.from_string(string="Model2", config=config),
    )

    result = merge_properties(model_1, model_2, "ParentSchema", config)

    assert isinstance(result, ModelProperty)
    assert [p.name for p in result.required_properties] == ["req_1", "req_2"]
    assert [p.name for p in result.optional_properties] == ["opt_1", "opt_2"]
    assert result.class_info.name == "ParentSchemaPropName"
    assert result.description == model_2.description


def test_merge_models_with_incompatible_property(
    model_property_factory, string_property_factory, int_property_factory, config
):
    model_1 = model_property_factory(
        name="propName",
        details=ModelDetails(
            required_properties=[
                string_property_factory(name="prop1", required=True),
            ],
            optional_properties=[],
        ),
        class_info=Class.from_string(string="Model1", config=config),
    )
    model_2 = model_property_factory(
        name="propName",
        details=ModelDetails(
            required_properties=[
                int_property_factory(name="prop1", required=True),
            ],
            optional_properties=[],
        ),
        class_info=Class.from_string(string="Model2", config=config),
    )

    result = merge_properties(model_1, model_2, "ParentSchema", config)

    assert isinstance(result, PropertyError)
    assert result.detail == "str can't be merged with int"


def test_merge_models_not_yet_processed(model_property_factory, string_property_factory, int_property_factory, config):
    model_1 = model_property_factory(
        name="propName",
        details=ModelDetails(required_properties=None, optional_properties=None),
        class_info=Class.from_string(string="Model1", config=config),
    )
    model_2 = model_property_factory(
        name="propName",
        details=ModelDetails(required_properties=None, optional_properties=None),
        class_info=Class.from_string(string="Model2", config=config),
    )

    result = merge_properties(model_1, model_2, "ParentSchema", config)

    assert isinstance(result, PropertyError)
    assert "not processed" in result.detail
