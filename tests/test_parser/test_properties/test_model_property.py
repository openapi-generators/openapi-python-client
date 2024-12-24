from typing import Optional

import pytest
from attr import evolve

import openapi_python_client.schema as oai
from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties import Schemas, StringProperty
from openapi_python_client.parser.properties.model_property import ANY_ADDITIONAL_PROPERTY, _process_properties

MODULE_NAME = "openapi_python_client.parser.properties.model_property"


class TestModelProperty:
    @pytest.mark.parametrize(
        "no_optional,required,json,quoted,expected",
        [
            (False, False, False, False, "Union[Unset, MyClass]"),
            (False, True, False, False, "MyClass"),
            (True, False, False, False, "MyClass"),
            (True, True, False, False, "MyClass"),
            (False, True, True, False, "dict[str, Any]"),
            (False, False, False, True, "Union[Unset, 'MyClass']"),
            (False, True, False, True, "'MyClass'"),
            (True, False, False, True, "'MyClass'"),
            (True, True, False, True, "'MyClass'"),
            (False, True, True, True, "dict[str, Any]"),
        ],
    )
    def test_get_type_string(self, no_optional, required, json, expected, model_property_factory, quoted):
        prop = model_property_factory(
            required=required,
        )

        assert prop.get_type_string(no_optional=no_optional, json=json, quoted=quoted) == expected

    def test_get_imports(self, model_property_factory):
        prop = model_property_factory(required=False)

        assert prop.get_imports(prefix="..") == {
            "from typing import Union",
            "from ..types import UNSET, Unset",
            "from typing import cast",
        }

    def test_get_lazy_imports(self, model_property_factory):
        prop = model_property_factory(required=False)

        assert prop.get_lazy_imports(prefix="..") == {
            "from ..models.my_module import MyClass",
        }

    def test_is_base_type(self, model_property_factory):
        assert model_property_factory().is_base_type is False

    @pytest.mark.parametrize(
        "quoted,expected",
        [
            (False, "MyClass"),
            (True, '"MyClass"'),
        ],
    )
    def test_get_base_type_string(self, quoted, expected, model_property_factory):
        m = model_property_factory()
        assert m.get_base_type_string(quoted=quoted) == expected


