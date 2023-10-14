from typing import Type
from unittest.mock import MagicMock, call

import attr
import pytest

import openapi_python_client.schema as oai
from openapi_python_client import Config
from openapi_python_client.parser.errors import ParameterError, PropertyError, ValidationError
from openapi_python_client.parser.properties import (
    BooleanProperty,
    FloatProperty,
    IntProperty,
    Property,
    Schemas,
    UnionProperty,
)

MODULE_NAME = "openapi_python_client.parser.properties"


class TestStringProperty:
    def test_is_base_type(self, string_property_factory):
        assert string_property_factory().is_base_type is True

    @pytest.mark.parametrize(
        "required, expected",
        (
            (True, "str"),
            (False, "Union[Unset, str]"),
        ),
    )
    def test_get_type_string(self, string_property_factory, required, expected):
        p = string_property_factory(required=required)

        assert p.get_type_string() == expected


class TestDateTimeProperty:
    def test_is_base_type(self, date_time_property_factory):
        assert date_time_property_factory().is_base_type is True

    @pytest.mark.parametrize("required", (True, False))
    def test_get_imports(self, date_time_property_factory, required):
        p = date_time_property_factory(required=required)

        expected = {
            "import datetime",
            "from typing import cast",
            "from dateutil.parser import isoparse",
        }
        if not required:
            expected |= {
                "from typing import Union",
                "from ...types import UNSET, Unset",
            }

        assert p.get_imports(prefix="...") == expected


class TestDateProperty:
    def test_is_base_type(self, date_property_factory):
        assert date_property_factory().is_base_type is True

    @pytest.mark.parametrize("required", (True, False))
    def test_get_imports(self, date_property_factory, required):
        p = date_property_factory(required=required)

        expected = {
            "import datetime",
            "from typing import cast",
            "from dateutil.parser import isoparse",
        }
        if not required:
            expected |= {
                "from typing import Union",
                "from ...types import UNSET, Unset",
            }

        assert p.get_imports(prefix="...") == expected


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


class TestNoneProperty:
    def test_is_base_type(self, none_property_factory):
        assert none_property_factory().is_base_type is True


class TestBooleanProperty:
    def test_is_base_type(self, boolean_property_factory):
        assert boolean_property_factory().is_base_type is True


class TestAnyProperty:
    def test_is_base_type(self, any_property_factory):
        assert any_property_factory().is_base_type is True


class TestIntProperty:
    def test_is_base_type(self, int_property_factory):
        assert int_property_factory().is_base_type is True


