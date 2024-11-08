import openapi_python_client.schema as oai
from openapi_python_client.parser.errors import ParseError
from openapi_python_client.parser.properties import Schemas, UnionProperty
from openapi_python_client.parser.properties.protocol import Value
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
            string_property_factory(name=f"{name}_type_0", default=Value("'a'", "a")),
            date_time_property_factory(name=f"{name}_type_1"),
        ],
    )

    p, s = property_from_data(
        name=name, required=required, data=data, schemas=Schemas(), parent_name="parent", config=config
    )

    assert p == expected
    assert s == Schemas()


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
