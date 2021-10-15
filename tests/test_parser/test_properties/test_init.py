from unittest.mock import MagicMock, call

import attr
import pytest

import openapi_python_client.schema as oai
from openapi_python_client import Config
from openapi_python_client.parser.errors import PropertyError, ValidationError
from openapi_python_client.parser.properties import BooleanProperty, FloatProperty, IntProperty, Schemas

MODULE_NAME = "openapi_python_client.parser.properties"


class TestStringProperty:
    @pytest.mark.parametrize(
        "required, nullable, expected",
        (
            (True, False, "str"),
            (True, True, "Optional[str]"),
            (False, True, "Union[Unset, None, str]"),
            (False, False, "Union[Unset, str]"),
        ),
    )
    def test_get_type_string(self, string_property_factory, required, nullable, expected):
        p = string_property_factory(required=required, nullable=nullable)

        assert p.get_type_string() == expected


class TestDateTimeProperty:
    @pytest.mark.parametrize("required", (True, False))
    @pytest.mark.parametrize("nullable", (True, False))
    def test_get_imports(self, date_time_property_factory, required, nullable):
        p = date_time_property_factory(required=required, nullable=nullable)

        expected = {
            "import datetime",
            "from typing import cast",
            "from dateutil.parser import isoparse",
        }
        if nullable:
            expected.add("from typing import Optional")
        if not required:
            expected |= {
                "from typing import Union",
                "from ...types import UNSET, Unset",
            }

        assert p.get_imports(prefix="...") == expected


class TestDateProperty:
    @pytest.mark.parametrize("required", (True, False))
    @pytest.mark.parametrize("nullable", (True, False))
    def test_get_imports(self, date_property_factory, required, nullable):
        p = date_property_factory(required=required, nullable=nullable)

        expected = {
            "import datetime",
            "from typing import cast",
            "from dateutil.parser import isoparse",
        }
        if nullable:
            expected.add("from typing import Optional")
        if not required:
            expected |= {
                "from typing import Union",
                "from ...types import UNSET, Unset",
            }

        assert p.get_imports(prefix="...") == expected


class TestFileProperty:
    @pytest.mark.parametrize("required", (True, False))
    @pytest.mark.parametrize("nullable", (True, False))
    def test_get_imports(self, file_property_factory, required, nullable):
        p = file_property_factory(required=required, nullable=nullable)

        expected = {
            "from io import BytesIO",
            "from ...types import File, FileJsonType",
        }
        if nullable:
            expected.add("from typing import Optional")
        if not required:
            expected |= {
                "from typing import Union",
                "from ...types import UNSET, Unset",
            }

        assert p.get_imports(prefix="...") == expected


class TestListProperty:
    @pytest.mark.parametrize(
        "required, nullable, expected",
        (
            (True, False, "List[str]"),
            (True, True, "Optional[List[str]]"),
            (False, False, "Union[Unset, List[str]]"),
            (False, True, "Union[Unset, None, List[str]]"),
        ),
    )
    def test_get_type_string(self, list_property_factory, required, nullable, expected):
        p = list_property_factory(required=required, nullable=nullable)

        assert p.get_type_string() == expected

    @pytest.mark.parametrize("required", (True, False))
    @pytest.mark.parametrize("nullable", (True, False))
    def test_get_type_imports(self, list_property_factory, date_time_property_factory, required, nullable):
        inner_property = date_time_property_factory()
        p = list_property_factory(inner_property=inner_property, required=required, nullable=nullable)
        expected = {
            "import datetime",
            "from typing import cast",
            "from dateutil.parser import isoparse",
            "from typing import cast, List",
        }
        if nullable:
            expected.add("from typing import Optional")
        if not required:
            expected |= {
                "from typing import Union",
                "from ...types import UNSET, Unset",
            }

        assert p.get_imports(prefix="...") == expected