class TestListProperty:
    def test_is_base_type(self, list_property_factory):
        assert list_property_factory().is_base_type is False

    @pytest.mark.parametrize("quoted", (True, False))
    def test_get_base_json_type_string_base_inner(self, list_property_factory, quoted):
        p = list_property_factory()
        assert p.get_base_json_type_string(quoted=quoted) == "List[str]"

    @pytest.mark.parametrize("quoted", (True, False))
    def test_get_base_json_type_string_model_inner(self, list_property_factory, model_property_factory, quoted):
        m = model_property_factory()
        p = list_property_factory(inner_property=m)
        assert p.get_base_json_type_string(quoted=quoted) == "List[Dict[str, Any]]"

    def test_get_lazy_import_base_inner(self, list_property_factory):
        p = list_property_factory()
        assert p.get_lazy_imports(prefix="..") == set()

    def test_get_lazy_import_model_inner(self, list_property_factory, model_property_factory):
        m = model_property_factory()
        p = list_property_factory(inner_property=m)
        assert p.get_lazy_imports(prefix="..") == {"from ..models.my_module import MyClass"}

    @pytest.mark.parametrize(
        "required, expected",
        (
            (True, "List[str]"),
            (False, "Union[Unset, List[str]]"),
        ),
    )
    def test_get_type_string_base_inner(self, list_property_factory, required, expected):
        p = list_property_factory(required=required)

        assert p.get_type_string() == expected

    @pytest.mark.parametrize(
        "required, expected",
        (
            (True, "List['MyClass']"),
            (False, "Union[Unset, List['MyClass']]"),
        ),
    )
    def test_get_type_string_model_inner(self, list_property_factory, model_property_factory, required, expected):
        m = model_property_factory()
        p = list_property_factory(required=required, inner_property=m)

        assert p.get_type_string() == expected

    @pytest.mark.parametrize(
        "quoted,expected",
        [
            (False, "List[str]"),
            (True, "List[str]"),
        ],
    )
    def test_get_base_type_string_base_inner(self, list_property_factory, quoted, expected):
        p = list_property_factory()
        assert p.get_base_type_string(quoted=quoted) == expected

    @pytest.mark.parametrize(
        "quoted,expected",
        [
            (False, "List['MyClass']"),
            (True, "List['MyClass']"),
        ],
    )
    def test_get_base_type_string_model_inner(self, list_property_factory, model_property_factory, quoted, expected):
        m = model_property_factory()
        p = list_property_factory(inner_property=m)
        assert p.get_base_type_string(quoted=quoted) == expected

    @pytest.mark.parametrize("required", (True, False))
    def test_get_type_imports(self, list_property_factory, date_time_property_factory, required):
        inner_property = date_time_property_factory()
        p = list_property_factory(inner_property=inner_property, required=required)
        expected = {
            "import datetime",
            "from typing import cast",
            "from dateutil.parser import isoparse",
            "from typing import cast, List",
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


class TestEnumProperty:
    def test_is_base_type(self, enum_property_factory):
        assert enum_property_factory().is_base_type is True

    @pytest.mark.parametrize(
        "required, expected",
        (
            (False, "Union[Unset, {}]"),
            (True, "{}"),
        ),
    )
    def test_get_type_string(self, mocker, enum_property_factory, required, expected):
        fake_class = mocker.MagicMock()
        fake_class.name = "MyTestEnum"

        p = enum_property_factory(class_info=fake_class, required=required)

        assert p.get_type_string() == expected.format(fake_class.name)
        assert p.get_type_string(no_optional=True) == fake_class.name
        assert p.get_type_string(json=True) == expected.format("str")

    def test_get_imports(self, mocker, enum_property_factory):
        fake_class = mocker.MagicMock(module_name="my_test_enum")
        fake_class.name = "MyTestEnum"
        prefix = "..."

        enum_property = enum_property_factory(class_info=fake_class, required=False)

        assert enum_property.get_imports(prefix=prefix) == {
            f"from {prefix}models.{fake_class.module_name} import {fake_class.name}",
            "from typing import Union",  # Makes sure unset is handled via base class
            "from ...types import UNSET, Unset",
        }

    def test_values_from_list(self):
        from openapi_python_client.parser.properties import EnumProperty

        data = ["abc", "123", "a23", "1bc", 4, -3, "a Thing WIth spaces", ""]

        result = EnumProperty.values_from_list(data)

        assert result == {
            "ABC": "abc",
            "VALUE_1": "123",
            "A23": "a23",
            "VALUE_3": "1bc",
            "VALUE_4": 4,
            "VALUE_NEGATIVE_3": -3,
            "A_THING_WITH_SPACES": "a Thing WIth spaces",
            "VALUE_7": "",
        }

    def test_values_from_list_duplicate(self):
        from openapi_python_client.parser.properties import EnumProperty

        data = ["abc", "123", "a23", "abc"]

        with pytest.raises(ValueError):
            EnumProperty.values_from_list(data)


class TestPropertyFromData:
    def test_property_from_data_str_enum(self, enum_property_factory):
        from openapi_python_client.parser.properties import Class, Schemas, property_from_data
        from openapi_python_client.schema import Schema

        existing = enum_property_factory()
        data = Schema(title="AnEnum", enum=["A", "B", "C"], default="B")
        name = "my_enum"
        required = True

        schemas = Schemas(classes_by_name={"AnEnum": existing})

        prop, new_schemas = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=Config()
        )

        assert prop == enum_property_factory(
            name=name,
            required=required,
            values={"A": "A", "B": "B", "C": "C"},
            class_info=Class(name="ParentAnEnum", module_name="parent_an_enum"),
            value_type=str,
            default="ParentAnEnum.B",
        )
        assert schemas != new_schemas, "Provided Schemas was mutated"
        assert new_schemas.classes_by_name == {
            "AnEnum": existing,
            "ParentAnEnum": prop,
        }

    def test_property_from_data_str_enum_with_null(self, enum_property_factory):
        from openapi_python_client.parser.properties import Class, Schemas, property_from_data
        from openapi_python_client.schema import Schema

        existing = enum_property_factory()
        data = Schema(title="AnEnum", enum=["A", "B", "C", None], default="B")
        name = "my_enum"
        required = True

        schemas = Schemas(classes_by_name={"AnEnum": existing})

        prop, new_schemas = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=Config()
        )

        # None / null is removed from enum, and property is now nullable
        assert isinstance(prop, UnionProperty), "Enums with None should be converted to UnionProperties"
        assert prop == enum_property_factory(
            name=name,
            required=required,
            values={"A": "A", "B": "B", "C": "C"},
            class_info=Class(name="ParentAnEnum", module_name="parent_an_enum"),
            value_type=str,
            default="ParentAnEnum.B",
        )
        assert schemas != new_schemas, "Provided Schemas was mutated"
        assert new_schemas.classes_by_name == {
            "AnEnum": existing,
            "ParentAnEnum": prop,
        }

    def test_property_from_data_null_enum(self, enum_property_factory, none_property_factory):
        from openapi_python_client.parser.properties import Schemas, property_from_data
        from openapi_python_client.schema import Schema

        data = Schema(title="AnEnumWithOnlyNull", enum=[None], default=None)
        name = "my_enum"
        required = True

        schemas = Schemas()

        prop, new_schemas = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=Config()
        )

        assert prop == none_property_factory(name="my_enum", required=required, default="None")

    def test_property_from_data_int_enum(self, enum_property_factory):
        from openapi_python_client.parser.properties import Class, Schemas, property_from_data
        from openapi_python_client.schema import Schema

        name = "my_enum"
        required = True
        data = Schema.model_construct(title="anEnum", enum=[1, 2, 3], default=3)

        existing = enum_property_factory()
        schemas = Schemas(classes_by_name={"AnEnum": existing})

        prop, new_schemas = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=Config()
        )

        assert prop == enum_property_factory(
            name=name,
            required=required,
            values={"VALUE_1": 1, "VALUE_2": 2, "VALUE_3": 3},
            class_info=Class(name="ParentAnEnum", module_name="parent_an_enum"),
            value_type=int,
            default="ParentAnEnum.VALUE_3",
        )
        assert schemas != new_schemas, "Provided Schemas was mutated"
        assert new_schemas.classes_by_name == {
            "AnEnum": existing,
            "ParentAnEnum": prop,
        }

    def test_property_from_data_ref_enum(self, enum_property_factory):
        from openapi_python_client.parser.properties import Class, Schemas, property_from_data

        name = "some_enum"
        data = oai.Reference.model_construct(ref="#/components/schemas/MyEnum")
        existing_enum = enum_property_factory(
            name="an_enum",
            required=False,
            values={"A": "a"},
            class_info=Class(name="MyEnum", module_name="my_enum"),
        )
        schemas = Schemas(classes_by_reference={"/components/schemas/MyEnum": existing_enum})

        prop, new_schemas = property_from_data(
            name=name, required=False, data=data, schemas=schemas, parent_name="", config=Config()
        )

        assert prop == enum_property_factory(
            name="some_enum",
            required=False,
            values={"A": "a"},
            class_info=Class(name="MyEnum", module_name="my_enum"),
        )
        assert schemas == new_schemas

    def test_property_from_data_ref_enum_with_overridden_default(self, enum_property_factory):
        from openapi_python_client.parser.properties import Class, Schemas, property_from_data

        name = "some_enum"
        required = False
        data = oai.Schema.model_construct(
            default="b", allOf=[oai.Reference.model_construct(ref="#/components/schemas/MyEnum")]
        )
        existing_enum = enum_property_factory(
            name="an_enum",
            default="MyEnum.A",
            required=required,
            values={"A": "a", "B": "b"},
            class_info=Class(name="MyEnum", module_name="my_enum"),
        )
        schemas = Schemas(classes_by_reference={"/components/schemas/MyEnum": existing_enum})

        prop, new_schemas = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="", config=Config()
        )

        assert prop == enum_property_factory(
            name="some_enum",
            default="MyEnum.B",
            required=required,
            values={"A": "a", "B": "b"},
            class_info=Class(name="MyEnum", module_name="my_enum"),
        )
        assert schemas == new_schemas

    def test_property_from_data_ref_enum_with_invalid_default(self, enum_property_factory):
        from openapi_python_client.parser.properties import Class, Schemas, property_from_data

        name = "some_enum"
        data = oai.Schema.model_construct(
            default="x", allOf=[oai.Reference.model_construct(ref="#/components/schemas/MyEnum")]
        )
        existing_enum = enum_property_factory(
            name="an_enum",
            default="MyEnum.A",
            values={"A": "a", "B": "b"},
            class_info=Class(name="MyEnum", module_name="my_enum"),
            python_name="an_enum",
        )
        schemas = Schemas(classes_by_reference={"/components/schemas/MyEnum": existing_enum})

        prop, new_schemas = property_from_data(
            name=name, required=False, data=data, schemas=schemas, parent_name="", config=Config()
        )

        assert schemas == new_schemas
        assert prop == PropertyError(data=data, detail="x is an invalid default for enum MyEnum")

    def test_property_from_data_ref_model(self, model_property_factory):
        from openapi_python_client.parser.properties import Class, Schemas, property_from_data

        name = "new_name"
        required = False
        class_name = "MyModel"
        data = oai.Reference.model_construct(ref=f"#/components/schemas/{class_name}")
        class_info = Class(name=class_name, module_name="my_model")

        existing_model = model_property_factory(
            name="old_name",
            class_info=class_info,
        )
        schemas = Schemas(classes_by_reference={f"/components/schemas/{class_name}": existing_model})

        prop, new_schemas = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="", config=Config()
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
    def test_property_from_data_ref(self, property_factory, references_exist):
        from openapi_python_client.parser.properties import Schemas, property_from_data

        name = "new_name"
        required = False
        ref_path = "/components/schemas/RefName"
        data = oai.Reference.model_construct(ref=f"#{ref_path}")
        roots = {"new_root"}

        existing_property = property_factory(name="old_name")
        references = {ref_path: {"old_root"}} if references_exist else {}
        schemas = Schemas(classes_by_reference={ref_path: existing_property}, dependencies=references)

        prop, new_schemas = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="", config=Config(), roots=roots
        )

        assert prop == property_factory(name=name, required=required)
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

    @pytest.mark.parametrize(
        "openapi_type,prop_type,python_type",
        [
            ("number", FloatProperty, float),
            ("integer", IntProperty, int),
            ("boolean", BooleanProperty, bool),
        ],
    )
    def test_property_from_data_simple_types(self, openapi_type: str, prop_type: Type[Property], python_type):
        from openapi_python_client.parser.properties import Schemas, property_from_data

        name = "test_prop"
        required = True
        description = "a description"
        example = "an example"
        data = oai.Schema.model_construct(type=openapi_type, default=1, description=description, example=example)
        schemas = Schemas()

        p, new_schemas = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=MagicMock()
        )

        assert p == prop_type(
            name=name,
            required=required,
            default=python_type(data.default),
            python_name=name,
            description=description,
            example=example,
        )
        assert new_schemas == schemas

        # Test nullable values
        data.default = 0

        p, _ = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=MagicMock()
        )
        assert p == prop_type(
            name=name,
            required=required,
            default=python_type(data.default),
            python_name=name,
            description=description,
            example=example,
        )

        # Test bad default value
        data.default = "a"
        p, _ = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=MagicMock()
        )
        assert python_type is bool or isinstance(p, PropertyError)

    def test_property_from_data_array(self, mocker):
        from openapi_python_client.parser.properties import Schemas, property_from_data

        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema(
            type="array",
            items={"type": "number", "default": "0.0"},
        )
        build_list_property = mocker.patch(f"{MODULE_NAME}.build_list_property")
        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=name)
        schemas = Schemas()
        config = MagicMock()
        roots = {"root"}
        process_properties = False

        response = property_from_data(
            name=name,
            required=required,
            data=data,
            schemas=schemas,
            parent_name="parent",
            config=config,
            roots=roots,
            process_properties=process_properties,
        )

        assert response == build_list_property.return_value
        build_list_property.assert_called_once_with(
            data=data,
            name=name,
            required=required,
            schemas=schemas,
            parent_name="parent",
            config=config,
            process_properties=process_properties,
            roots=roots,
        )

    def test_property_from_data_object(self, mocker):
        from openapi_python_client.parser.properties import Schemas, property_from_data

        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema(
            type="object",
        )
        build_model_property = mocker.patch(f"{MODULE_NAME}.build_model_property")
        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=name)
        schemas = Schemas()
        config = MagicMock()
        roots = {"root"}
        process_properties = False

        response = property_from_data(
            name=name,
            required=required,
            data=data,
            schemas=schemas,
            parent_name="parent",
            config=config,
            process_properties=process_properties,
            roots=roots,
        )

        assert response == build_model_property.return_value
        build_model_property.assert_called_once_with(
            data=data,
            name=name,
            required=required,
            schemas=schemas,
            parent_name="parent",
            config=config,
            process_properties=process_properties,
            roots=roots,
        )

    def test_property_from_data_union(self, mocker):
        from openapi_python_client.parser.properties import Schemas, property_from_data

        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema.model_construct(
            anyOf=[{"type": "number", "default": "0.0"}],
            oneOf=[
                {"type": "integer", "default": "0"},
            ],
        )
        build_union_property = mocker.patch(f"{MODULE_NAME}.build_union_property")
        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=name)
        schemas = Schemas()
        config = MagicMock()

        response = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=config
        )

        assert response == build_union_property.return_value
        build_union_property.assert_called_once_with(
            data=data, name=name, required=required, schemas=schemas, parent_name="parent", config=config
        )

    def test_property_from_data_union_of_one_element(self, mocker, model_property_factory):
        from openapi_python_client.parser.properties import Schemas, property_from_data

        name = "new_name"
        required = False
        class_name = "MyModel"
        existing_model = model_property_factory()
        schemas = Schemas(classes_by_reference={f"/{class_name}": existing_model})

        data = oai.Schema.model_construct(
            allOf=[oai.Reference.model_construct(ref=f"#/{class_name}")],
        )
        build_union_property = mocker.patch(f"{MODULE_NAME}.build_union_property")

        prop, schemas = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=Config()
        )

        assert prop == attr.evolve(existing_model, name=name, required=required, python_name=name)
        build_union_property.assert_not_called()

    def test_property_from_data_no_valid_props_in_data(self, any_property_factory):
        from openapi_python_client.parser.properties import Schemas, property_from_data

        schemas = Schemas()
        data = oai.Schema()
        name = "blah"

        prop, new_schemas = property_from_data(
            name=name, required=True, data=data, schemas=schemas, parent_name="parent", config=MagicMock()
        )

        assert prop == any_property_factory(name=name, required=True, default=None)
        assert new_schemas == schemas

    def test_property_from_data_validation_error(self, mocker):
        from openapi_python_client.parser.errors import PropertyError
        from openapi_python_client.parser.properties import Schemas, property_from_data

        mocker.patch(f"{MODULE_NAME}._property_from_data").side_effect = ValidationError()
        schemas = Schemas()

        data = oai.Schema()
        err, new_schemas = property_from_data(
            name="blah", required=True, data=data, schemas=schemas, parent_name="parent", config=MagicMock()
        )
        assert err == PropertyError(detail="Failed to validate default value", data=data)
        assert new_schemas == schemas


