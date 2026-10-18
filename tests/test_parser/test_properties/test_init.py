import pytest

import openapi_python_client.schema as oai
from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties import (
    AnyProperty,
    Class,
    ListProperty,
    ReferencePath,
    Schemas,
    _propogate_removal,
    build_schemas,
    property_from_data,
)
from openapi_python_client.schema.ref import Ref
from openapi_python_client.schema.untrusted_string import UntrustedString
from openapi_python_client.strings import ClassName, PythonCode, PythonIdentifier

MODULE_NAME = "openapi_python_client.parser.properties"


class TestFileProperty:
    @pytest.mark.parametrize("required", (True, False))
    def test_get_imports(self, file_property_factory, required):
        p = file_property_factory(required=required)

        expected = {
            "from io import BytesIO",
            "from ...types import File, FileTypes",
        }
        if not required:
            expected |= {
                "from ...types import UNSET, Unset",
            }

        assert p.get_imports(prefix="...") == expected


class TestUnionProperty:
    def test_get_lazy_import_base_inner(self, union_property_factory):
        p = union_property_factory()
        assert p.get_lazy_imports(prefix="..") == set()

    def test_get_lazy_import_model_inner(self, union_property_factory, model_property_factory):
        m = model_property_factory()
        p = union_property_factory(inner_properties=[m])
        assert p.get_lazy_imports(prefix="..") == {"from ..models.my_module import MyClass"}

    @pytest.mark.parametrize(
        "required,no_optional,json,expected",
        [
            (False, False, False, "datetime.datetime | str | Unset"),
            (False, True, False, "datetime.datetime | str"),
            (True, False, False, "datetime.datetime | str"),
            (True, True, False, "datetime.datetime | str"),
            (False, False, True, "str | Unset"),
            (False, True, True, "str"),
            (True, False, True, "str"),
            (True, True, True, "str"),
        ],
    )
    def test_get_type_string(
        self,
        union_property_factory,
        date_time_property_factory,
        string_property_factory,
        required,
        no_optional,
        json,
        expected,
    ):
        p = union_property_factory(
            required=required,
            inner_properties=[date_time_property_factory(), string_property_factory()],
        )

        assert p.get_base_type_string() == PythonCode("datetime.datetime | str")

        assert p.get_type_string(no_optional=no_optional, json=json) == PythonCode(expected)

    def test_get_base_type_string_base_inners(
        self, union_property_factory, date_time_property_factory, string_property_factory
    ):
        p = union_property_factory(inner_properties=[date_time_property_factory(), string_property_factory()])

        assert p.get_base_type_string() == PythonCode("datetime.datetime | str")

    def test_get_base_type_string_one_base_inner(self, union_property_factory, date_time_property_factory):
        p = union_property_factory(
            inner_properties=[date_time_property_factory()],
        )

        assert p.get_base_type_string() == PythonCode("datetime.datetime")

    def test_get_base_type_string_one_model_inner(self, union_property_factory, model_property_factory):
        p = union_property_factory(
            inner_properties=[model_property_factory()],
        )

        assert p.get_base_type_string() == PythonCode("MyClass")

    def test_get_base_type_string_model_inners(
        self, union_property_factory, date_time_property_factory, model_property_factory
    ):
        p = union_property_factory(inner_properties=[date_time_property_factory(), model_property_factory()])

        assert p.get_base_type_string() == PythonCode("datetime.datetime | MyClass")

    def test_get_base_json_type_string(self, union_property_factory, date_time_property_factory):
        p = union_property_factory(
            inner_properties=[date_time_property_factory()],
        )

        assert p.get_base_json_type_string() == PythonCode("str")

    @pytest.mark.parametrize("required", (True, False))
    def test_get_type_imports(self, union_property_factory, date_time_property_factory, required):
        p = union_property_factory(
            inner_properties=[date_time_property_factory()],
            required=required,
        )
        expected = {
            "import datetime",
            "from typing import cast",
        }
        if not required:
            expected |= {
                "from ...types import UNSET, Unset",
            }

        assert p.get_imports(prefix="...") == expected


