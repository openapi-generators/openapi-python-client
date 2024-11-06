from typing import Dict, List, Optional, Tuple, Union

import pytest
from attr import evolve

import openapi_python_client.schema as oai
from openapi_python_client.config import Config
from openapi_python_client.parser.errors import ParseError, PropertyError
from openapi_python_client.parser.properties import Schemas, UnionProperty
from openapi_python_client.parser.properties.model_property import ModelProperty
from openapi_python_client.parser.properties.property import Property
from openapi_python_client.parser.properties.protocol import Value
from openapi_python_client.parser.properties.schemas import Class, ReferencePath
from openapi_python_client.schema import DataType, ParameterLocation
from tests.test_parser.test_properties.properties_test_helpers import assert_prop_error


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


def _make_basic_model(
    name: str,
    props: Dict[str, oai.Schema],
    required_prop: Optional[str],
    schemas: Schemas,
    config: Config,
) -> Tuple[ModelProperty, Schemas]:
    model, schemas = ModelProperty.build(
        data=oai.Schema.model_construct(
            required=[required_prop] if required_prop else [],
            title=name,
            properties=props,
        ),
        name=name or "some_generated_name",
        schemas=schemas,
        required=False,
        parent_name="",
        config=config,
        roots={"root"},
        process_properties=True,
    )
    assert isinstance(model, ModelProperty)
    if name:
        model.ref_path = ReferencePath(f"/components/schemas/{name}")
        schemas = evolve(
            schemas, classes_by_reference={**schemas.classes_by_reference, f"/components/schemas/{name}": model}
        )
    return model, schemas


def _assert_valid_discriminator(
    p: Union[Property, PropertyError],
    expected_discriminators: List[Tuple[str, Dict[str, Class]]],
) -> None:
    assert isinstance(p, UnionProperty)
    assert p.discriminators
    assert [(d[0], {key: model.class_info for key, model in d[1].items()}) for d in expected_discriminators] == [
        (d.property_name, {key: model.class_info for key, model in d.value_to_model_map.items()})
        for d in p.discriminators
    ]


def test_discriminator_with_explicit_mapping(config):
    from openapi_python_client.parser.properties import Schemas, property_from_data

    schemas = Schemas()
    props = {"type": oai.Schema.model_construct(type="string")}
    model1, schemas = _make_basic_model("Model1", props, "type", schemas, config)
    model2, schemas = _make_basic_model("Model2", props, "type", schemas, config)
    data = oai.Schema.model_construct(
        oneOf=[
            oai.Reference(ref="#/components/schemas/Model1"),
            oai.Reference(ref="#/components/schemas/Model2"),
        ],
        discriminator=oai.Discriminator.model_construct(
            propertyName="type",
            mapping={
                # mappings can use either a fully-qualified schema reference or just the schema name
                "type1": "#/components/schemas/Model1",
                "type2": "Model2",
            },
        ),
    )

    p, schemas = property_from_data(
        name="MyUnion", required=False, data=data, schemas=schemas, parent_name="parent", config=config
    )
    _assert_valid_discriminator(p, [("type", {"type1": model1, "type2": model2})])


def test_discriminator_with_implicit_mapping(config):
    from openapi_python_client.parser.properties import Schemas, property_from_data

    schemas = Schemas()
    props = {"type": oai.Schema.model_construct(type="string")}
    model1, schemas = _make_basic_model("Model1", props, "type", schemas, config)
    model2, schemas = _make_basic_model("Model2", props, "type", schemas, config)
    data = oai.Schema.model_construct(
        oneOf=[
            oai.Reference(ref="#/components/schemas/Model1"),
            oai.Reference(ref="#/components/schemas/Model2"),
        ],
        discriminator=oai.Discriminator.model_construct(
            propertyName="type",
        ),
    )

    p, schemas = property_from_data(
        name="MyUnion", required=False, data=data, schemas=schemas, parent_name="parent", config=config
    )
    _assert_valid_discriminator(p, [("type", {"Model1": model1, "Model2": model2})])