class TestBuildListProperty:
    def test_build_list_property_no_items(self, mocker):
        from openapi_python_client.parser import properties

        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema.model_construct(type="array")
        property_from_data = mocker.patch.object(properties, "property_from_data")
        schemas = properties.Schemas()

        p, new_schemas = properties.build_list_property(
            name=name,
            required=required,
            data=data,
            schemas=schemas,
            parent_name="parent",
            config=MagicMock(),
            process_properties=True,
            roots={"root"},
        )

        assert p == PropertyError(data=data, detail="type array must have items defined")
        assert new_schemas == schemas
        property_from_data.assert_not_called()

    def test_build_list_property_invalid_items(self, mocker):
        from openapi_python_client.parser import properties

        name = "name"
        required = mocker.MagicMock()
        data = oai.Schema(
            type="array",
            items={},
        )
        schemas = properties.Schemas()
        second_schemas = properties.Schemas(errors=["error"])
        property_from_data = mocker.patch.object(
            properties, "property_from_data", return_value=(properties.PropertyError(data="blah"), second_schemas)
        )
        config = MagicMock()
        process_properties = False
        roots = {"root"}

        p, new_schemas = properties.build_list_property(
            name=name,
            required=required,
            data=data,
            schemas=schemas,
            parent_name="parent",
            config=config,
            roots=roots,
            process_properties=process_properties,
        )

        assert isinstance(p, PropertyError)
        assert p.data == "blah"
        assert p.header.startswith(f"invalid data in items of array {name}")
        assert new_schemas == second_schemas
        assert schemas != new_schemas, "Schema was mutated"
        property_from_data.assert_called_once_with(
            name=f"{name}_item",
            required=True,
            data=data.items,
            schemas=schemas,
            parent_name="parent",
            config=config,
            process_properties=process_properties,
            roots=roots,
        )

    def test_build_list_property(self, any_property_factory):
        from openapi_python_client.parser import properties

        name = "prop"
        data = oai.Schema(
            type="array",
            items={},
        )
        schemas = properties.Schemas(errors=["error"])
        config = Config()

        p, new_schemas = properties.build_list_property(
            name=name,
            required=True,
            data=data,
            schemas=schemas,
            parent_name="parent",
            config=config,
            roots={"root"},
            process_properties=True,
        )

        assert isinstance(p, properties.ListProperty)
        assert p.inner_property == any_property_factory(name=f"{name}_item")
        assert new_schemas == schemas


