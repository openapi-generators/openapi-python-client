from unittest.mock import call

import pytest

import openapi_python_client.schema as oai
from openapi_python_client.parser.errors import ParameterError, PropertyError
from openapi_python_client.parser.properties import (
    ReferencePath,
    Schemas,
)
from openapi_python_client.utils import ClassName, PythonIdentifier

MODULE_NAME = "openapi_python_client.parser.properties"


class TestFileProperty:
    def test_is_base_type(self, file_property_factory):
        assert file_property_factory().is_base_type is True

    @pytest.mark.parametrize("required", (True, False))
    def test_get_imports(self, file_property_factory, required):
        p = file_property_factory(required=required)

        expected = {
            "from io import BytesIO",
            "from ...types import File, FileJsonType",
        }
        if not required:
            expected |= {
                "from typing import Union",
                "from ...types import UNSET, Unset",
            }

        assert p.get_imports(prefix="...") == expected


class TestUnionProperty:
    def test_is_base_type(self, union_property_factory):
        assert union_property_factory().is_base_type is False

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
            (False, False, False, "Union[Unset, datetime.datetime, str]"),
            (False, True, False, "Union[datetime.datetime, str]"),
            (True, False, False, "Union[datetime.datetime, str]"),
            (True, True, False, "Union[datetime.datetime, str]"),
            (False, False, True, "Union[Unset, str]"),
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

        assert p.get_base_type_string() == "Union[datetime.datetime, str]"

        assert p.get_type_string(no_optional=no_optional, json=json) == expected

    def test_get_base_type_string_base_inners(
        self, union_property_factory, date_time_property_factory, string_property_factory
    ):
        p = union_property_factory(inner_properties=[date_time_property_factory(), string_property_factory()])

        assert p.get_base_type_string() == "Union[datetime.datetime, str]"

    def test_get_base_type_string_one_base_inner(self, union_property_factory, date_time_property_factory):
        p = union_property_factory(
            inner_properties=[date_time_property_factory()],
        )

        assert p.get_base_type_string() == "datetime.datetime"

    def test_get_base_type_string_one_model_inner(self, union_property_factory, model_property_factory):
        p = union_property_factory(
            inner_properties=[model_property_factory()],
        )

        assert p.get_base_type_string() == "'MyClass'"

    def test_get_base_type_string_model_inners(
        self, union_property_factory, date_time_property_factory, model_property_factory
    ):
        p = union_property_factory(inner_properties=[date_time_property_factory(), model_property_factory()])

        assert p.get_base_type_string() == "Union['MyClass', datetime.datetime]"

    def test_get_base_json_type_string(self, union_property_factory, date_time_property_factory):
        p = union_property_factory(
            inner_properties=[date_time_property_factory()],
        )

        assert p.get_base_json_type_string() == "str"

    @pytest.mark.parametrize("required", (True, False))
    def test_get_type_imports(self, union_property_factory, date_time_property_factory, required):
        p = union_property_factory(
            inner_properties=[date_time_property_factory()],
            required=required,
        )
        expected = {
            "import datetime",
            "from typing import cast",
            "from dateutil.parser import isoparse",
            "from typing import cast, Union",
        }
        if not required:
            expected |= {
                "from typing import Union",
                "from ...types import UNSET, Unset",
            }

        assert p.get_imports(prefix="...") == expected


class TestPropertyFromData:
    def test_property_from_data_ref_model(self, model_property_factory, config):
        from openapi_python_client.parser.properties import Class, Schemas, property_from_data

        name = "new_name"
        required = False
        class_name = ClassName("MyModel", "")
        data = oai.Reference.model_construct(ref=f"#/components/schemas/{class_name}")
        class_info = Class(name=class_name, module_name=PythonIdentifier("my_model", ""))

        existing_model = model_property_factory(
            name="old_name",
            class_info=class_info,
        )
        schemas = Schemas(classes_by_reference={ReferencePath(f"/components/schemas/{class_name}"): existing_model})

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
        from openapi_python_client.parser.properties import PropertyError, Schemas, property_from_data

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
        from openapi_python_client.parser.properties import Schemas, property_from_data

        name = "new_name"
        required = False
        ref_path = "/components/schemas/RefName"
        data = oai.Reference.model_construct(ref=f"#{ref_path}")
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

    def test_property_from_data_invalid_ref(self, mocker):
        from openapi_python_client.parser.properties import PropertyError, Schemas, property_from_data

        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Reference.model_construct(ref=mocker.MagicMock())
        parse_reference_path = mocker.patch(
            f"{MODULE_NAME}.parse_reference_path", return_value=PropertyError(detail="bad stuff")
        )
        schemas = Schemas()

        prop, new_schemas = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=mocker.MagicMock()
        )

        parse_reference_path.assert_called_once_with(data.ref)
        assert prop == PropertyError(data=data, detail="bad stuff")
        assert schemas == new_schemas