def test_discriminator_with_partial_explicit_mapping(config):
    from openapi_python_client.parser.properties import Schemas, property_from_data

    schemas = Schemas()
    props = {"type": oai.Schema.model_construct(type="string")}
    model1, schemas = _make_basic_model("Model1", props, "type", schemas, config)
    model2, schemas = _make_basic_model("Model2", props, "type", schemas, config)
    data = oai.Schema.model_construct(
        oneOf=[
            oai.Reference(ref="#/components/schemas/Model1"),
            oai.Reference(ref="#/components/schemas/Model2"),
        ],
        discriminator=oai.Discriminator.model_construct(
            propertyName="type",
            mapping={
                "type1": "#/components/schemas/Model1",
                # no value specified for Model2, so it defaults to just "Model2"
            },
        ),
    )

    p, schemas = property_from_data(
        name="MyUnion", required=False, data=data, schemas=schemas, parent_name="parent", config=config
    )
    _assert_valid_discriminator(p, [("type", {"type1": model1, "Model2": model2})])


def test_discriminators_in_nested_unions_same_property(config):
    from openapi_python_client.parser.properties import Schemas, property_from_data

    schemas = Schemas()
    props = {"type": oai.Schema.model_construct(type="string")}
    model1, schemas = _make_basic_model("Model1", props, "type", schemas, config)
    model2, schemas = _make_basic_model("Model2", props, "type", schemas, config)
    model3, schemas = _make_basic_model("Model3", props, "type", schemas, config)
    model4, schemas = _make_basic_model("Model4", props, "type", schemas, config)
    data = oai.Schema.model_construct(
        oneOf=[
            oai.Schema.model_construct(
                oneOf=[
                    oai.Reference(ref="#/components/schemas/Model1"),
                    oai.Reference(ref="#/components/schemas/Model2"),
                ],
                discriminator=oai.Discriminator.model_construct(propertyName="type"),
            ),
            oai.Schema.model_construct(
                oneOf=[
                    oai.Reference(ref="#/components/schemas/Model3"),
                    oai.Reference(ref="#/components/schemas/Model4"),
                ],
                discriminator=oai.Discriminator.model_construct(propertyName="type"),
            ),
        ],
    )

    p, schemas = property_from_data(
        name="MyUnion", required=False, data=data, schemas=schemas, parent_name="parent", config=config
    )
    _assert_valid_discriminator(
        p,
        [
            ("type", {"Model1": model1, "Model2": model2}),
            ("type", {"Model3": model3, "Model4": model4}),
        ],
    )


def test_discriminators_in_nested_unions_different_property(config):
    from openapi_python_client.parser.properties import Schemas, property_from_data

    schemas = Schemas()
    props1 = {"type": oai.Schema.model_construct(type="string")}
    props2 = {"other": oai.Schema.model_construct(type="string")}
    model1, schemas = _make_basic_model("Model1", props1, "type", schemas, config)
    model2, schemas = _make_basic_model("Model2", props1, "type", schemas, config)
    model3, schemas = _make_basic_model("Model3", props2, "other", schemas, config)
    model4, schemas = _make_basic_model("Model4", props2, "other", schemas, config)
    data = oai.Schema.model_construct(
        oneOf=[
            oai.Schema.model_construct(
                oneOf=[
                    oai.Reference(ref="#/components/schemas/Model1"),
                    oai.Reference(ref="#/components/schemas/Model2"),
                ],
                discriminator=oai.Discriminator.model_construct(propertyName="type"),
            ),
            oai.Schema.model_construct(
                oneOf=[
                    oai.Reference(ref="#/components/schemas/Model3"),
                    oai.Reference(ref="#/components/schemas/Model4"),
                ],
                discriminator=oai.Discriminator.model_construct(propertyName="other"),
            ),
        ],
    )

    p, schemas = property_from_data(
        name="MyUnion", required=False, data=data, schemas=schemas, parent_name="parent", config=config
    )
    _assert_valid_discriminator(
        p,
        [
            ("type", {"Model1": model1, "Model2": model2}),
            ("other", {"Model3": model3, "Model4": model4}),
        ],
    )


def test_build_union_property_invalid_property(config):
    name = "bad_union"
    required = True
    reference = oai.Reference.model_construct(ref="#/components/schema/NotExist")
    data = oai.Schema(anyOf=[reference])

    p, s = UnionProperty.build(
        name=name, required=required, data=data, schemas=Schemas(), parent_name="parent", config=config
    )
    assert_prop_error(p, f"Invalid property in union {name}", data=reference)


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