class TestBuildUnionProperty:
    def test_property_from_data_union(
        self, union_property_factory, date_time_property_factory, string_property_factory
    ):
        from openapi_python_client.parser.properties import Schemas, property_from_data

        name = "union_prop"
        required = True
        data = oai.Schema(
            anyOf=[{"type": "string", "default": "a"}],
            oneOf=[
                {"type": "string", "format": "date-time"},
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
            name=name, required=required, data=data, schemas=Schemas(), parent_name="parent", config=MagicMock()
        )

        assert p == expected
        assert s == Schemas()

    def test_build_union_property_invalid_property(self, mocker):
        name = "bad_union"
        required = mocker.MagicMock()
        reference = oai.Reference.model_construct(ref="#/components/schema/NotExist")
        data = oai.Schema(anyOf=[reference])
        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=name)

        from openapi_python_client.parser.properties import Schemas, build_union_property

        p, s = build_union_property(
            name=name, required=required, data=data, schemas=Schemas(), parent_name="parent", config=MagicMock()
        )
        assert p == PropertyError(detail=f"Invalid property in union {name}", data=reference)


class TestStringBasedProperty:
    @pytest.mark.parametrize("required", (True, False))
    def test_no_format(self, string_property_factory, required):
        from openapi_python_client.parser.properties import property_from_data

        name = "some_prop"
        data = oai.Schema.model_construct(type="string", default='"hello world"', pattern="abcdef")

        p, _ = property_from_data(
            name=name, required=required, data=data, parent_name=None, config=Config(), schemas=Schemas()
        )

        assert p == string_property_factory(
            name=name, required=required, default="'\\\\\"hello world\\\\\"'", pattern=data.pattern
        )

    def test_datetime_format(self, date_time_property_factory):
        from openapi_python_client.parser.properties import property_from_data

        name = "datetime_prop"
        required = True
        data = oai.Schema.model_construct(type="string", schema_format="date-time", default="2020-11-06T12:00:00")

        p, _ = property_from_data(
            name=name, required=required, data=data, schemas=Schemas(), config=Config(), parent_name=None
        )

        assert p == date_time_property_factory(name=name, required=required, default=f"isoparse('{data.default}')")

    def test_datetime_bad_default(self):
        from openapi_python_client.parser.properties import property_from_data

        name = "datetime_prop"
        required = True
        data = oai.Schema.model_construct(type="string", schema_format="date-time", default="a")

        result, _ = property_from_data(
            name=name, required=required, data=data, schemas=Schemas(), config=Config(), parent_name=None
        )

        assert result == PropertyError(detail="Failed to validate default value", data=data)

    def test_date_format(self, date_property_factory):
        from openapi_python_client.parser.properties import property_from_data

        name = "date_prop"
        required = True

        data = oai.Schema.model_construct(type="string", schema_format="date", default="2020-11-06")

        p, _ = property_from_data(
            name=name, required=required, data=data, schemas=Schemas(), config=Config(), parent_name=None
        )

        assert p == date_property_factory(name=name, required=required, default=f"isoparse('{data.default}').date()")

    def test_date_format_bad_default(self):
        from openapi_python_client.parser.properties import property_from_data

        name = "date_prop"
        required = True

        data = oai.Schema.model_construct(type="string", schema_format="date", default="a")

        p, _ = property_from_data(
            name=name, required=required, data=data, schemas=Schemas(), config=Config(), parent_name=None
        )

        assert p == PropertyError(detail="Failed to validate default value", data=data)

    def test__string_based_property_binary_format(self, file_property_factory):
        from openapi_python_client.parser.properties import property_from_data

        name = "file_prop"
        required = True
        data = oai.Schema.model_construct(type="string", schema_format="binary", default="a")

        p, _ = property_from_data(
            name=name, required=required, data=data, schemas=Schemas(), config=Config(), parent_name=None
        )
        assert p == file_property_factory(name=name, required=required)

    def test__string_based_property_unsupported_format(self, string_property_factory):
        from openapi_python_client.parser.properties import property_from_data

        name = "unknown"
        required = True
        data = oai.Schema.model_construct(type="string", schema_format="blah")

        p, _ = property_from_data(
            name=name, required=required, data=data, schemas=Schemas, config=Config(), parent_name=None
        )

        assert p == string_property_factory(name=name, required=required)