class TestPropertyFromData:
    def test_property_from_data_ref_model(self, model_property_factory, config):
        name = "new_name"
        required = False
        class_name = ClassName(UntrustedString("MyModel"), "")
        data = oai.Reference.model_construct(ref=Ref(f"#/components/schemas/{class_name}"))
        class_info = Class(name=class_name, module_name=PythonIdentifier("my_model", ""))

        existing_model = model_property_factory(
            name="old_name",
            class_info=class_info,
        )
        schemas = Schemas(
            classes_by_reference={ReferencePath(UntrustedString(f"/components/schemas/{class_name}")): existing_model}
        )

        prop, new_schemas = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="", config=config
        )

        assert prop == model_property_factory(
            name=name,
            required=required,
            class_info=class_info,
        )
        assert schemas == new_schemas

    def test_property_from_data_ref_not_found(self, mocker):
        data = oai.Reference.model_construct(ref="a/b/c")
        parse_reference_path = mocker.patch(f"{MODULE_NAME}.parse_reference_path")
        schemas = Schemas()

        prop, new_schemas = property_from_data(
            name="a_prop", required=False, data=data, schemas=schemas, parent_name="parent", config=mocker.MagicMock()
        )

        parse_reference_path.assert_called_once_with(data.ref)
        assert prop == PropertyError(data=data, detail="Could not find reference in parsed models or enums")
        assert schemas == new_schemas
        assert schemas.dependencies == {}

    @pytest.mark.parametrize("references_exist", (True, False))
    def test_property_from_data_ref(self, any_property_factory, references_exist, config):
        name = "new_name"
        required = False
        ref_path = ReferencePath(UntrustedString("/components/schemas/RefName"))
        data = oai.Reference.model_construct(ref=Ref(f"#{ref_path.get_untrusted_value()}"))
        roots = {"new_root"}

        existing_property = any_property_factory(name="old_name")
        references = {ref_path: {"old_root"}} if references_exist else {}
        schemas = Schemas(classes_by_reference={ref_path: existing_property}, dependencies=references)

        prop, new_schemas = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="", config=config, roots=roots
        )

        assert prop == any_property_factory(name=name, required=required)
        assert schemas == new_schemas
        assert schemas.dependencies == {ref_path: {*roots, *references.get(ref_path, set())}}


class TestStringBasedProperty:
    def test__string_based_property_binary_format(self, file_property_factory, config):
        name = "file_prop"
        required = True
        data = oai.Schema.model_construct(type="string", schema_format="binary", default="a")

        p, _ = property_from_data(
            name=name, required=required, data=data, schemas=Schemas(), config=config, parent_name=""
        )
        assert p == file_property_factory(name=name, required=required)


class TestProcessModels:
    def test_resolve_reference_to_single_allof_reference(self, config, model_property_factory):
        # test for https://github.com/openapi-generators/openapi-python-client/issues/1091

        components = {
            UntrustedString("Model1"): oai.Schema.model_construct(
                type="object",
                properties={
                    UntrustedString("prop1"): oai.Schema.model_construct(type="string"),
                },
            ),
            UntrustedString("Model2"): oai.Schema.model_construct(
                allOf=[
                    oai.Reference.model_construct(ref=Ref("#/components/schemas/Model1")),
                ]
            ),
            UntrustedString("Model3"): oai.Schema.model_construct(
                allOf=[
                    oai.Reference.model_construct(ref=Ref("#/components/schemas/Model2")),
                    oai.Schema.model_construct(
                        type="object",
                        properties={
                            UntrustedString("prop2"): oai.Schema.model_construct(type="string"),
                        },
                    ),
                ],
            ),
        }
        schemas = Schemas()

        result = build_schemas(components=components, schemas=schemas, config=config)

        assert result.errors == []
        assert result.models_to_process == []

        # Classes should only be generated for Model1 and Model3
        assert result.classes_by_name.keys() == {"Model1", "Model3"}

        # References to Model2 should be resolved to the same class as Model1
        assert result.classes_by_reference.keys() == {
            "/components/schemas/Model1",
            "/components/schemas/Model2",
            "/components/schemas/Model3",
        }
        assert (
            result.classes_by_reference[ReferencePath(UntrustedString("/components/schemas/Model2"))].class_info
            == result.classes_by_reference[ReferencePath(UntrustedString("/components/schemas/Model1"))].class_info
        )

        # Verify that Model3 extended the properties from Model1
        assert [p.name for p in result.classes_by_name["Model3"].optional_properties] == ["prop1", "prop2"]


