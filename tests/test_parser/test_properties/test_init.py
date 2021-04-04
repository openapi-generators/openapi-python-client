from unittest.mock import MagicMock, call

import pytest

import openapi_python_client.schema as oai
from openapi_python_client import Config
from openapi_python_client.parser.errors import PropertyError, ValidationError
from openapi_python_client.parser.properties import BooleanProperty, FloatProperty, IntProperty

MODULE_NAME = "openapi_python_client.parser.properties"


class TestProperty:
    @pytest.mark.parametrize(
        "nullable,required,no_optional,json,expected",
        [
            (False, False, False, False, "Union[Unset, TestType]"),
            (False, False, True, False, "TestType"),
            (False, True, False, False, "TestType"),
            (False, True, True, False, "TestType"),
            (True, False, False, False, "Union[Unset, None, TestType]"),
            (True, False, True, False, "TestType"),
            (True, True, False, False, "Optional[TestType]"),
            (True, True, True, False, "TestType"),
            (False, False, False, True, "Union[Unset, str]"),
            (False, False, True, True, "str"),
            (False, True, False, True, "str"),
            (False, True, True, True, "str"),
            (True, False, False, True, "Union[Unset, None, str]"),
            (True, False, True, True, "str"),
            (True, True, False, True, "Optional[str]"),
            (True, True, True, True, "str"),
        ],
    )
    def test_get_type_string(self, mocker, nullable, required, no_optional, json, expected):
        from openapi_python_client.parser.properties import Property

        mocker.patch.object(Property, "_type_string", "TestType")
        mocker.patch.object(Property, "_json_type_string", "str")
        p = Property(name="test", required=required, default=None, nullable=nullable)
        assert p.get_type_string(no_optional=no_optional, json=json) == expected

    @pytest.mark.parametrize(
        "default,required,expected",
        [
            (None, False, "test: Union[Unset, TestType] = UNSET"),
            (None, True, "test: TestType"),
            ("Test", False, "test: Union[Unset, TestType] = Test"),
            ("Test", True, "test: TestType = Test"),
        ],
    )
    def test_to_string(self, mocker, default, required, expected):
        from openapi_python_client.parser.properties import Property

        name = "test"
        mocker.patch.object(Property, "_type_string", "TestType")
        p = Property(name=name, required=required, default=default, nullable=False)
        assert p.to_string() == expected

    def test_get_imports(self):
        from openapi_python_client.parser.properties import Property

        p = Property(name="test", required=True, default=None, nullable=False)
        assert p.get_imports(prefix="") == set()

        p = Property(name="test", required=False, default=None, nullable=False)
        assert p.get_imports(prefix="") == {"from types import UNSET, Unset", "from typing import Union"}

        p = Property(name="test", required=False, default=None, nullable=True)
        assert p.get_imports(prefix="") == {
            "from types import UNSET, Unset",
            "from typing import Optional",
            "from typing import Union",
        }


class TestStringProperty:
    def test_get_type_string(self):
        from openapi_python_client.parser.properties import StringProperty

        p = StringProperty(name="test", required=True, default=None, nullable=False)

        base_type_string = f"str"

        assert p.get_type_string() == base_type_string
        assert p.get_type_string(json=True) == base_type_string

        p = StringProperty(name="test", required=True, default=None, nullable=True)
        assert p.get_type_string() == f"Optional[{base_type_string}]"

        p = StringProperty(name="test", required=False, default=None, nullable=True)
        assert p.get_type_string() == f"Union[Unset, None, {base_type_string}]"

        p = StringProperty(name="test", required=False, default=None, nullable=False)
        assert p.get_type_string() == f"Union[Unset, {base_type_string}]"


