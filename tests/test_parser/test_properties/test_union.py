import openapi_python_client.schema as oai
from openapi_python_client import Config
from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties import Schemas, UnionProperty
from openapi_python_client.schema import DataType


def test_property_from_data_union(union_property_factory, date_time_property_factory, string_property_factory):
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
        name=name, required=required, data=data, schemas=Schemas(), parent_name="parent", config=Config()
    )

    assert p == expected
    assert s == Schemas()


def test_build_union_property_invalid_property():
    name = "bad_union"
    required = True
    reference = oai.Reference.model_construct(ref="#/components/schema/NotExist")
    data = oai.Schema(anyOf=[reference])

    p, s = UnionProperty.build(
        name=name, required=required, data=data, schemas=Schemas(), parent_name="parent", config=Config()
    )
    assert p == PropertyError(detail=f"Invalid property in union {name}", data=reference)


def test_invalid_default():
    data = oai.Schema(
        type=[DataType.NUMBER, DataType.INTEGER],
        default="a",
    )

    err, _ = UnionProperty.build(
        data=data,
        required=True,
        schemas=Schemas(),
        parent_name="parent",
        name="name",
        config=Config(),
    )

    assert isinstance(err, PropertyError)