class TestStringBasedProperty:
    def test__string_based_property_binary_format(self, file_property_factory, config):
        from openapi_python_client.parser.properties import property_from_data

        name = "file_prop"
        required = True
        data = oai.Schema.model_construct(type="string", schema_format="binary", default="a")

        p, _ = property_from_data(
            name=name, required=required, data=data, schemas=Schemas(), config=config, parent_name=""
        )
        assert p == file_property_factory(name=name, required=required)


class TestCreateSchemas:
    def test_skips_references_and_keeps_going(self, mocker, config):
        from openapi_python_client.parser.properties import Schemas, _create_schemas
        from openapi_python_client.schema import Reference, Schema

        components = {"a_ref": Reference.model_construct(), "a_schema": Schema.model_construct()}
        update_schemas_with_data = mocker.patch(f"{MODULE_NAME}.update_schemas_with_data")
        parse_reference_path = mocker.patch(f"{MODULE_NAME}.parse_reference_path")
        schemas = Schemas()

        result = _create_schemas(components=components, schemas=schemas, config=config)
        # Should not even try to parse a path for the Reference
        parse_reference_path.assert_called_once_with("#/components/schemas/a_schema")
        update_schemas_with_data.assert_called_once_with(
            ref_path=parse_reference_path.return_value,
            config=config,
            data=components["a_schema"],
            schemas=Schemas(
                errors=[PropertyError(detail="Reference schemas are not supported.", data=components["a_ref"])]
            ),
        )
        assert result == update_schemas_with_data.return_value

    def test_records_bad_uris_and_keeps_going(self, mocker, config):
        from openapi_python_client.parser.properties import Schemas, _create_schemas
        from openapi_python_client.schema import Schema

        components = {"first": Schema.model_construct(), "second": Schema.model_construct()}
        update_schemas_with_data = mocker.patch(f"{MODULE_NAME}.update_schemas_with_data")
        parse_reference_path = mocker.patch(
            f"{MODULE_NAME}.parse_reference_path", side_effect=[PropertyError(detail="some details"), "a_path"]
        )
        schemas = Schemas()

        result = _create_schemas(components=components, schemas=schemas, config=config)
        parse_reference_path.assert_has_calls(
            [
                call("#/components/schemas/first"),
                call("#/components/schemas/second"),
            ]
        )
        update_schemas_with_data.assert_called_once_with(
            ref_path="a_path",
            config=config,
            data=components["second"],
            schemas=Schemas(errors=[PropertyError(detail="some details", data=components["first"])]),
        )
        assert result == update_schemas_with_data.return_value

    def test_retries_failing_properties_while_making_progress(self, mocker, config):
        from openapi_python_client.parser.properties import Schemas, _create_schemas
        from openapi_python_client.schema import Schema

        components = {"first": Schema.model_construct(), "second": Schema.model_construct()}
        update_schemas_with_data = mocker.patch(
            f"{MODULE_NAME}.update_schemas_with_data", side_effect=[PropertyError(), Schemas(), PropertyError()]
        )
        parse_reference_path = mocker.patch(f"{MODULE_NAME}.parse_reference_path")
        schemas = Schemas()

        result = _create_schemas(components=components, schemas=schemas, config=config)
        parse_reference_path.assert_has_calls(
            [
                call("#/components/schemas/first"),
                call("#/components/schemas/second"),
                call("#/components/schemas/first"),
            ]
        )
        assert update_schemas_with_data.call_count == 3
        assert result.errors == [PropertyError()]