class TestDateTimeProperty:
    def test_get_imports(self):
        from openapi_python_client.parser.properties import DateTimeProperty

        p = DateTimeProperty(name="test", required=True, default=None, nullable=False)
        assert p.get_imports(prefix="...") == {
            "import datetime",
            "from typing import cast",
            "from dateutil.parser import isoparse",
        }

        p = DateTimeProperty(name="test", required=False, default=None, nullable=False)
        assert p.get_imports(prefix="...") == {
            "import datetime",
            "from typing import cast",
            "from dateutil.parser import isoparse",
            "from typing import Union",
            "from ...types import UNSET, Unset",
        }

        p = DateTimeProperty(name="test", required=False, default=None, nullable=True)
        assert p.get_imports(prefix="...") == {
            "import datetime",
            "from typing import cast",
            "from dateutil.parser import isoparse",
            "from typing import Union",
            "from typing import Optional",
            "from ...types import UNSET, Unset",
        }


class TestDateProperty:
    def test_get_imports(self):
        from openapi_python_client.parser.properties import DateProperty

        p = DateProperty(name="test", required=True, default=None, nullable=False)
        assert p.get_imports(prefix="...") == {
            "import datetime",
            "from typing import cast",
            "from dateutil.parser import isoparse",
        }

        p = DateProperty(name="test", required=False, default=None, nullable=False)
        assert p.get_imports(prefix="...") == {
            "import datetime",
            "from typing import cast",
            "from dateutil.parser import isoparse",
            "from typing import Union",
            "from ...types import UNSET, Unset",
        }

        p = DateProperty(name="test", required=False, default=None, nullable=True)
        assert p.get_imports(prefix="...") == {
            "import datetime",
            "from typing import cast",
            "from dateutil.parser import isoparse",
            "from typing import Union",
            "from typing import Optional",
            "from ...types import UNSET, Unset",
        }


class TestFileProperty:
    def test_get_imports(self):
        from openapi_python_client.parser.properties import FileProperty

        prefix = "..."
        p = FileProperty(name="test", required=True, default=None, nullable=False)
        assert p.get_imports(prefix=prefix) == {
            "from io import BytesIO",
            "from ...types import File",
        }

        p = FileProperty(name="test", required=False, default=None, nullable=False)
        assert p.get_imports(prefix=prefix) == {
            "from io import BytesIO",
            "from ...types import File",
            "from typing import Union",
            "from ...types import UNSET, Unset",
        }

        p = FileProperty(name="test", required=False, default=None, nullable=True)
        assert p.get_imports(prefix=prefix) == {
            "from io import BytesIO",
            "from ...types import File",
            "from typing import Union",
            "from typing import Optional",
            "from ...types import UNSET, Unset",
        }


class TestListProperty:
    def test_get_type_string(self, mocker):
        from openapi_python_client.parser.properties import ListProperty

        inner_property = mocker.MagicMock()
        inner_type_string = mocker.MagicMock()
        inner_property.get_type_string.side_effect = (
            lambda no_optional=False, json=False: "int" if json else inner_type_string
        )
        p = ListProperty(name="test", required=True, default=None, inner_property=inner_property, nullable=False)

        base_type_string = f"List[{inner_type_string}]"

        assert p.get_type_string() == base_type_string
        assert p.get_type_string(json=True) == "List[int]"

        p = ListProperty(name="test", required=True, default=None, inner_property=inner_property, nullable=True)
        assert p.get_type_string() == f"Optional[{base_type_string}]"
        assert p.get_type_string(no_optional=True) == base_type_string

        p = ListProperty(name="test", required=False, default=None, inner_property=inner_property, nullable=True)
        assert p.get_type_string() == f"Union[Unset, None, {base_type_string}]"
        assert p.get_type_string(no_optional=True) == base_type_string

        p = ListProperty(name="test", required=False, default=None, inner_property=inner_property, nullable=False)
        assert p.get_type_string() == f"Union[Unset, {base_type_string}]"
        assert p.get_type_string(no_optional=True) == base_type_string

    def test_get_type_imports(self, mocker):
        from openapi_python_client.parser.properties import ListProperty

        inner_property = mocker.MagicMock()
        inner_import = mocker.MagicMock()
        inner_property.get_imports.return_value = {inner_import}
        prefix = "..."
        p = ListProperty(name="test", required=True, default=None, inner_property=inner_property, nullable=False)

        assert p.get_imports(prefix=prefix) == {
            inner_import,
            "from typing import cast, List",
        }

        p = ListProperty(name="test", required=False, default=None, inner_property=inner_property, nullable=False)
        assert p.get_imports(prefix=prefix) == {
            inner_import,
            "from typing import cast, List",
            "from typing import Union",
            "from ...types import UNSET, Unset",
        }

        p = ListProperty(name="test", required=False, default=None, inner_property=inner_property, nullable=True)
        assert p.get_imports(prefix=prefix) == {
            inner_import,
            "from typing import cast, List",
            "from typing import Union",
            "from typing import Optional",
            "from ...types import UNSET, Unset",
        }