class TestCreateSchemas:
    def test_skips_references_and_keeps_going(self, mocker):
        from openapi_python_client.parser.properties import Schemas, _create_schemas
        from openapi_python_client.schema import Reference, Schema

        components = {"a_ref": Reference.model_construct(), "a_schema": Schema.model_construct()}
        update_schemas_with_data = mocker.patch(f"{MODULE_NAME}.update_schemas_with_data")
        parse_reference_path = mocker.patch(f"{MODULE_NAME}.parse_reference_path")
        config = Config()
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

    def test_records_bad_uris_and_keeps_going(self, mocker):
        from openapi_python_client.parser.properties import Schemas, _create_schemas
        from openapi_python_client.schema import Schema

        components = {"first": Schema.model_construct(), "second": Schema.model_construct()}
        update_schemas_with_data = mocker.patch(f"{MODULE_NAME}.update_schemas_with_data")
        parse_reference_path = mocker.patch(
            f"{MODULE_NAME}.parse_reference_path", side_effect=[PropertyError(detail="some details"), "a_path"]
        )
        config = Config()
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

    def test_retries_failing_properties_while_making_progress(self, mocker):
        from openapi_python_client.parser.properties import Schemas, _create_schemas
        from openapi_python_client.schema import Schema

        components = {"first": Schema.model_construct(), "second": Schema.model_construct()}
        update_schemas_with_data = mocker.patch(
            f"{MODULE_NAME}.update_schemas_with_data", side_effect=[PropertyError(), Schemas(), PropertyError()]
        )
        parse_reference_path = mocker.patch(f"{MODULE_NAME}.parse_reference_path")
        config = Config()
        schemas = Schemas()

        result = _create_schemas(components=components, schemas=schemas, config=config)
        parse_reference_path.assert_has_calls(
            [
                call("#/components/schemas/first"),
                call("#/components/schemas/second"),
                call("#/components/schemas/first"),
            ]
        )
        assert update_schemas_with_data.call_count == 3  # noqa: PLR2004
        assert result.errors == [PropertyError()]