class TestPropogateRemoval:
    def test_propogate_removal_class_name(self):
        root = ClassName(UntrustedString("ClassName"), "")
        ref_path = ReferencePath(UntrustedString("/reference"))
        other_class_name = ClassName(UntrustedString("OtherClassName"), "")
        schemas = Schemas(
            classes_by_name={root: None, other_class_name: None},
            classes_by_reference={ref_path: None},
            dependencies={ref_path: {other_class_name}, root: {ref_path}},
        )
        error = PropertyError()

        _propogate_removal(root=root, schemas=schemas, error=error)

        assert schemas.classes_by_name == {other_class_name: None}
        assert schemas.classes_by_reference == {ref_path: None}
        assert not error.detail

    def test_propogate_removal_ref_path(self):
        root = ReferencePath(UntrustedString("/root/reference"))
        class_name = ClassName(UntrustedString("ClassName"), "")
        ref_path = ReferencePath(UntrustedString("/ref/path"))
        schemas = Schemas(
            classes_by_name={class_name: None},
            classes_by_reference={root: None, ref_path: None},
            dependencies={root: {ref_path, class_name}},
        )
        error = PropertyError()

        _propogate_removal(root=root, schemas=schemas, error=error)

        assert schemas.classes_by_name == {}
        assert schemas.classes_by_reference == {}
        assert error.detail == f"\n{root.get_untrusted_value()}\n{ref_path.get_untrusted_value()}"

    def test_propogate_removal_ref_path_no_refs(self):
        root = ReferencePath(UntrustedString("/root/reference"))
        class_name = ClassName(UntrustedString("ClassName"), "")
        ref_path = ReferencePath(UntrustedString("/ref/path"))
        schemas = Schemas(
            classes_by_name={class_name: None},
            classes_by_reference={root: None, ref_path: None},
        )
        error = PropertyError()

        _propogate_removal(root=root, schemas=schemas, error=error)

        assert schemas.classes_by_name == {class_name: None}
        assert schemas.classes_by_reference == {ref_path: None}
        assert error.detail == f"\n{root.get_untrusted_value()}"

    def test_propogate_removal_ref_path_already_removed(self):
        root = ReferencePath(UntrustedString("/root/reference"))
        class_name = ClassName(UntrustedString("ClassName"), "")
        ref_path = ReferencePath(UntrustedString("/ref/path"))
        schemas = Schemas(
            classes_by_name={class_name: None},
            classes_by_reference={ref_path: None},
            dependencies={root: {ref_path, class_name}},
        )
        error = PropertyError()

        _propogate_removal(root=root, schemas=schemas, error=error)

        assert schemas.classes_by_name == {class_name: None}
        assert schemas.classes_by_reference == {ref_path: None}
        assert not error.detail


class TestArrayWithoutItems:
    def test_array_without_items_becomes_list_of_any(self, config):
        """Issue #1435: `{"type": "array"}` with no `items`/`prefixItems` is
        valid in OpenAPI 3.1 (JSON Schema 2020-12) and means "array of any". It
        must generate a list of Any instead of failing with a PropertyError."""
        data = oai.Schema(type="array", description="anything")
        prop, _ = property_from_data(
            name=UntrustedString("metrics"),
            required=True,
            data=data,
            schemas=Schemas(),
            parent_name="parent",
            config=config,
        )

        assert isinstance(prop, ListProperty)
        assert isinstance(prop.inner_property, AnyProperty)
        assert prop.get_base_type_string().as_unembedded_code() == "list[Any]"
