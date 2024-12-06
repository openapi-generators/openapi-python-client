import openapi_python_client.schema as oai
from openapi_python_client.parser.errors import ParseError, PropertyError
from openapi_python_client.parser.properties import Schemas, UnionProperty
from openapi_python_client.parser.properties.enum_property import EnumProperty
from openapi_python_client.parser.properties.model_property import ModelProperty
from openapi_python_client.parser.properties.protocol import Value
from openapi_python_client.parser.properties.schemas import Class
from openapi_python_client.schema import DataType, ParameterLocation
from openapi_python_client.utils import ClassName


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


def test_name_is_preserved_if_union_is_nullable_model(config):
    from openapi_python_client.parser.properties import Schemas, property_from_data

    parent_name = "parent"
    name = "prop_1"
    required = True
    data = oai.Schema(
        oneOf=[
            oai.Schema(type=DataType.OBJECT),
            oai.Schema(type=DataType.NULL),
        ],
    )
    expected_model_class = Class(name=ClassName("ParentProp1", ""), module_name="parent_prop_1")

    p, s = property_from_data(
        name=name, required=required, data=data, schemas=Schemas(), parent_name=parent_name, config=config
    )

    assert isinstance(p, UnionProperty)
    assert len(p.inner_properties) == 2
    prop1 = p.inner_properties[0]
    assert isinstance(prop1, ModelProperty)
    assert prop1.name == name
    assert prop1.class_info == expected_model_class

    assert s == Schemas(classes_by_name={expected_model_class.name: prop1}, models_to_process=[prop1])


def test_name_is_preserved_if_union_is_nullable_enum(config):
    from openapi_python_client.parser.properties import Schemas, property_from_data

    parent_name = "parent"
    name = "prop_1"
    required = True
    data = oai.Schema(
        oneOf=[
            oai.Schema(type=DataType.INTEGER, enum=[10, 20]),
            oai.Schema(type=DataType.NULL),
        ],
    )
    expected_enum_class = Class(name=ClassName("ParentProp1", ""), module_name="parent_prop_1")

    p, s = property_from_data(
        name=name, required=required, data=data, schemas=Schemas(), parent_name=parent_name, config=config
    )

    assert isinstance(p, UnionProperty)
    assert len(p.inner_properties) == 2
    prop1 = p.inner_properties[0]
    assert isinstance(prop1, EnumProperty)
    assert prop1.name == name
    assert prop1.class_info == expected_enum_class

    assert s == Schemas(classes_by_name={expected_enum_class.name: prop1})


def test_name_is_preserved_if_union_has_multiple_models_or_enums(config):
    from openapi_python_client.parser.properties import Schemas, property_from_data

    parent_name = "parent"
    name = "prop_1"
    required = True
    data = oai.Schema(
        oneOf=[
            oai.Schema(type=DataType.OBJECT),
            oai.Schema(type=DataType.INTEGER, enum=[10, 20]),
        ],
    )
    expected_model_class = Class(name=ClassName("ParentProp1Type0", ""), module_name="parent_prop_1_type_0")
    expected_enum_class = Class(name=ClassName("ParentProp1Type1", ""), module_name="parent_prop_1_type_1")

    p, s = property_from_data(
        name=name, required=required, data=data, schemas=Schemas(), parent_name=parent_name, config=config
    )

    assert isinstance(p, UnionProperty)
    assert len(p.inner_properties) == 2
    [prop1, prop2] = p.inner_properties
    assert isinstance(prop1, ModelProperty)
    assert prop1.name == f"{name}_type_0"
    assert prop1.class_info == expected_model_class
    assert isinstance(prop2, EnumProperty)
    assert prop2.name == f"{name}_type_1"
    assert prop2.class_info == expected_enum_class

    assert s == Schemas(
        classes_by_name={expected_model_class.name: prop1, expected_enum_class.name: prop2},
        models_to_process=[prop1],
    )


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