class TestProcessModels:
    def test_retries_failing_models_while_making_progress(self, mocker, model_property_factory, property_factory):
        from openapi_python_client.parser.properties import _process_models

        first_model = model_property_factory()
        schemas = Schemas(
            classes_by_name={
                "first": first_model,
                "second": model_property_factory(),
                "non-model": property_factory(),
            }
        )
        process_model = mocker.patch(
            f"{MODULE_NAME}.process_model", side_effect=[PropertyError(), Schemas(), PropertyError()]
        )
        process_model_errors = mocker.patch(f"{MODULE_NAME}._process_model_errors", return_value=["error"])
        config = Config()

        result = _process_models(schemas=schemas, config=config)

        process_model.assert_has_calls(
            [
                call(first_model, schemas=schemas, config=config),
                call(schemas.classes_by_name["second"], schemas=schemas, config=config),
                call(first_model, schemas=result, config=config),
            ]
        )
        assert process_model_errors.was_called_once_with([(first_model, PropertyError())])
        assert all(error in result.errors for error in process_model_errors.return_value)

    def test_detect_recursive_allof_reference_no_retry(self, mocker, model_property_factory):
        from openapi_python_client.parser.properties import Class, _process_models
        from openapi_python_client.schema import Reference

        class_name = "class_name"
        recursive_model = model_property_factory(class_info=Class(name=class_name, module_name="module_name"))
        schemas = Schemas(
            classes_by_name={
                "recursive": recursive_model,
                "second": model_property_factory(),
            }
        )
        recursion_error = PropertyError(data=Reference.model_construct(ref=f"#/{class_name}"))
        process_model = mocker.patch(f"{MODULE_NAME}.process_model", side_effect=[recursion_error, Schemas()])
        process_model_errors = mocker.patch(f"{MODULE_NAME}._process_model_errors", return_value=["error"])
        config = Config()

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
    def test_skips_references_and_keeps_going(self, mocker):
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

        config = Config()
        result = build_parameters(components=parameters, parameters=Parameters(), config=Config())
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

    def test_records_bad_uris_and_keeps_going(self, mocker):
        from openapi_python_client.parser.properties import Parameters, build_parameters
        from openapi_python_client.schema import Parameter

        parameters = {"first": Parameter.model_construct(), "second": Parameter.model_construct()}
        update_parameters_with_data = mocker.patch(f"{MODULE_NAME}.update_parameters_with_data")
        parse_reference_path = mocker.patch(
            f"{MODULE_NAME}.parse_reference_path", side_effect=[ParameterError(detail="some details"), "a_path"]
        )

        config = Config()
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

    def test_retries_failing_parameters_while_making_progress(self, mocker):
        from openapi_python_client.parser.properties import Parameters, build_parameters
        from openapi_python_client.schema import Parameter

        parameters = {"first": Parameter.model_construct(), "second": Parameter.model_construct()}
        update_parameters_with_data = mocker.patch(
            f"{MODULE_NAME}.update_parameters_with_data", side_effect=[ParameterError(), Parameters(), ParameterError()]
        )

        parse_reference_path = mocker.patch(f"{MODULE_NAME}.parse_reference_path")
        config = Config()
        result = build_parameters(components=parameters, parameters=Parameters(), config=config)
        parse_reference_path.assert_has_calls(
            [
                call("#/components/parameters/first"),
                call("#/components/parameters/second"),
                call("#/components/parameters/first"),
            ]
        )
        assert update_parameters_with_data.call_count == 3  # noqa: PLR2004
        assert result.errors == [ParameterError()]


