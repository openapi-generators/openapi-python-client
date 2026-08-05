import openapi_python_client.schema as oai
from openapi_python_client.parser.errors import ParseError
from openapi_python_client.parser.properties import (
    ModelProperty,
    Schemas,
    UnionProperty,
    build_schemas,
    property_from_data,
)
from openapi_python_client.schema import DataType, ParameterLocation


def _tagged_union_schemas(tag_schema: dict | None = None) -> dict[str, oai.Schema]:
    """Two models tagged by `tag`, a union over them, and a model holding that union behind a `$ref`.

    Each member gets its own `const` tag unless `tag_schema` replaces it for both of them.
    """
    return {
        name: oai.Schema.model_validate(data)
        for name, data in {
            "A": {"type": "object", "required": ["tag"], "properties": {"tag": tag_schema or {"const": "a"}}},
            "B": {"type": "object", "required": ["tag"], "properties": {"tag": tag_schema or {"const": "b"}}},
            "Tagged": {
                "discriminator": {"propertyName": "tag"},
                "oneOf": [{"$ref": "#/components/schemas/A"}, {"$ref": "#/components/schemas/B"}],
            },
            "Holder": {
                "type": "object",
                "properties": {
                    "nullableTagged": {
                        "anyOf": [{"$ref": "#/components/schemas/Tagged"}, {"type": "null"}],
                    }
                },
            },
        }.items()
    }


def _holder_union(components: dict[str, oai.Schema], config) -> tuple[UnionProperty, Schemas]:
    schemas = build_schemas(components=components, schemas=Schemas(), config=config)
    assert not schemas.errors
    holder = schemas.classes_by_name["Holder"]
    assert isinstance(holder, ModelProperty)
    union = (holder.optional_properties or [])[0]
    assert isinstance(union, UnionProperty)
    return union, schemas


def test_discriminator_is_resolved_from_the_registered_members(config):
    """The union has to consult the members registered in `Schemas`, not its own `inner_properties`.

    Those are copies `property_from_data` made while the schemas they point at were still being processed, so
    they never learn what properties they have -- which is exactly what choosing a discriminator needs to know.
    Only the registered objects get filled in, in place, once processing reaches them.
    """
    union, schemas = _holder_union(_tagged_union_schemas(), config)

    # The discriminator was declared on `Tagged`, which is flattened into this union rather than kept nested.
    assert union.discriminator_property_name == "tag"
    assert union.get_discriminator_field_name() == "tag"

    members = [prop for prop in union.inner_properties if isinstance(prop, ModelProperty)]
    assert [prop.required_properties for prop in members] == [None, None], "copies should stay unprocessed"
    assert union.registered_members["A"] is schemas.classes_by_name["A"]
    assert union.registered_members["B"] is schemas.classes_by_name["B"]


def test_no_discriminator_when_a_member_cannot_carry_a_tag(config):
    """A tag declared as a plain `string` renders as `str`, which pydantic will not dispatch on."""
    union, _ = _holder_union(_tagged_union_schemas({"type": "string"}), config)

    assert union.discriminator_property_name == "tag"
    assert union.get_discriminator_field_name() is None


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
    union_property_factory,
    date_time_property_factory,
    string_property_factory,
    boolean_property_factory,
    date_property_factory,
    int_property_factory,
    float_property_factory,
    config,
):
    nested_schema_variant_A = oai.Schema(type=DataType.STRING, title="A")
    nested_schema_variant_B = oai.Schema(type=DataType.INTEGER, title="B")
    nested_schema_variant_2 = oai.Schema(type=DataType.NUMBER)
    nested_schema_variant_C = oai.Schema(type=DataType.BOOLEAN, title="C")

    name = "union_prop"
    required = True
    data = oai.Schema(
        anyOf=[
            # AnyOf retains the old naming convention
            nested_schema_variant_C,
            oai.Schema(type=DataType.STRING, schema_format="date"),
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
            boolean_property_factory(name=f"{name}_C"),
            date_property_factory(name=f"{name}_type_1"),
            string_property_factory(name=f"{name}_A"),
            int_property_factory(name=f"{name}_B"),
            float_property_factory(name=f"{name}_type_4"),
            date_time_property_factory(name=f"{name}_type_5"),
        ],
    )

    p, s = property_from_data(
        name=name, required=required, data=data, schemas=Schemas(), parent_name="parent", config=config
    )

    assert p == expected
    assert s == Schemas()