class TestUnionProperty:
    @pytest.mark.parametrize(
        "nullable,required,no_optional,json,expected",
        [
            (False, False, False, False, "Union[Unset, datetime.datetime, str]"),
            (False, False, True, False, "Union[datetime.datetime, str]"),
            (False, True, False, False, "Union[datetime.datetime, str]"),
            (False, True, True, False, "Union[datetime.datetime, str]"),
            (True, False, False, False, "Union[None, Unset, datetime.datetime, str]"),
            (True, False, True, False, "Union[datetime.datetime, str]"),
            (True, True, False, False, "Union[None, datetime.datetime, str]"),
            (True, True, True, False, "Union[datetime.datetime, str]"),
            (False, False, False, True, "Union[Unset, str]"),
            (False, False, True, True, "str"),
            (False, True, False, True, "str"),
            (False, True, True, True, "str"),
            (True, False, False, True, "Union[None, Unset, str]"),
            (True, False, True, True, "str"),
            (True, True, False, True, "Union[None, str]"),
            (True, True, True, True, "str"),
        ],
    )
    def test_get_type_string(
        self,
        union_property_factory,
        date_time_property_factory,
        string_property_factory,
        nullable,
        required,
        no_optional,
        json,
        expected,
    ):
        p = union_property_factory(
            required=required,
            nullable=nullable,
            inner_properties=[date_time_property_factory(), string_property_factory()],
        )

        assert p.get_base_type_string() == "Union[datetime.datetime, str]"

        assert p.get_type_string(no_optional=no_optional, json=json) == expected

    def test_get_base_type_string(self, union_property_factory, date_time_property_factory, string_property_factory):
        p = union_property_factory(inner_properties=[date_time_property_factory(), string_property_factory()])

        assert p.get_base_type_string() == "Union[datetime.datetime, str]"

    def test_get_base_type_string_one_element(self, union_property_factory, date_time_property_factory):
        p = union_property_factory(
            inner_properties=[date_time_property_factory()],
        )

        assert p.get_base_type_string() == "datetime.datetime"

    def test_get_base_json_type_string(self, union_property_factory, date_time_property_factory):
        p = union_property_factory(
            inner_properties=[date_time_property_factory()],
        )

        assert p.get_base_json_type_string() == "str"

    @pytest.mark.parametrize("required", (True, False))
    @pytest.mark.parametrize("nullable", (True, False))
    def test_get_type_imports(self, union_property_factory, date_time_property_factory, required, nullable):
        p = union_property_factory(
            inner_properties=[date_time_property_factory()], required=required, nullable=nullable
        )
        expected = {
            "import datetime",
            "from typing import cast",
            "from dateutil.parser import isoparse",
            "from typing import cast, Union",
        }
        if nullable:
            expected.add("from typing import Optional")
        if not required:
            expected |= {
                "from typing import Union",
                "from ...types import UNSET, Unset",
            }

        assert p.get_imports(prefix="...") == expected


class TestEnumProperty:
    @pytest.mark.parametrize(
        "required, nullable, expected",
        (
            (False, False, "Union[Unset, {}]"),
            (True, False, "{}"),
            (False, True, "Union[Unset, None, {}]"),
            (True, True, "Optional[{}]"),
            (True, False, "Optional[{}]"),
            (True, False, "{}"),
        ),
    )
    def test_get_type_string(self, mocker, enum_property_factory, required, nullable, expected):
        fake_class = mocker.MagicMock()
        fake_class.name = "MyTestEnum"

        p = enum_property_factory(class_info=fake_class, required=required, nullable=nullable)

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

    def test_values_from_list_with_null(self):
        from openapi_python_client.parser.properties import EnumProperty

        data = ["abc", "123", "a23", "1bc", 4, -3, "a Thing WIth spaces", "", "null"]

        result = EnumProperty.values_from_list(data)

        # None / null is removed from result, and result is now Optional[{}]
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

    def test_values_from_list_with_only_null(self):
        from openapi_python_client.parser.properties import EnumProperty

        data = ["null"]

        result = EnumProperty.values_from_list(data)

        # None / null is not removed from result since it's the only value
        assert result == {
            "VALUE_0": None,
        }