def test_build_enum_property_conflict():
    from openapi_python_client.parser.properties import Schemas, build_enum_property

    data = oai.Schema()
    schemas = Schemas()

    _, schemas = build_enum_property(
        data=data, name="Existing", required=True, schemas=schemas, enum=["a"], parent_name=None, config=Config()
    )
    err, new_schemas = build_enum_property(
        data=data,
        name="Existing",
        required=True,
        schemas=schemas,
        enum=["a", "b"],
        parent_name=None,
        config=Config(),
    )

    assert schemas == new_schemas
    assert err == PropertyError(detail="Found conflicting enums named Existing with incompatible values.", data=data)


def test_build_enum_property_no_values():
    from openapi_python_client.parser.properties import Schemas, build_enum_property

    data = oai.Schema()
    schemas = Schemas()

    err, new_schemas = build_enum_property(
        data=data, name="Existing", required=True, schemas=schemas, enum=[], parent_name=None, config=Config()
    )

    assert schemas == new_schemas
    assert err == PropertyError(detail="No values provided for Enum", data=data)


def test_build_enum_property_bad_default():
    from openapi_python_client.parser.properties import Schemas, build_enum_property

    data = oai.Schema(default="B")
    schemas = Schemas()

    err, new_schemas = build_enum_property(
        data=data, name="Existing", required=True, schemas=schemas, enum=["A"], parent_name=None, config=Config()
    )

    assert schemas == new_schemas
    assert err == PropertyError(detail="B is an invalid default for enum Existing", data=data)


def test_build_schemas(mocker):
    from openapi_python_client.parser.properties import Schemas, build_schemas
    from openapi_python_client.schema import Reference, Schema

    create_schemas = mocker.patch(f"{MODULE_NAME}._create_schemas")
    process_models = mocker.patch(f"{MODULE_NAME}._process_models")

    components = {"a_ref": Reference.model_construct(), "a_schema": Schema.model_construct()}
    schemas = Schemas()
    config = Config()

    result = build_schemas(components=components, schemas=schemas, config=config)

    create_schemas.assert_called_once_with(components=components, schemas=schemas, config=config)
    process_models.assert_called_once_with(schemas=create_schemas.return_value, config=config)
    assert result == process_models.return_value