class TestUnionProperty:
    @pytest.mark.parametrize(
        "nullable,required,no_optional,json,expected",
        [
            (False, False, False, False, "Union[Unset, inner_type_string_1, inner_type_string_2]"),
            (False, False, True, False, "Union[inner_type_string_1, inner_type_string_2]"),
            (False, True, False, False, "Union[inner_type_string_1, inner_type_string_2]"),
            (False, True, True, False, "Union[inner_type_string_1, inner_type_string_2]"),
            (True, False, False, False, "Union[None, Unset, inner_type_string_1, inner_type_string_2]"),
            (True, False, True, False, "Union[inner_type_string_1, inner_type_string_2]"),
            (True, True, False, False, "Union[None, inner_type_string_1, inner_type_string_2]"),
            (True, True, True, False, "Union[inner_type_string_1, inner_type_string_2]"),
            (False, False, False, True, "Union[Unset, inner_json_type_string_1, inner_json_type_string_2]"),
            (False, False, True, True, "Union[inner_json_type_string_1, inner_json_type_string_2]"),
            (False, True, False, True, "Union[inner_json_type_string_1, inner_json_type_string_2]"),
            (False, True, True, True, "Union[inner_json_type_string_1, inner_json_type_string_2]"),
            (True, False, False, True, "Union[None, Unset, inner_json_type_string_1, inner_json_type_string_2]"),
            (True, False, True, True, "Union[inner_json_type_string_1, inner_json_type_string_2]"),
            (True, True, False, True, "Union[None, inner_json_type_string_1, inner_json_type_string_2]"),
            (True, True, True, True, "Union[inner_json_type_string_1, inner_json_type_string_2]"),
        ],
    )
    def test_get_type_string(self, mocker, nullable, required, no_optional, json, expected):
        from openapi_python_client.parser.properties import UnionProperty

        inner_property_1 = mocker.MagicMock()
        inner_property_1.get_type_string.side_effect = (
            lambda no_optional=False, json=False: "inner_json_type_string_1" if json else "inner_type_string_1"
        )
        inner_property_2 = mocker.MagicMock()
        inner_property_2.get_type_string.side_effect = (
            lambda no_optional=False, json=False: "inner_json_type_string_2" if json else "inner_type_string_2"
        )
        p = UnionProperty(
            name="test",
            required=required,
            default=None,
            inner_properties=[inner_property_1, inner_property_2],
            nullable=nullable,
        )
        assert p.get_type_string(no_optional=no_optional, json=json) == expected

    def test_get_base_type_string(self, mocker):
        from openapi_python_client.parser.properties import UnionProperty

        inner_property_1 = mocker.MagicMock()
        inner_property_1.get_type_string.side_effect = (
            lambda no_optional=False, json=False: "inner_json_type_string_1" if json else "inner_type_string_1"
        )
        inner_property_2 = mocker.MagicMock()
        inner_property_2.get_type_string.side_effect = (
            lambda no_optional=False, json=False: "inner_json_type_string_2" if json else "inner_type_string_2"
        )
        p = UnionProperty(
            name="test",
            required=False,
            default=None,
            inner_properties=[inner_property_1, inner_property_2],
            nullable=True,
        )
        assert p.get_base_type_string() == "Union[inner_type_string_1, inner_type_string_2]"

    def test_get_base_type_string_one_element(self, mocker):
        from openapi_python_client.parser.properties import UnionProperty

        inner_property_1 = mocker.MagicMock()
        inner_property_1.get_type_string.side_effect = (
            lambda no_optional=False, json=False: "inner_json_type_string_1" if json else "inner_type_string_1"
        )
        p = UnionProperty(
            name="test",
            required=False,
            default=None,
            inner_properties=[inner_property_1],
            nullable=True,
        )
        assert p.get_base_type_string() == "inner_type_string_1"

    def test_get_base_json_type_string(self, mocker):
        from openapi_python_client.parser.properties import UnionProperty

        inner_property_1 = mocker.MagicMock()
        inner_property_1.get_type_string.side_effect = (
            lambda no_optional=False, json=False: "inner_json_type_string_1" if json else "inner_type_string_1"
        )
        inner_property_2 = mocker.MagicMock()
        inner_property_2.get_type_string.side_effect = (
            lambda no_optional=False, json=False: "inner_json_type_string_2" if json else "inner_type_string_2"
        )
        p = UnionProperty(
            name="test",
            required=False,
            default=None,
            inner_properties=[inner_property_1, inner_property_2],
            nullable=True,
        )
        assert p.get_base_json_type_string() == "Union[inner_json_type_string_1, inner_json_type_string_2]"

    def test_get_imports(self, mocker):
        from openapi_python_client.parser.properties import UnionProperty

        inner_property_1 = mocker.MagicMock()
        inner_import_1 = mocker.MagicMock()
        inner_property_1.get_imports.return_value = {inner_import_1}
        inner_property_2 = mocker.MagicMock()
        inner_import_2 = mocker.MagicMock()
        inner_property_2.get_imports.return_value = {inner_import_2}
        prefix = "..."
        p = UnionProperty(
            name="test",
            required=True,
            default=None,
            inner_properties=[inner_property_1, inner_property_2],
            nullable=False,
        )

        assert p.get_imports(prefix=prefix) == {
            inner_import_1,
            inner_import_2,
            "from typing import cast, Union",
        }

        p = UnionProperty(
            name="test",
            required=False,
            default=None,
            inner_properties=[inner_property_1, inner_property_2],
            nullable=False,
        )
        assert p.get_imports(prefix=prefix) == {
            inner_import_1,
            inner_import_2,
            "from typing import Union",
            "from typing import cast, Union",
            "from ...types import UNSET, Unset",
        }

        p = UnionProperty(
            name="test",
            required=False,
            default=None,
            inner_properties=[inner_property_1, inner_property_2],
            nullable=True,
        )
        assert p.get_imports(prefix=prefix) == {
            inner_import_1,
            inner_import_2,
            "from typing import Union",
            "from typing import cast, Union",
            "from typing import Optional",
            "from ...types import UNSET, Unset",
        }