class TestBuild:
    @pytest.mark.parametrize(
        "additional_properties_schema, expected_additional_properties",
        [
            (True, ANY_ADDITIONAL_PROPERTY),
            (oai.Schema.model_construct(), ANY_ADDITIONAL_PROPERTY),
            (None, ANY_ADDITIONAL_PROPERTY),
            (False, None),
            (
                oai.Schema.model_construct(type="string"),
                StringProperty(
                    name="AdditionalProperty",
                    required=True,
                    default=None,
                    python_name="additional_property",
                    description=None,
                    example=None,
                ),
            ),
        ],
    )
    def test_additional_schemas(self, additional_properties_schema, expected_additional_properties, config):
        from openapi_python_client.parser.properties import ModelProperty, Schemas

        data = oai.Schema.model_construct(
            additionalProperties=additional_properties_schema,
        )

        model, _ = ModelProperty.build(
            data=data,
            name="prop",
            schemas=Schemas(),
            required=True,
            parent_name="parent",
            config=config,
            roots={"root"},
            process_properties=True,
        )

        assert model.additional_properties == expected_additional_properties

    def test_happy_path(self, model_property_factory, string_property_factory, date_time_property_factory, config):
        from openapi_python_client.parser.properties import Class, ModelProperty, Schemas

        name = "prop"
        required = True

        data = oai.Schema.model_construct(
            required=["req"],
            title="MyModel",
            properties={
                "req": oai.Schema.model_construct(type="string"),
                "opt": oai.Schema(type="string", format="date-time"),
            },
            description="A class called MyModel",
        )
        schemas = Schemas(classes_by_reference={"OtherModel": None}, classes_by_name={"OtherModel": None})
        class_info = Class(name="ParentMyModel", module_name="parent_my_model")
        roots = {"root"}

        model, new_schemas = ModelProperty.build(
            data=data,
            name=name,
            schemas=schemas,
            required=required,
            parent_name="parent",
            config=config,
            roots=roots,
            process_properties=True,
        )

        assert new_schemas != schemas
        assert new_schemas.classes_by_name == {
            "OtherModel": None,
            "ParentMyModel": model,
        }
        assert new_schemas.classes_by_reference == {
            "OtherModel": None,
        }
        assert new_schemas.dependencies == {"root": {class_info.name}}
        assert model == model_property_factory(
            name=name,
            required=required,
            roots={*roots, class_info.name},
            data=data,
            class_info=class_info,
            required_properties=[string_property_factory(name="req", required=True)],
            optional_properties=[date_time_property_factory(name="opt", required=False)],
            description=data.description,
            relative_imports={
                "from dateutil.parser import isoparse",
                "from typing import cast",
                "import datetime",
                "from ..types import UNSET, Unset",
                "from typing import Union",
            },
            lazy_imports=set(),
            additional_properties=ANY_ADDITIONAL_PROPERTY,
        )

    def test_model_name_conflict(self, config):
        from openapi_python_client.parser.properties import ModelProperty

        data = oai.Schema.model_construct()
        schemas = Schemas(classes_by_name={"OtherModel": None})

        err, new_schemas = ModelProperty.build(
            data=data,
            name="OtherModel",
            schemas=schemas,
            required=True,
            parent_name=None,
            config=config,
            roots={"root"},
            process_properties=True,
        )

        assert new_schemas == schemas
        assert err == PropertyError(detail='Attempted to generate duplicate models with name "OtherModel"', data=data)

    @pytest.mark.parametrize(
        "name, title, parent_name, use_title_prefixing, expected",
        ids=(
            "basic name only",
            "title override",
            "name with parent",
            "name with parent and title prefixing disabled",
            "title with parent",
            "title with parent and title prefixing disabled",
        ),
        argvalues=(
            ("prop", None, None, True, "Prop"),
            ("prop", "MyModel", None, True, "MyModel"),
            ("prop", None, "parent", True, "ParentProp"),
            ("prop", None, "parent", False, "ParentProp"),
            ("prop", "MyModel", "parent", True, "ParentMyModel"),
            ("prop", "MyModel", "parent", False, "MyModel"),
        ),
    )
    def test_model_naming(
        self,
        name: str,
        title: Optional[str],
        parent_name: Optional[str],
        use_title_prefixing: bool,
        expected: str,
        config,
    ):
        from openapi_python_client.parser.properties import ModelProperty

        data = oai.Schema(
            title=title,
            properties={},
        )
        config = evolve(config, use_path_prefixes_for_title_model_names=use_title_prefixing)
        result = ModelProperty.build(
            data=data,
            name=name,
            schemas=Schemas(),
            required=True,
            parent_name=parent_name,
            config=config,
            roots={"root"},
            process_properties=True,
        )[0]
        assert result.class_info.name == expected

    def test_model_bad_properties(self, config):
        from openapi_python_client.parser.properties import ModelProperty

        data = oai.Schema(
            properties={
                "bad": oai.Reference.model_construct(ref="#/components/schema/NotExist"),
            },
        )
        result = ModelProperty.build(
            data=data,
            name="prop",
            schemas=Schemas(),
            required=True,
            parent_name="parent",
            config=config,
            roots={"root"},
            process_properties=True,
        )[0]
        assert isinstance(result, PropertyError)

    def test_model_bad_additional_properties(self, config):
        from openapi_python_client.parser.properties import ModelProperty

        additional_properties = oai.Schema(
            type="object",
            properties={
                "bad": oai.Reference(ref="#/components/schemas/not_exist"),
            },
        )
        data = oai.Schema(additionalProperties=additional_properties)
        result = ModelProperty.build(
            data=data,
            name="prop",
            schemas=Schemas(),
            required=True,
            parent_name="parent",
            config=config,
            roots={"root"},
            process_properties=True,
        )[0]
        assert isinstance(result, PropertyError)

    def test_process_properties_false(self, model_property_factory, config):
        from openapi_python_client.parser.properties import Class, ModelProperty

        name = "prop"
        required = True

        data = oai.Schema.model_construct(
            required=["req"],
            title="MyModel",
            properties={
                "req": oai.Schema.model_construct(type="string"),
                "opt": oai.Schema(type="string", format="date-time"),
            },
            description="A class called MyModel",
        )
        schemas = Schemas(classes_by_reference={"OtherModel": None}, classes_by_name={"OtherModel": None})
        roots = {"root"}
        class_info = Class(name="ParentMyModel", module_name="parent_my_model")

        model, new_schemas = ModelProperty.build(
            data=data,
            name=name,
            schemas=schemas,
            required=required,
            parent_name="parent",
            config=config,
            roots=roots,
            process_properties=False,
        )

        assert new_schemas != schemas
        assert new_schemas.classes_by_name == {
            "OtherModel": None,
            "ParentMyModel": model,
        }
        assert new_schemas.classes_by_reference == {
            "OtherModel": None,
        }
        assert model == model_property_factory(
            name=name,
            required=required,
            class_info=class_info,
            data=data,
            description=data.description,
            roots={*roots, class_info.name},
        )