class TestProcessModels:
    def test_detect_recursive_allof_reference_no_retry(self, mocker, model_property_factory, config):
        from openapi_python_client.parser.properties import Class, _process_models
        from openapi_python_client.schema import Reference

        class_name = ClassName("class_name", "")
        recursive_model = model_property_factory(
            class_info=Class(name=class_name, module_name=PythonIdentifier("module_name", ""))
        )
        second_model = model_property_factory()
        schemas = Schemas(
            classes_by_name={
                "recursive": recursive_model,
                "second": second_model,
            },
            models_to_process=[recursive_model, second_model],
        )
        recursion_error = PropertyError(data=Reference.model_construct(ref=f"#/{class_name}"))
        process_model = mocker.patch(f"{MODULE_NAME}.process_model", side_effect=[recursion_error, schemas])
        process_model_errors = mocker.patch(f"{MODULE_NAME}._process_model_errors", return_value=["error"])

        result = _process_models(schemas=schemas, config=config)

        process_model.assert_has_calls(
            [
                call(recursive_model, schemas=schemas, config=config),
                call(schemas.classes_by_name["second"], schemas=schemas, config=config),
            ]
        )
        assert process_model_errors.was_called_once_with([(recursive_model, recursion_error)])
        assert all(error in result.errors for error in process_model_errors.return_value)
        assert "\n\nRecursive allOf reference found" in recursion_error.detail

    def test_resolve_reference_to_single_allof_reference(self, config, model_property_factory):
        # test for https://github.com/openapi-generators/openapi-python-client/issues/1091
        from openapi_python_client.parser.properties import Schemas, build_schemas

        components = {
            "Model1": oai.Schema.model_construct(
                type="object",
                properties={
                    "prop1": oai.Schema.model_construct(type="string"),
                },
            ),
            "Model2": oai.Schema.model_construct(
                allOf=[
                    oai.Reference.model_construct(ref="#/components/schemas/Model1"),
                ]
            ),
            "Model3": oai.Schema.model_construct(
                allOf=[
                    oai.Reference.model_construct(ref="#/components/schemas/Model2"),
                    oai.Schema.model_construct(
                        type="object",
                        properties={
                            "prop2": oai.Schema.model_construct(type="string"),
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
            result.classes_by_reference["/components/schemas/Model2"].class_info
            == result.classes_by_reference["/components/schemas/Model1"].class_info
        )

        # Verify that Model3 extended the properties from Model1
        assert [p.name for p in result.classes_by_name["Model3"].optional_properties] == ["prop1", "prop2"]


class TestPropogateRemoval:
    def test_propogate_removal_class_name(self):
        from openapi_python_client.parser.properties import ReferencePath, _propogate_removal
        from openapi_python_client.utils import ClassName

        root = ClassName("ClassName", "")
        ref_path = ReferencePath("/reference")
        other_class_name = ClassName("OtherClassName", "")
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
        from openapi_python_client.parser.properties import ReferencePath, _propogate_removal
        from openapi_python_client.utils import ClassName

        root = ReferencePath("/root/reference")
        class_name = ClassName("ClassName", "")
        ref_path = ReferencePath("/ref/path")
        schemas = Schemas(
            classes_by_name={class_name: None},
            classes_by_reference={root: None, ref_path: None},
            dependencies={root: {ref_path, class_name}},
        )
        error = PropertyError()

        _propogate_removal(root=root, schemas=schemas, error=error)

        assert schemas.classes_by_name == {}
        assert schemas.classes_by_reference == {}
        assert error.detail == f"\n{root}\n{ref_path}"

    def test_propogate_removal_ref_path_no_refs(self):
        from openapi_python_client.parser.properties import ReferencePath, _propogate_removal
        from openapi_python_client.utils import ClassName

        root = ReferencePath("/root/reference")
        class_name = ClassName("ClassName", "")
        ref_path = ReferencePath("/ref/path")
        schemas = Schemas(classes_by_name={class_name: None}, classes_by_reference={root: None, ref_path: None})
        error = PropertyError()

        _propogate_removal(root=root, schemas=schemas, error=error)

        assert schemas.classes_by_name == {class_name: None}
        assert schemas.classes_by_reference == {ref_path: None}
        assert error.detail == f"\n{root}"

    def test_propogate_removal_ref_path_already_removed(self):
        from openapi_python_client.parser.properties import ReferencePath, _propogate_removal
        from openapi_python_client.utils import ClassName

        root = ReferencePath("/root/reference")
        class_name = ClassName("ClassName", "")
        ref_path = ReferencePath("/ref/path")
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


def test_process_model_errors(mocker, model_property_factory):
    from openapi_python_client.parser.properties import _process_model_errors

    propogate_removal = mocker.patch(f"{MODULE_NAME}._propogate_removal")
    model_errors = [
        (model_property_factory(roots={"root1", "root2"}), PropertyError(detail="existing detail")),
        (model_property_factory(roots=set()), PropertyError()),
        (model_property_factory(roots={"root1", "root3"}), PropertyError(detail="other existing detail")),
    ]
    schemas = Schemas()

    result = _process_model_errors(model_errors, schemas=schemas)

    propogate_removal.assert_has_calls(
        [call(root=root, schemas=schemas, error=error) for model, error in model_errors for root in model.roots]
    )
    assert result == [error for _, error in model_errors]
    assert all("\n\nFailure to process schema has resulted in the removal of:" in error.detail for error in result)


class TestBuildParameters:
    def test_skips_references_and_keeps_going(self, mocker, config):
        from openapi_python_client.parser.properties import Parameters, build_parameters
        from openapi_python_client.schema import Parameter, Reference

        parameters = {
            "reference": Reference(ref="#/components/parameters/another_parameter"),
            "defined": Parameter(
                name="page",
                param_in="query",
                required=False,
                style="form",
                explode=True,
                schema=oai.Schema(type="integer", default=0),
            ),
        }

        update_parameters_with_data = mocker.patch(f"{MODULE_NAME}.update_parameters_with_data")
        parse_reference_path = mocker.patch(f"{MODULE_NAME}.parse_reference_path")

        result = build_parameters(components=parameters, parameters=Parameters(), config=config)
        # Should not even try to parse a path for the Reference
        parse_reference_path.assert_called_once_with("#/components/parameters/defined")
        update_parameters_with_data.assert_called_once_with(
            ref_path=parse_reference_path.return_value,
            data=parameters["defined"],
            parameters=Parameters(
                errors=[ParameterError(detail="Reference parameters are not supported.", data=parameters["reference"])]
            ),
            config=config,
        )
        assert result == update_parameters_with_data.return_value

    def test_records_bad_uris_and_keeps_going(self, mocker, config):
        from openapi_python_client.parser.properties import Parameters, build_parameters
        from openapi_python_client.schema import Parameter

        parameters = {"first": Parameter.model_construct(), "second": Parameter.model_construct()}
        update_parameters_with_data = mocker.patch(f"{MODULE_NAME}.update_parameters_with_data")
        parse_reference_path = mocker.patch(
            f"{MODULE_NAME}.parse_reference_path", side_effect=[ParameterError(detail="some details"), "a_path"]
        )

        result = build_parameters(components=parameters, parameters=Parameters(), config=config)
        parse_reference_path.assert_has_calls(
            [
                call("#/components/parameters/first"),
                call("#/components/parameters/second"),
            ]
        )
        update_parameters_with_data.assert_called_once_with(
            ref_path="a_path",
            data=parameters["second"],
            parameters=Parameters(errors=[ParameterError(detail="some details", data=parameters["first"])]),
            config=config,
        )
        assert result == update_parameters_with_data.return_value

    def test_retries_failing_parameters_while_making_progress(self, mocker, config):
        from openapi_python_client.parser.properties import Parameters, build_parameters
        from openapi_python_client.schema import Parameter

        parameters = {"first": Parameter.model_construct(), "second": Parameter.model_construct()}
        update_parameters_with_data = mocker.patch(
            f"{MODULE_NAME}.update_parameters_with_data", side_effect=[ParameterError(), Parameters(), ParameterError()]
        )

        parse_reference_path = mocker.patch(f"{MODULE_NAME}.parse_reference_path")
        result = build_parameters(components=parameters, parameters=Parameters(), config=config)
        parse_reference_path.assert_has_calls(
            [
                call("#/components/parameters/first"),
                call("#/components/parameters/second"),
                call("#/components/parameters/first"),
            ]
        )
        assert update_parameters_with_data.call_count == 3
        assert result.errors == [ParameterError()]


def test_build_schemas(mocker, config):
    from openapi_python_client.parser.properties import Schemas, build_schemas
    from openapi_python_client.schema import Reference, Schema

    create_schemas = mocker.patch(f"{MODULE_NAME}._create_schemas")
    process_models = mocker.patch(f"{MODULE_NAME}._process_models")

    components = {"a_ref": Reference.model_construct(), "a_schema": Schema.model_construct()}
    schemas = Schemas()

    result = build_schemas(components=components, schemas=schemas, config=config)

    create_schemas.assert_called_once_with(components=components, schemas=schemas, config=config)
    process_models.assert_called_once_with(schemas=create_schemas.return_value, config=config)
    assert result == process_models.return_value