class TestEnumProperty:
    @pytest.mark.parametrize(
        "required, nullable, expected",
        (
            (False, False, "Union[Unset, {}]"),
            (True, False, "{}"),
            (False, True, "Union[Unset, None, {}]"),
            (True, True, "Optional[{}]"),
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


class TestPropertyFromData:
    def test_property_from_data_str_enum(self, mocker):
        from openapi_python_client.parser.properties import Class, EnumProperty
        from openapi_python_client.schema import Schema

        data = Schema(title="AnEnum", enum=["A", "B", "C"], nullable=False, default="B")
        name = "my_enum"
        required = True

        from openapi_python_client.parser.properties import Schemas, property_from_data

        schemas = Schemas(classes_by_name={"AnEnum": mocker.MagicMock()})

        prop, new_schemas = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=Config()
        )

        assert prop == EnumProperty(
            name="my_enum",
            required=True,
            nullable=False,
            values={"A": "A", "B": "B", "C": "C"},
            class_info=Class(name="ParentAnEnum", module_name="parent_an_enum"),
            value_type=str,
            default="ParentAnEnum.B",
        )
        assert schemas != new_schemas, "Provided Schemas was mutated"
        assert new_schemas.classes_by_name == {
            "AnEnum": schemas.classes_by_name["AnEnum"],
            "ParentAnEnum": prop,
        }

    def test_property_from_data_int_enum(self, mocker):
        from openapi_python_client.parser.properties import Class, EnumProperty
        from openapi_python_client.schema import Schema

        data = Schema.construct(title="anEnum", enum=[1, 2, 3], nullable=False, default=3)
        name = "my_enum"
        required = True

        from openapi_python_client.parser.properties import Schemas, property_from_data

        schemas = Schemas(classes_by_name={"AnEnum": mocker.MagicMock()})

        prop, new_schemas = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=Config()
        )

        assert prop == EnumProperty(
            name="my_enum",
            required=True,
            nullable=False,
            values={"VALUE_1": 1, "VALUE_2": 2, "VALUE_3": 3},
            class_info=Class(name="ParentAnEnum", module_name="parent_an_enum"),
            value_type=int,
            default="ParentAnEnum.VALUE_3",
        )
        assert schemas != new_schemas, "Provided Schemas was mutated"
        assert new_schemas.classes_by_name == {
            "AnEnum": schemas.classes_by_name["AnEnum"],
            "ParentAnEnum": prop,
        }

    def test_property_from_data_ref_enum(self):
        from openapi_python_client.parser.properties import Class, EnumProperty, Schemas, property_from_data

        name = "some_enum"
        data = oai.Reference.construct(ref="#/components/schemas/MyEnum")
        existing_enum = EnumProperty(
            name="an_enum",
            required=True,
            nullable=False,
            default=None,
            values={"A": "a"},
            value_type=str,
            class_info=Class(name="MyEnum", module_name="my_enum"),
        )
        schemas = Schemas(classes_by_reference={"/components/schemas/MyEnum": existing_enum})

        prop, new_schemas = property_from_data(
            name=name, required=False, data=data, schemas=schemas, parent_name="", config=Config()
        )

        assert prop == EnumProperty(
            name="some_enum",
            required=False,
            nullable=False,
            default=None,
            values={"A": "a"},
            value_type=str,
            class_info=Class(name="MyEnum", module_name="my_enum"),
        )
        assert schemas == new_schemas

    def test_property_from_data_ref_model(self):
        from openapi_python_client.parser.properties import Class, ModelProperty, Schemas, property_from_data

        name = "new_name"
        required = False
        class_name = "MyModel"
        data = oai.Reference.construct(ref=f"#/components/schemas/{class_name}")
        existing_model = ModelProperty(
            name="old_name",
            required=True,
            nullable=False,
            default=None,
            class_info=Class(name=class_name, module_name="my_model"),
            required_properties=[],
            optional_properties=[],
            description="",
            relative_imports=set(),
            additional_properties=False,
        )
        schemas = Schemas(classes_by_reference={f"/components/schemas/{class_name}": existing_model})

        prop, new_schemas = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="", config=Config()
        )

        assert prop == ModelProperty(
            name=name,
            required=required,
            nullable=False,
            default=None,
            class_info=Class(name=class_name, module_name="my_model"),
            required_properties=[],
            optional_properties=[],
            description="",
            relative_imports=set(),
            additional_properties=False,
        )
        assert schemas == new_schemas

    def test_property_from_data_ref_not_found(self, mocker):
        from openapi_python_client.parser.properties import PropertyError, Schemas, property_from_data

        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Reference.construct(ref=mocker.MagicMock())
        parse_reference_path = mocker.patch(f"{MODULE_NAME}.parse_reference_path")
        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=name)
        schemas = Schemas()

        prop, new_schemas = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=mocker.MagicMock()
        )

        parse_reference_path.assert_called_once_with(data.ref)
        assert prop == PropertyError(data=data, detail="Could not find reference in parsed models or enums")
        assert schemas == new_schemas

    def test_property_from_data_string(self, mocker):
        from openapi_python_client.parser.properties import Schemas, property_from_data

        _string_based_property = mocker.patch(f"{MODULE_NAME}._string_based_property")
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema.construct(type="string")
        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=name)
        schemas = Schemas()

        p, new_schemas = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=mocker.MagicMock()
        )

        assert p == _string_based_property.return_value
        assert schemas == new_schemas
        _string_based_property.assert_called_once_with(name=name, required=required, data=data)

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

        assert p == prop_type(name=name, required=required, default=python_type(data.default), nullable=False)
        assert new_schemas == schemas

        # Test nullable values
        data.default = 0
        data.nullable = True

        p, _ = property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=MagicMock()
        )
        assert p == prop_type(name=name, required=required, default=python_type(data.default), nullable=True)

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

    def test_property_from_data_unsupported_type(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema.construct(type=mocker.MagicMock())

        from openapi_python_client.parser.errors import PropertyError
        from openapi_python_client.parser.properties import Schemas, property_from_data

        assert property_from_data(
            name=name, required=required, data=data, schemas=Schemas(), parent_name="parent", config=MagicMock()
        ) == (
            PropertyError(data=data, detail=f"unknown type {data.type}"),
            Schemas(),
        )

    def test_property_from_data_no_valid_props_in_data(self):
        from openapi_python_client.parser.properties import NoneProperty, Schemas, property_from_data

        schemas = Schemas()
        data = oai.Schema()

        prop, new_schemas = property_from_data(
            name="blah", required=True, data=data, schemas=schemas, parent_name="parent", config=MagicMock()
        )

        assert prop == NoneProperty(name="blah", required=True, nullable=False, default=None)
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

    def test_build_list_property(self, mocker):
        from openapi_python_client.parser import properties

        name = "prop"
        required = mocker.MagicMock()
        data = oai.Schema(
            type="array",
            items={},
        )
        schemas = properties.Schemas()
        second_schemas = properties.Schemas(errors=["error"])
        property_from_data = mocker.patch.object(
            properties, "property_from_data", return_value=(mocker.MagicMock(), second_schemas)
        )
        mocker.patch("openapi_python_client.utils.snake_case", return_value=name)
        mocker.patch("openapi_python_client.utils.to_valid_python_identifier", return_value=name)
        config = MagicMock()

        p, new_schemas = properties.build_list_property(
            name=name, required=required, data=data, schemas=schemas, parent_name="parent", config=config
        )

        assert isinstance(p, properties.ListProperty)
        assert p.inner_property == property_from_data.return_value[0]
        assert new_schemas == second_schemas
        assert schemas != new_schemas, "Schema was mutated"
        property_from_data.assert_called_once_with(
            name=f"{name}_item", required=True, data=data.items, schemas=schemas, parent_name="parent", config=config
        )


class TestBuildUnionProperty:
    def test_property_from_data_union(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema(
            anyOf=[{"type": "number", "default": "0.0"}],
            oneOf=[
                {"type": "integer", "default": "0"},
            ],
        )
        UnionProperty = mocker.patch(f"{MODULE_NAME}.UnionProperty")
        FloatProperty = mocker.patch(f"{MODULE_NAME}.FloatProperty")
        IntProperty = mocker.patch(f"{MODULE_NAME}.IntProperty")
        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=name)

        from openapi_python_client.parser.properties import Schemas, property_from_data

        p, s = property_from_data(
            name=name, required=required, data=data, schemas=Schemas(), parent_name="parent", config=MagicMock()
        )

        FloatProperty.assert_called_once_with(name=name, required=required, default=0.0, nullable=False)
        IntProperty.assert_called_once_with(name=name, required=required, default=0, nullable=False)
        UnionProperty.assert_called_once_with(
            name=name,
            required=required,
            default=None,
            inner_properties=[FloatProperty.return_value, IntProperty.return_value],
            nullable=False,
        )
        assert p == UnionProperty.return_value
        assert s == Schemas()

    def test_property_from_data_union_bad_type(self, mocker):
        name = "bad_union"
        required = mocker.MagicMock()
        data = oai.Schema(anyOf=[{"type": "garbage"}])
        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=name)

        from openapi_python_client.parser.properties import Schemas, property_from_data

        p, s = property_from_data(
            name=name, required=required, data=data, schemas=Schemas(), parent_name="parent", config=MagicMock()
        )

        assert p == PropertyError(detail=f"Invalid property in union {name}", data=oai.Schema(type="garbage"))