class TestProcessProperties:
    def test_conflicting_properties_different_types(
        self, model_property_factory, string_property_factory, int_property_factory, config
    ):
        data = oai.Schema.model_construct(
            allOf=[oai.Reference.model_construct(ref="#/First"), oai.Reference.model_construct(ref="#/Second")]
        )
        schemas = Schemas(
            classes_by_reference={
                "/First": model_property_factory(
                    required_properties=[], optional_properties=[string_property_factory()]
                ),
                "/Second": model_property_factory(required_properties=[], optional_properties=[int_property_factory()]),
            }
        )

        result = _process_properties(data=data, schemas=schemas, class_name="", config=config, roots={"root"})

        assert isinstance(result, PropertyError)

    def test_process_properties_reference_not_exist(self, config):
        data = oai.Schema(
            properties={
                "bad": oai.Reference.model_construct(ref="#/components/schema/NotExist"),
            },
        )

        result = _process_properties(data=data, class_name="", schemas=Schemas(), config=config, roots={"root"})

        assert isinstance(result, PropertyError)

    def test_process_properties_all_of_reference_not_exist(self, config):
        data = oai.Schema.model_construct(allOf=[oai.Reference.model_construct(ref="#/components/schema/NotExist")])

        result = _process_properties(data=data, class_name="", schemas=Schemas(), config=config, roots={"root"})

        assert isinstance(result, PropertyError)

    def test_process_properties_model_property_roots(self, model_property_factory, config):
        roots = {"root"}
        data = oai.Schema(properties={"test_model_property": oai.Schema.model_construct(type="object")})

        result = _process_properties(data=data, class_name="", schemas=Schemas(), config=config, roots=roots)

        assert all(root in result.optional_props[0].roots for root in roots)

    def test_invalid_reference(self, config):
        data = oai.Schema.model_construct(allOf=[oai.Reference.model_construct(ref="ThisIsNotGood")])
        schemas = Schemas()

        result = _process_properties(data=data, schemas=schemas, class_name="", config=config, roots={"root"})

        assert isinstance(result, PropertyError)

    def test_non_model_reference(self, enum_property_factory, config):
        data = oai.Schema.model_construct(allOf=[oai.Reference.model_construct(ref="#/First")])
        schemas = Schemas(
            classes_by_reference={
                "/First": enum_property_factory(),
            }
        )

        result = _process_properties(data=data, schemas=schemas, class_name="", config=config, roots={"root"})

        assert isinstance(result, PropertyError)

    def test_reference_not_processed(self, model_property_factory, config):
        data = oai.Schema.model_construct(allOf=[oai.Reference.model_construct(ref="#/Unprocessed")])
        schemas = Schemas(
            classes_by_reference={
                "/Unprocessed": model_property_factory(),
            }
        )

        result = _process_properties(data=data, schemas=schemas, class_name="", config=config, roots={"root"})

        assert isinstance(result, PropertyError)

    def test_allof_string_and_string_enum(
        self, model_property_factory, enum_property_factory, string_property_factory, config
    ):
        data = oai.Schema.model_construct(
            allOf=[oai.Reference.model_construct(ref="#/First"), oai.Reference.model_construct(ref="#/Second")]
        )
        enum_property = enum_property_factory(
            values={"foo": "foo"},
        )
        schemas = Schemas(
            classes_by_reference={
                "/First": model_property_factory(
                    required_properties=[],
                    optional_properties=[string_property_factory(required=False)],
                ),
                "/Second": model_property_factory(required_properties=[], optional_properties=[enum_property]),
            }
        )

        result = _process_properties(data=data, schemas=schemas, class_name="", config=config, roots={"root"})
        assert result.required_props[0] == enum_property

    def test_allof_string_enum_and_string(
        self, model_property_factory, enum_property_factory, string_property_factory, config
    ):
        data = oai.Schema.model_construct(
            allOf=[oai.Reference.model_construct(ref="#/First"), oai.Reference.model_construct(ref="#/Second")]
        )
        enum_property = enum_property_factory(
            required=False,
            values={"foo": "foo"},
        )
        schemas = Schemas(
            classes_by_reference={
                "/First": model_property_factory(required_properties=[], optional_properties=[enum_property]),
                "/Second": model_property_factory(
                    required_properties=[],
                    optional_properties=[string_property_factory(required=False)],
                ),
            }
        )

        result = _process_properties(data=data, schemas=schemas, class_name="", config=config, roots={"root"})
        assert result.optional_props[0] == enum_property

    def test_allof_int_and_int_enum(self, model_property_factory, enum_property_factory, int_property_factory, config):
        data = oai.Schema.model_construct(
            allOf=[oai.Reference.model_construct(ref="#/First"), oai.Reference.model_construct(ref="#/Second")]
        )
        enum_property = enum_property_factory(
            values={"foo": 1},
            value_type=int,
        )
        schemas = Schemas(
            classes_by_reference={
                "/First": model_property_factory(required_properties=[], optional_properties=[int_property_factory()]),
                "/Second": model_property_factory(required_properties=[], optional_properties=[enum_property]),
            }
        )

        result = _process_properties(data=data, schemas=schemas, class_name="", config=config, roots={"root"})
        assert result.required_props[0] == enum_property

    def test_allof_enum_incompatible_type(
        self, model_property_factory, enum_property_factory, int_property_factory, config
    ):
        data = oai.Schema.model_construct(
            allOf=[oai.Reference.model_construct(ref="#/First"), oai.Reference.model_construct(ref="#/Second")]
        )
        enum_property = enum_property_factory(
            values={"foo": 1},
            value_type=str,
        )
        schemas = Schemas(
            classes_by_reference={
                "/First": model_property_factory(required_properties=[], optional_properties=[int_property_factory()]),
                "/Second": model_property_factory(required_properties=[], optional_properties=[enum_property]),
            }
        )

        result = _process_properties(data=data, schemas=schemas, class_name="", config=config, roots={"root"})
        assert isinstance(result, PropertyError)

    def test_allof_string_enums(self, model_property_factory, enum_property_factory, config):
        data = oai.Schema.model_construct(
            allOf=[oai.Reference.model_construct(ref="#/First"), oai.Reference.model_construct(ref="#/Second")]
        )
        enum_property1 = enum_property_factory(
            name="an_enum",
            value_type=str,
            values={"foo": "foo"},
        )
        enum_property2 = enum_property_factory(
            name="an_enum",
            values={"foo": "foo", "bar": "bar"},
            value_type=str,
        )
        schemas = Schemas(
            classes_by_reference={
                "/First": model_property_factory(required_properties=[], optional_properties=[enum_property1]),
                "/Second": model_property_factory(required_properties=[], optional_properties=[enum_property2]),
            }
        )

        result = _process_properties(data=data, schemas=schemas, class_name="", config=config, roots={"root"})
        assert result.required_props[0] == enum_property1

    def test_allof_int_enums(self, model_property_factory, enum_property_factory, config):
        data = oai.Schema.model_construct(
            allOf=[oai.Reference.model_construct(ref="#/First"), oai.Reference.model_construct(ref="#/Second")]
        )
        enum_property1 = enum_property_factory(
            name="an_enum",
            values={"foo": 1, "bar": 2},
            value_type=int,
        )
        enum_property2 = enum_property_factory(
            name="an_enum",
            values={"foo": 1},
            value_type=int,
        )
        schemas = Schemas(
            classes_by_reference={
                "/First": model_property_factory(required_properties=[], optional_properties=[enum_property1]),
                "/Second": model_property_factory(required_properties=[], optional_properties=[enum_property2]),
            }
        )

        result = _process_properties(data=data, schemas=schemas, class_name="", config=config, roots={"root"})
        assert result.required_props[0] == enum_property2

    def test_allof_enums_are_not_subsets(self, model_property_factory, enum_property_factory, config):
        data = oai.Schema.model_construct(
            allOf=[oai.Reference.model_construct(ref="#/First"), oai.Reference.model_construct(ref="#/Second")]
        )
        enum_property1 = enum_property_factory(
            name="an_enum",
            values={"foo": 1, "bar": 2},
            value_type=int,
        )
        enum_property2 = enum_property_factory(
            name="an_enum",
            values={"foo": 1, "baz": 3},
            value_type=int,
        )
        schemas = Schemas(
            classes_by_reference={
                "/First": model_property_factory(required_properties=[], optional_properties=[enum_property1]),
                "/Second": model_property_factory(required_properties=[], optional_properties=[enum_property2]),
            }
        )

        result = _process_properties(data=data, schemas=schemas, class_name="", config=config, roots={"root"})
        assert isinstance(result, PropertyError)

    def test_duplicate_properties(self, model_property_factory, string_property_factory, config):
        data = oai.Schema.model_construct(
            allOf=[oai.Reference.model_construct(ref="#/First"), oai.Reference.model_construct(ref="#/Second")]
        )
        prop = string_property_factory(required=False)
        schemas = Schemas(
            classes_by_reference={
                "/First": model_property_factory(required_properties=[], optional_properties=[prop]),
                "/Second": model_property_factory(required_properties=[], optional_properties=[prop]),
            }
        )

        result = _process_properties(data=data, schemas=schemas, class_name="", config=config, roots={"root"})

        assert result.optional_props == [prop], "There should only be one copy of duplicate properties"

    @pytest.mark.parametrize("first_required", [True, False])
    @pytest.mark.parametrize("second_required", [True, False])
    def test_mixed_requirements(
        self,
        model_property_factory,
        first_required,
        second_required,
        string_property_factory,
        config,
    ):
        data = oai.Schema.model_construct(
            allOf=[oai.Reference.model_construct(ref="#/First"), oai.Reference.model_construct(ref="#/Second")]
        )
        schemas = Schemas(
            classes_by_reference={
                "/First": model_property_factory(
                    required_properties=[],
                    optional_properties=[string_property_factory(required=first_required)],
                ),
                "/Second": model_property_factory(
                    required_properties=[],
                    optional_properties=[string_property_factory(required=second_required)],
                ),
            }
        )
        roots = {"root"}

        result = _process_properties(data=data, schemas=schemas, class_name="", config=config, roots=roots)

        required = first_required or second_required
        expected_prop = string_property_factory(
            required=required,
        )

        assert result.schemas.dependencies == {"/First": roots, "/Second": roots}
        if not required:
            assert result.optional_props == [expected_prop]
        else:
            assert result.required_props == [expected_prop]

    def test_direct_properties_non_ref(self, string_property_factory, config):
        data = oai.Schema.model_construct(
            allOf=[
                oai.Schema.model_construct(
                    required=["first"],
                    properties={
                        "first": oai.Schema.model_construct(type="string"),
                        "second": oai.Schema.model_construct(type="string"),
                    },
                )
            ]
        )
        schemas = Schemas()

        result = _process_properties(data=data, schemas=schemas, class_name="", config=config, roots={"root"})

        assert result.optional_props == [string_property_factory(name="second", required=False)]
        assert result.required_props == [string_property_factory(name="first", required=True)]

    def test_conflicting_property_names(self, config):
        data = oai.Schema.model_construct(
            properties={
                "int": oai.Schema.model_construct(type="integer"),
                "int_": oai.Schema.model_construct(type="string"),
            }
        )
        schemas = Schemas()
        result = _process_properties(data=data, schemas=schemas, class_name="", config=config, roots={"root"})
        assert isinstance(result, PropertyError)

    def test_merge_inline_objects(self, model_property_factory, enum_property_factory, config):
        data = oai.Schema.model_construct(
            allOf=[
                oai.Schema.model_construct(
                    type="object",
                    properties={
                        "prop1": oai.Schema.model_construct(type="string", default="a"),
                    },
                ),
                oai.Schema.model_construct(
                    type="object",
                    properties={
                        "prop1": oai.Schema.model_construct(type="string", description="desc"),
                    },
                ),
            ]
        )
        schemas = Schemas()

        result = _process_properties(data=data, schemas=schemas, class_name="", config=config, roots={"root"})
        assert not isinstance(result, PropertyError)
        assert len(result.optional_props) == 1
        prop1 = result.optional_props[0]
        assert isinstance(prop1, StringProperty)
        assert prop1.description == "desc"
        assert prop1.default == StringProperty.convert_value("a")


