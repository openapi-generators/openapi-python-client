import openapi_python_client.schema as oai
from openapi_python_client.parser.errors import ParseError, PropertyError
from openapi_python_client.parser.properties import Schemas, UnionProperty
from openapi_python_client.schema import DataType, ParameterLocation


def test_property_from_data_union(union_property_factory, date_time_property_factory, string_property_factory, config):
    from openapi_python_client.parser.properties import Schemas, property_from_data

    name = "union_prop"
    required = True
    data = oai.Schema(
        anyOf=[oai.Schema(type=DataType.STRING, default="a")],
        oneOf=[
            oai.Schema(type=DataType.STRING, schema_format="date-time"),
        ],
    )
    expected = union_property_factory(
        name=name,
        required=required,
        inner_properties=[
            string_property_factory(name=f"{name}_type_0", default="'a'"),
            date_time_property_factory(name=f"{name}_type_1"),
        ],
    )

    p, s = property_from_data(
        name=name, required=required, data=data, schemas=Schemas(), parent_name="parent", config=config
    )

    assert p == expected
    assert s == Schemas()


def test_build_union_property_invalid_property(config):
    name = "bad_union"
    required = True
    reference = oai.Reference.model_construct(ref="#/components/schema/NotExist")
    data = oai.Schema(anyOf=[reference])

    p, s = UnionProperty.build(
        name=name, required=required, data=data, schemas=Schemas(), parent_name="parent", config=config
    )
    assert p == PropertyError(detail=f"Invalid property in union {name}", data=reference)


def test_invalid_default(config):
    data = oai.Schema(
        type=[DataType.NUMBER, DataType.INTEGER],
        default="a",
    )

    err, _ = UnionProperty.build(
        data=data, required=True, schemas=Schemas(), parent_name="parent", name="name", config=config
    )

    assert isinstance(err, PropertyError)


def test_invalid_location(config):
    data = oai.Schema(
        type=[DataType.NUMBER, DataType.NULL],
    )

    prop, _ = UnionProperty.build(
        data=data, required=True, schemas=Schemas(), parent_name="parent", name="name", config=config
    )

    err = prop.validate_location(ParameterLocation.PATH)
    assert isinstance(err, ParseError)


def test_not_required_in_path(config):
    data = oai.Schema(
        oneOf=[oai.Schema(type=DataType.NUMBER), oai.Schema(type=DataType.INTEGER)],
    )

    prop, _ = UnionProperty.build(
        data=data, required=False, schemas=Schemas(), parent_name="parent", name="name", config=config
    )

    err = prop.validate_location(ParameterLocation.PATH)
    assert isinstance(err, ParseError)


def test_union_oneOf_descriptive_type_name(
    union_property_factory, date_time_property_factory, string_property_factory, config
):
    from openapi_python_client.parser.properties import Schemas, property_from_data

    nested_schema_variant_A = oai.Schema(type=DataType.STRING, title="A")
    nested_schema_variant_B = oai.Schema(type=DataType.STRING, title="B")
    nested_schema_variant_2 = oai.Schema(type=DataType.STRING)
    nested_schema_variant_C = oai.Schema(type=DataType.STRING, title="C")
    nested_schema_variant_4 = oai.Schema(type=DataType.STRING)

    name = "union_prop"
    required = True
    data = oai.Schema(
        anyOf=[
            # AnyOf retains the old naming convention
            nested_schema_variant_C,
            nested_schema_variant_4,
        ],
        oneOf=[
            # OneOf fields that define their own titles will have those titles as their Type names
            nested_schema_variant_A,
            nested_schema_variant_B,
            nested_schema_variant_2,
            oai.Schema(type=DataType.STRING, schema_format="date-time"),
        ],
    )
    expected = union_property_factory(
        name=name,
        required=required,
        inner_properties=[
            string_property_factory(name=f"{name}_type_0"),
            string_property_factory(name=f"{name}_type_1"),
            string_property_factory(name=f"{name}_type_A"),
            string_property_factory(name=f"{name}_type_B"),
            string_property_factory(name=f"{name}_type_4"),
            date_time_property_factory(name=f"{name}_type_5"),
        ],
    )

    p, s = property_from_data(
        name=name, required=required, data=data, schemas=Schemas(), parent_name="parent", config=config
    )

    assert p == expected
    assert s == Schemas()