@pytest.mark.parametrize("bad_ref", ["#/components/schemas/UnknownModel", "http://remote/Model2"])
def test_discriminator_invalid_reference(bad_ref, config):
    from openapi_python_client.parser.properties import Schemas, property_from_data

    schemas = Schemas()
    props = {"type": oai.Schema.model_construct(type="string")}
    model1, schemas = _make_basic_model("Model1", props, "type", schemas, config)
    model2, schemas = _make_basic_model("Model2", props, "type", schemas, config)
    data = oai.Schema.model_construct(
        oneOf=[
            oai.Reference(ref="#/components/schemas/Model1"),
            oai.Reference(ref="#/components/schemas/Model2"),
        ],
        discriminator=oai.Discriminator.model_construct(
            propertyName="type",
            mapping={
                "Model1": "#/components/schemas/Model1",
                "Model2": bad_ref,
            },
        ),
    )

    p, schemas = property_from_data(
        name="MyUnion", required=False, data=data, schemas=schemas, parent_name="parent", config=config
    )
    assert_prop_error(p, "^Invalid reference")


def test_discriminator_mapping_uses_schema_not_in_list(config):
    from openapi_python_client.parser.properties import Schemas, property_from_data

    schemas = Schemas()
    props = {"type": oai.Schema.model_construct(type="string")}
    model1, schemas = _make_basic_model("Model1", props, "type", schemas, config)
    model2, schemas = _make_basic_model("Model2", props, "type", schemas, config)
    model3, schemas = _make_basic_model("Model3", props, "type", schemas, config)
    data = oai.Schema.model_construct(
        oneOf=[
            oai.Reference(ref="#/components/schemas/Model1"),
            oai.Reference(ref="#/components/schemas/Model2"),
        ],
        discriminator=oai.Discriminator.model_construct(
            propertyName="type",
            mapping={
                "Model1": "#/components/schemas/Model1",
                "Model3": "#/components/schemas/Model3",
            },
        ),
    )

    p, schemas = property_from_data(
        name="MyUnion", required=False, data=data, schemas=schemas, parent_name="parent", config=config
    )
    assert_prop_error(p, "not one of the schema variants")


def test_discriminator_invalid_variant_is_not_object(config, string_property_factory):
    from openapi_python_client.parser.properties import Schemas, property_from_data

    schemas = Schemas()
    props = {"type": oai.Schema.model_construct(type="string")}
    model_type, schemas = _make_basic_model("ModelType", props, "type", schemas, config)
    string_type = string_property_factory()
    schemas = evolve(
        schemas,
        classes_by_reference={
            **schemas.classes_by_reference,
            "/components/schemas/StringType": string_type,
        },
    )
    data = oai.Schema.model_construct(
        oneOf=[
            oai.Reference(ref="#/components/schemas/ModelType"),
            oai.Reference(ref="#/components/schemas/StringType"),
        ],
        discriminator=oai.Discriminator.model_construct(
            propertyName="type",
        ),
    )

    p, schemas = property_from_data(
        name="MyUnion", required=False, data=data, schemas=schemas, parent_name="parent", config=config
    )
    assert_prop_error(p, "must be objects")


def test_discriminator_invalid_inline_schema_variant(config, string_property_factory):
    from openapi_python_client.parser.properties import Schemas, property_from_data

    schemas = Schemas()
    schemas = Schemas()
    props = {"type": oai.Schema.model_construct(type="string")}
    model1, schemas = _make_basic_model("Model1", props, "type", schemas, config)
    data = oai.Schema.model_construct(
        oneOf=[
            oai.Reference(ref="#/components/schemas/Model1"),
            oai.Schema.model_construct(
                type="object",
                properties=props,
            ),
        ],
        discriminator=oai.Discriminator.model_construct(
            propertyName="type",
        ),
    )

    p, schemas = property_from_data(
        name="MyUnion", required=False, data=data, schemas=schemas, parent_name="parent", config=config
    )
    assert_prop_error(p, "Inline schema")