class TestProcessModel:
    def test_process_model_error(self, mocker, model_property_factory, config):
        from openapi_python_client.parser.properties import Schemas
        from openapi_python_client.parser.properties.model_property import process_model

        model_prop = model_property_factory()
        schemas = Schemas()
        process_property_data = mocker.patch(f"{MODULE_NAME}._process_property_data")
        process_property_data.return_value = (PropertyError(), schemas)

        result = process_model(model_prop=model_prop, schemas=schemas, config=config)

        assert result == PropertyError()
        assert model_prop.required_properties is None
        assert model_prop.optional_properties is None
        assert model_prop.relative_imports is None
        assert model_prop.additional_properties is None

    def test_process_model(self, mocker, model_property_factory, config):
        from openapi_python_client.parser.properties import Schemas
        from openapi_python_client.parser.properties.model_property import _PropertyData, process_model

        model_prop = model_property_factory()
        schemas = Schemas()
        property_data = _PropertyData(
            required_props=["required"],
            optional_props=["optional"],
            relative_imports={"relative"},
            lazy_imports={"lazy"},
            schemas=schemas,
        )
        additional_properties = True
        process_property_data = mocker.patch(f"{MODULE_NAME}._process_property_data")
        process_property_data.return_value = ((property_data, additional_properties), schemas)

        result = process_model(model_prop=model_prop, schemas=schemas, config=config)

        assert result == schemas
        assert model_prop.required_properties == property_data.required_props
        assert model_prop.optional_properties == property_data.optional_props
        assert model_prop.relative_imports == property_data.relative_imports
        assert model_prop.lazy_imports == property_data.lazy_imports
        assert model_prop.additional_properties == additional_properties


def test_set_relative_imports(model_property_factory):
    from openapi_python_client.parser.properties import Class

    class_info = Class("ClassName", module_name="module_name")
    relative_imports = {f"from ..models.{class_info.module_name} import {class_info.name}"}

    model_property = model_property_factory(class_info=class_info, relative_imports=relative_imports)

    assert model_property.relative_imports == set()