class TestStringBasedProperty:
    def test__string_based_property_no_format(self):
        from openapi_python_client.parser.properties import StringProperty

        name = "some_prop"
        required = True
        data = oai.Schema.construct(type="string", nullable=True, default='"hello world"')

        from openapi_python_client.parser.properties import _string_based_property

        p = _string_based_property(name=name, required=required, data=data)

        assert p == StringProperty(name=name, required=required, nullable=True, default="'\\\\\"hello world\\\\\"'")

        data.pattern = "abcdef"
        data.nullable = False

        p = _string_based_property(
            name=name,
            required=required,
            data=data,
        )
        assert p == StringProperty(
            name=name, required=required, nullable=False, default="'\\\\\"hello world\\\\\"'", pattern="abcdef"
        )

    def test__string_based_property_datetime_format(self):
        from openapi_python_client.parser.properties import DateTimeProperty, _string_based_property

        name = "datetime_prop"
        required = True
        data = oai.Schema.construct(
            type="string", schema_format="date-time", nullable=True, default="2020-11-06T12:00:00"
        )

        p = _string_based_property(name=name, required=required, data=data)

        assert p == DateTimeProperty(
            name=name, required=required, nullable=True, default="isoparse('2020-11-06T12:00:00')"
        )

        # Test bad default
        data.default = "a"
        with pytest.raises(ValidationError):
            _string_based_property(name=name, required=required, data=data)

    def test__string_based_property_date_format(self):
        from openapi_python_client.parser.properties import DateProperty, _string_based_property

        name = "date_prop"
        required = True
        data = oai.Schema.construct(type="string", schema_format="date", nullable=True, default="2020-11-06")

        p = _string_based_property(name=name, required=required, data=data)

        assert p == DateProperty(name=name, required=required, nullable=True, default="isoparse('2020-11-06').date()")

        # Test bad default
        data.default = "a"
        with pytest.raises(ValidationError):
            _string_based_property(name=name, required=required, data=data)

    def test__string_based_property_binary_format(self):
        from openapi_python_client.parser.properties import FileProperty, _string_based_property

        name = "file_prop"
        required = True
        data = oai.Schema.construct(type="string", schema_format="binary", nullable=True, default="a")

        p = _string_based_property(name=name, required=required, data=data)
        assert p == FileProperty(name=name, required=required, nullable=True, default=None)

    def test__string_based_property_unsupported_format(self, mocker):
        from openapi_python_client.parser.properties import StringProperty, _string_based_property

        name = "unknown"
        required = True
        data = oai.Schema.construct(type="string", schema_format="blah", nullable=True)

        p = _string_based_property(name=name, required=required, data=data)

        assert p == StringProperty(name=name, required=required, nullable=True, default=None)


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