class TestPropertyFromData:
    def test_property_from_data_str_enum(self, enum_property_factory):
        from openapi_python_client.parser.properties import Class, Schemas, property_from_data
        from openapi_python_client.schema import Schema

        existing = enum_property_factory()
        data = Schema(title="AnEnum", enum=["A", "B", "C"], nullable=False, default="B")
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
        data = Schema(title="AnEnumWithNull", enum=["A", "B", "C", "null"], nullable=False, default="B")
        name = "my_enum"
        required = True

        schemas = Schemas(classes_by_name={"AnEnum": existing})

        prop, new_schemas = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=Config()
        )

        # None / null is removed from enum, and property is now nullable
        assert prop == enum_property_factory(
            name=name,
            required=required,
            values={"A": "A", "B": "B", "C": "C"},
            class_info=Class(name="ParentAnEnum", module_name="parent_an_enum"),
            value_type=str,
            default="ParentAnEnum.B",
        )
        assert prop.nullable is True
        assert schemas != new_schemas, "Provided Schemas was mutated"
        assert new_schemas.classes_by_name == {
            "AnEnumWithNull": existing,
            "ParentAnEnum": prop,
        }

    def test_property_from_data_null_enum(self, enum_property_factory):
        from openapi_python_client.parser.properties import Class, Schemas, property_from_data
        from openapi_python_client.schema import Schema

        existing = enum_property_factory()
        data = Schema(title="AnEnumWithOnlyNull", enum=["null"], nullable=False, default=None)
        name = "my_enum"
        required = True

        schemas = Schemas(classes_by_name={"AnEnum": existing})

        prop, new_schemas = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=Config()
        )

        assert prop == enum_property_factory(
            name=name,
            required=required,
            values={"VALUE_0": None},
            class_info=Class(name="ParentAnEnum", module_name="parent_an_enum"),
            value_type=type(None),
            default=None,
        )
        assert prop.nullable is False
        assert schemas != new_schemas, "Provided Schemas was mutated"
        assert new_schemas.classes_by_name == {
            "AnEnumWithOnlyNull": existing,
            "ParentAnEnum": prop,
        }

    def test_property_from_data_int_enum(self, enum_property_factory):
        from openapi_python_client.parser.properties import Class, EnumProperty, Schemas, property_from_data
        from openapi_python_client.schema import Schema

        name = "my_enum"
        required = True
        nullable = False
        data = Schema.construct(title="anEnum", enum=[1, 2, 3], nullable=nullable, default=3)

        existing = enum_property_factory()
        schemas = Schemas(classes_by_name={"AnEnum": existing})

        prop, new_schemas = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=Config()
        )

        assert prop == enum_property_factory(
            name=name,
            required=required,
            nullable=nullable,
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
        data = oai.Reference.construct(ref="#/components/schemas/MyEnum")
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
        data = oai.Schema.construct(default="b", allOf=[oai.Reference.construct(ref="#/components/schemas/MyEnum")])
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
        data = oai.Schema.construct(default="x", allOf=[oai.Reference.construct(ref="#/components/schemas/MyEnum")])
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
        from openapi_python_client.parser.properties import Class, ModelProperty, Schemas, property_from_data

        name = "new_name"
        required = False
        class_name = "MyModel"
        data = oai.Reference.construct(ref=f"#/components/schemas/{class_name}")
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

        data = oai.Reference.construct(ref="a/b/c")
        parse_reference_path = mocker.patch(f"{MODULE_NAME}.parse_reference_path")
        schemas = Schemas()

        prop, new_schemas = property_from_data(
            name="a_prop", required=False, data=data, schemas=schemas, parent_name="parent", config=mocker.MagicMock()
        )

        parse_reference_path.assert_called_once_with(data.ref)
        assert prop == PropertyError(data=data, detail="Could not find reference in parsed models or enums")
        assert schemas == new_schemas

    def test_property_from_data_invalid_ref(self, mocker):
        from openapi_python_client.parser.properties import PropertyError, Schemas, property_from_data

        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Reference.construct(ref=mocker.MagicMock())
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
    def test_property_from_data_simple_types(self, openapi_type, prop_type, python_type):
        from openapi_python_client.parser.properties import Schemas, property_from_data

        name = "test_prop"
        required = True
        data = oai.Schema.construct(type=openapi_type, default=1)
        schemas = Schemas()

        p, new_schemas = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=MagicMock()
        )

        assert p == prop_type(
            name=name, required=required, default=python_type(data.default), nullable=False, python_name=name
        )
        assert new_schemas == schemas

        # Test nullable values
        data.default = 0
        data.nullable = True

        p, _ = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=MagicMock()
        )
        assert p == prop_type(
            name=name, required=required, default=python_type(data.default), nullable=True, python_name=name
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

        response = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=config
        )

        assert response == build_list_property.return_value
        build_list_property.assert_called_once_with(
            data=data, name=name, required=required, schemas=schemas, parent_name="parent", config=config
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

        response = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=config
        )

        assert response == build_model_property.return_value
        build_model_property.assert_called_once_with(
            data=data, name=name, required=required, schemas=schemas, parent_name="parent", config=config
        )

    def test_property_from_data_union(self, mocker):
        from openapi_python_client.parser.properties import Schemas, property_from_data

        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema.construct(
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
        from openapi_python_client.parser.properties import Class, ModelProperty, Schemas, property_from_data

        name = "new_name"
        required = False
        class_name = "MyModel"
        nullable = True
        existing_model = model_property_factory()
        schemas = Schemas(classes_by_reference={f"/{class_name}": existing_model})

        data = oai.Schema.construct(
            allOf=[oai.Reference.construct(ref=f"#/{class_name}")],
            nullable=nullable,
        )
        build_union_property = mocker.patch(f"{MODULE_NAME}.build_union_property")

        prop, schemas = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=Config()
        )

        assert prop == attr.evolve(existing_model, name=name, required=required, nullable=nullable, python_name=name)
        build_union_property.assert_not_called()

    def test_property_from_data_no_valid_props_in_data(self):
        from openapi_python_client.parser.properties import AnyProperty, Schemas, property_from_data

        schemas = Schemas()
        data = oai.Schema()
        name = "blah"

        prop, new_schemas = property_from_data(
            name=name, required=True, data=data, schemas=schemas, parent_name="parent", config=MagicMock()
        )

        assert prop == AnyProperty(name=name, required=True, nullable=False, default=None, python_name=name)
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
        data = oai.Schema.construct(type="array")
        property_from_data = mocker.patch.object(properties, "property_from_data")
        schemas = properties.Schemas()

        p, new_schemas = properties.build_list_property(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=MagicMock()
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

        p, new_schemas = properties.build_list_property(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=config
        )

        assert p == PropertyError(data="blah", detail=f"invalid data in items of array {name}")
        assert new_schemas == second_schemas
        assert schemas != new_schemas, "Schema was mutated"
        property_from_data.assert_called_once_with(
            name=f"{name}_item", required=True, data=data.items, schemas=schemas, parent_name="parent", config=config
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
            name=name, required=True, data=data, schemas=schemas, parent_name="parent", config=config
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
        reference = oai.Reference.construct(ref="#/components/schema/NotExist")
        data = oai.Schema(anyOf=[reference])
        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=name)

        from openapi_python_client.parser.properties import Schemas, build_union_property

        p, s = build_union_property(
            name=name, required=required, data=data, schemas=Schemas(), parent_name="parent", config=MagicMock()
        )
        assert p == PropertyError(detail=f"Invalid property in union {name}", data=reference)


class TestStringBasedProperty:
    @pytest.mark.parametrize("nullable", (True, False))
    @pytest.mark.parametrize("required", (True, False))
    def test_no_format(self, string_property_factory, nullable, required):
        from openapi_python_client.parser.properties import property_from_data

        name = "some_prop"
        data = oai.Schema.construct(type="string", nullable=nullable, default='"hello world"', pattern="abcdef")

        p, _ = property_from_data(
            name=name, required=required, data=data, parent_name=None, config=Config(), schemas=Schemas()
        )

        assert p == string_property_factory(
            name=name, required=required, nullable=nullable, default="'\\\\\"hello world\\\\\"'", pattern=data.pattern
        )

    def test_datetime_format(self, date_time_property_factory):
        from openapi_python_client.parser.properties import property_from_data

        name = "datetime_prop"
        required = True
        data = oai.Schema.construct(
            type="string", schema_format="date-time", nullable=True, default="2020-11-06T12:00:00"
        )

        p, _ = property_from_data(
            name=name, required=required, data=data, schemas=Schemas(), config=Config(), parent_name=None
        )

        assert p == date_time_property_factory(
            name=name, required=required, nullable=True, default=f"isoparse('{data.default}')"
        )

    def test_datetime_bad_default(self):
        from openapi_python_client.parser.properties import property_from_data

        name = "datetime_prop"
        required = True
        data = oai.Schema.construct(type="string", schema_format="date-time", nullable=True, default="a")

        result, _ = property_from_data(
            name=name, required=required, data=data, schemas=Schemas(), config=Config(), parent_name=None
        )

        assert result == PropertyError(detail="Failed to validate default value", data=data)

    def test_date_format(self, date_property_factory):
        from openapi_python_client.parser.properties import property_from_data

        name = "date_prop"
        required = True
        nullable = True

        data = oai.Schema.construct(type="string", schema_format="date", nullable=nullable, default="2020-11-06")

        p, _ = property_from_data(
            name=name, required=required, data=data, schemas=Schemas(), config=Config(), parent_name=None
        )

        assert p == date_property_factory(
            name=name, required=required, nullable=nullable, default=f"isoparse('{data.default}').date()"
        )

    def test_date_format_bad_default(self):
        from openapi_python_client.parser.properties import property_from_data

        name = "date_prop"
        required = True
        nullable = True

        data = oai.Schema.construct(type="string", schema_format="date", nullable=nullable, default="a")

        p, _ = property_from_data(
            name=name, required=required, data=data, schemas=Schemas(), config=Config(), parent_name=None
        )

        assert p == PropertyError(detail="Failed to validate default value", data=data)

    def test__string_based_property_binary_format(self, file_property_factory):
        from openapi_python_client.parser.properties import property_from_data

        name = "file_prop"
        required = True
        nullable = True
        data = oai.Schema.construct(type="string", schema_format="binary", nullable=nullable, default="a")

        p, _ = property_from_data(
            name=name, required=required, data=data, schemas=Schemas(), config=Config(), parent_name=None
        )
        assert p == file_property_factory(name=name, required=required, nullable=nullable)

    def test__string_based_property_unsupported_format(self, string_property_factory):
        from openapi_python_client.parser.properties import property_from_data

        name = "unknown"
        required = True
        nullable = True
        data = oai.Schema.construct(type="string", schema_format="blah", nullable=nullable)

        p, _ = property_from_data(
            name=name, required=required, data=data, schemas=Schemas, config=Config(), parent_name=None
        )

        assert p == string_property_factory(name=name, required=required, nullable=nullable)


class TestBuildSchemas:
    def test_skips_references_and_keeps_going(self, mocker):
        from openapi_python_client.parser.properties import Schemas, build_schemas
        from openapi_python_client.schema import Reference, Schema

        components = {"a_ref": Reference.construct(), "a_schema": Schema.construct()}
        update_schemas_with_data = mocker.patch(f"{MODULE_NAME}.update_schemas_with_data")
        parse_reference_path = mocker.patch(f"{MODULE_NAME}.parse_reference_path")
        config = Config()

        result = build_schemas(components=components, schemas=Schemas(), config=config)
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
        from openapi_python_client.parser.properties import Schemas, build_schemas
        from openapi_python_client.schema import Schema

        components = {"first": Schema.construct(), "second": Schema.construct()}
        update_schemas_with_data = mocker.patch(f"{MODULE_NAME}.update_schemas_with_data")
        parse_reference_path = mocker.patch(
            f"{MODULE_NAME}.parse_reference_path", side_effect=[PropertyError(detail="some details"), "a_path"]
        )
        config = Config()

        result = build_schemas(components=components, schemas=Schemas(), config=config)
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
        from openapi_python_client.parser.properties import Schemas, build_schemas
        from openapi_python_client.schema import Schema

        components = {"first": Schema.construct(), "second": Schema.construct()}
        update_schemas_with_data = mocker.patch(
            f"{MODULE_NAME}.update_schemas_with_data", side_effect=[PropertyError(), Schemas(), PropertyError()]
        )
        parse_reference_path = mocker.patch(f"{MODULE_NAME}.parse_reference_path")
        config = Config()

        result = build_schemas(components=components, schemas=Schemas(), config=config)
        parse_reference_path.assert_has_calls(
            [
                call("#/components/schemas/first"),
                call("#/components/schemas/second"),
                call("#/components/schemas/first"),
            ]
        )
        assert update_schemas_with_data.call_count == 3
        assert result.errors == [PropertyError()]


def test_build_enum_property_conflict(mocker):
    from openapi_python_client.parser.properties import Schemas, build_enum_property

    data = oai.Schema()
    schemas = Schemas(classes_by_name={"Existing": mocker.MagicMock()})

    err, schemas = build_enum_property(
        data=data, name="Existing", required=True, schemas=schemas, enum=[], parent_name=None, config=Config()
    )

    assert schemas == schemas
    assert err == PropertyError(detail="Found conflicting enums named Existing with incompatible values.", data=data)


def test_build_enum_property_no_values():
    from openapi_python_client.parser.properties import Schemas, build_enum_property

    data = oai.Schema()
    schemas = Schemas()

    err, schemas = build_enum_property(
        data=data, name="Existing", required=True, schemas=schemas, enum=[], parent_name=None, config=Config()
    )

    assert schemas == schemas
    assert err == PropertyError(detail="No values provided for Enum", data=data)


def test_build_enum_property_bad_default():
    from openapi_python_client.parser.properties import Schemas, build_enum_property

    data = oai.Schema(default="B")
    schemas = Schemas()

    err, schemas = build_enum_property(
        data=data, name="Existing", required=True, schemas=schemas, enum=["A"], parent_name=None, config=Config()
    )

    assert schemas == schemas
    assert err == PropertyError(detail="B is an invalid default for enum Existing", data=data)
