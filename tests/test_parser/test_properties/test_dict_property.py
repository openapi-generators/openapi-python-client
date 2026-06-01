import openapi_python_client.schema as oai
from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties import DictProperty, ModelProperty, Schemas, property_from_data
from openapi_python_client.parser.properties.float import FloatProperty


class TestPropertyFromDataDict:
    def test_additional_properties_number_becomes_dict(self, config):
        data = oai.Schema.model_construct(
            type=oai.DataType.OBJECT,
            additionalProperties=oai.Schema.model_construct(type=oai.DataType.NUMBER),
        )

        prop, _ = property_from_data(
            name="scores_by_id",
            required=True,
            data=data,
            schemas=Schemas(),
            parent_name="SearchCodesResponse",
            config=config,
        )

        assert isinstance(prop, DictProperty)
        assert prop.get_type_string() == "dict[str, float]"
        assert isinstance(prop.inner_property, FloatProperty)

    def test_additional_properties_ref_becomes_dict(self, config, model_property_factory):
        existing = model_property_factory(name="AnEnum")
        ref_path = "/components/schemas/AnEnum"
        schemas = Schemas(classes_by_reference={ref_path: existing})

        data = oai.Schema.model_construct(
            type=oai.DataType.OBJECT,
            additionalProperties=oai.Reference.model_construct(ref=f"#{ref_path}"),
        )

        prop, _ = property_from_data(
            name="enum_map",
            required=True,
            data=data,
            schemas=schemas,
            parent_name="Parent",
            config=config,
        )

        assert isinstance(prop, DictProperty)
        assert prop.get_type_string() == "dict[str, MyClass]"

    def test_additional_properties_inside_union(self, config):
        data = oai.Schema.model_construct(
            anyOf=[
                oai.Schema.model_construct(
                    type=oai.DataType.OBJECT,
                    additionalProperties=oai.Schema.model_construct(type=oai.DataType.NUMBER),
                ),
                oai.Schema.model_construct(type=oai.DataType.NULL),
            ]
        )

        prop, _ = property_from_data(
            name="scores_by_id",
            required=False,
            data=data,
            schemas=Schemas(),
            parent_name="SearchCodesResponse",
            config=config,
        )

        assert not isinstance(prop, PropertyError)
        type_string = prop.get_type_string(no_optional=True)
        assert "dict[str, float]" in type_string
        assert "None" in type_string
        assert "ScoresById" not in type_string
        assert "Type0" not in type_string

    def test_additional_properties_with_properties_still_becomes_model(self, config):
        data = oai.Schema.model_construct(
            type=oai.DataType.OBJECT,
            properties={"name": oai.Schema.model_construct(type=oai.DataType.STRING)},
            additionalProperties=oai.Schema.model_construct(type=oai.DataType.NUMBER),
        )

        prop, _ = property_from_data(
            name="mixed",
            required=True,
            data=data,
            schemas=Schemas(),
            parent_name="Parent",
            config=config,
        )

        assert isinstance(prop, ModelProperty)

    def test_additional_properties_true_still_becomes_model(self, config):
        data = oai.Schema.model_construct(
            type=oai.DataType.OBJECT,
            additionalProperties=True,
        )

        prop, _ = property_from_data(
            name="any_map",
            required=True,
            data=data,
            schemas=Schemas(),
            parent_name="Parent",
            config=config,
        )

        assert isinstance(prop, ModelProperty)

    def test_top_level_schema_stays_model(self, config):
        data = oai.Schema.model_construct(
            type=oai.DataType.OBJECT,
            additionalProperties=oai.Schema.model_construct(type=oai.DataType.NUMBER),
        )

        # Top-level schema is called from schemas.update_schemas_with_data with parent_name=""
        prop, _ = property_from_data(
            name="ScoresByIdTopLevel",
            required=True,
            data=data,
            schemas=Schemas(),
            parent_name="",
            config=config,
            process_properties=False,
        )

        assert isinstance(prop, ModelProperty)


class TestDictPropertyAPI:
    def test_get_type_string_required(self, config):
        data = oai.Schema.model_construct(
            type=oai.DataType.OBJECT,
            additionalProperties=oai.Schema.model_construct(type=oai.DataType.NUMBER),
        )
        prop, _ = DictProperty.build(
            data=data,
            name="m",
            required=True,
            schemas=Schemas(),
            parent_name="Parent",
            config=config,
            process_properties=True,
            roots=set(),
        )
        assert prop.get_type_string() == "dict[str, float]"
        assert prop.get_type_string(no_optional=True) == "dict[str, float]"
        assert prop.get_base_json_type_string() == "dict[str, float]"
        assert prop.get_instance_type_string() == "dict"

    def test_get_type_string_optional(self, config):
        data = oai.Schema.model_construct(
            type=oai.DataType.OBJECT,
            additionalProperties=oai.Schema.model_construct(type=oai.DataType.STRING),
        )
        prop, _ = DictProperty.build(
            data=data,
            name="m",
            required=False,
            schemas=Schemas(),
            parent_name="Parent",
            config=config,
            process_properties=True,
            roots=set(),
        )
        assert prop.get_type_string() == "dict[str, str] | Unset"
        assert prop.get_type_string(no_optional=True) == "dict[str, str]"

    def test_build_without_typed_additional_errors(self, config):
        data = oai.Schema.model_construct(type=oai.DataType.OBJECT, additionalProperties=True)
        result, _ = DictProperty.build(
            data=data,
            name="m",
            required=True,
            schemas=Schemas(),
            parent_name="Parent",
            config=config,
            process_properties=True,
            roots=set(),
        )
        assert isinstance(result, PropertyError)

    def test_build_with_bad_inner_schema(self, config):
        data = oai.Schema.model_construct(
            type=oai.DataType.OBJECT,
            additionalProperties=oai.Reference.model_construct(ref="#/components/schemas/Missing"),
        )
        result, _ = DictProperty.build(
            data=data,
            name="m",
            required=True,
            schemas=Schemas(),
            parent_name="Parent",
            config=config,
            process_properties=True,
            roots=set(),
        )
        assert isinstance(result, PropertyError)
