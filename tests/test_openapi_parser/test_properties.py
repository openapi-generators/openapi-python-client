import pytest

MODULE_NAME = "openapi_python_client.openapi_parser.properties"


class TestProperty:
    def test_get_type_string(self):
        from openapi_python_client.openapi_parser.properties import Property

        p = Property(name="test", required=True, default=None)
        p._type_string = "TestType"

        assert p.get_type_string() == "TestType"
        p.required = False
        assert p.get_type_string() == "Optional[TestType]"

    def test_to_string(self, mocker):
        from openapi_python_client.openapi_parser.properties import Property

        name = mocker.MagicMock()
        snake_case = mocker.patch(f"openapi_python_client.utils.snake_case")
        p = Property(name=name, required=True, default=None)
        get_type_string = mocker.patch.object(p, "get_type_string")

        assert p.to_string() == f"{snake_case(name)}: {get_type_string()}"
        p.required = False
        assert p.to_string() == f"{snake_case(name)}: {get_type_string()} = None"

        p.default = "TEST"
        assert p.to_string() == f"{snake_case(name)}: {get_type_string()} = TEST"

    def test_transform(self, mocker):
        from openapi_python_client.openapi_parser.properties import Property

        name = mocker.MagicMock()
        snake_case = mocker.patch(f"openapi_python_client.utils.snake_case")
        p = Property(name=name, required=True, default=None)
        assert p.transform() == snake_case(name)

    def test_get_imports(self, mocker):
        from openapi_python_client.openapi_parser.properties import Property

        name = mocker.MagicMock()
        mocker.patch(f"openapi_python_client.utils.snake_case")
        p = Property(name=name, required=True, default=None)
        assert p.get_imports(prefix="") == set()

        p.required = False
        assert p.get_imports(prefix="") == {"from typing import Optional"}


class TestStringProperty:
    def test___post_init__(self):
        from openapi_python_client.openapi_parser.properties import StringProperty

        sp = StringProperty(name="test", required=True, default="A Default Value",)

        assert sp.default == '"A Default Value"'

    def test_get_type_string(self):
        from openapi_python_client.openapi_parser.properties import StringProperty

        p = StringProperty(name="test", required=True, default=None)

        assert p.get_type_string() == "str"
        p.required = False
        assert p.get_type_string() == "Optional[str]"


class TestDateTimeProperty:
    def test_transform(self, mocker):
        name = "thePropertyName"
        mocker.patch(f"{MODULE_NAME}.Reference.from_ref")

        from openapi_python_client.openapi_parser.properties import DateTimeProperty

        prop = DateTimeProperty(name=name, required=True, default=None)

        assert prop.transform() == f"the_property_name.isoformat()"

    def test_get_imports(self, mocker):
        from openapi_python_client.openapi_parser.properties import DateTimeProperty

        name = mocker.MagicMock()
        mocker.patch(f"openapi_python_client.utils.snake_case")
        p = DateTimeProperty(name=name, required=True, default=None)
        assert p.get_imports(prefix="") == {
            "from datetime import datetime",
            "from typing import cast",
        }

        p.required = False
        assert p.get_imports(prefix="") == {
            "from typing import Optional",
            "from datetime import datetime",
            "from typing import cast",
        }


class TestDateProperty:
    def test_transform(self, mocker):
        name = "thePropertyName"
        mocker.patch(f"{MODULE_NAME}.Reference.from_ref")

        from openapi_python_client.openapi_parser.properties import DateProperty

        prop = DateProperty(name=name, required=True, default=None)

        assert prop.transform() == f"the_property_name.isoformat()"

    def test_get_imports(self, mocker):
        from openapi_python_client.openapi_parser.properties import DateProperty

        name = mocker.MagicMock()
        mocker.patch(f"openapi_python_client.utils.snake_case")
        p = DateProperty(name=name, required=True, default=None)
        assert p.get_imports(prefix="") == {
            "from datetime import date",
            "from typing import cast",
        }

        p.required = False
        assert p.get_imports(prefix="") == {
            "from typing import Optional",
            "from datetime import date",
            "from typing import cast",
        }


class TestFileProperty:
    def test_transform(self):
        name = "thePropertyName"

        from openapi_python_client.openapi_parser.properties import FileProperty

        prop = FileProperty(name=name, required=True, default=None)

        assert prop.transform() == f"the_property_name.to_tuple()"

    def test_get_imports(self, mocker):
        from openapi_python_client.openapi_parser.properties import FileProperty

        name = mocker.MagicMock()
        mocker.patch(f"openapi_python_client.utils.snake_case")
        prefix = "blah"
        p = FileProperty(name=name, required=True, default=None)
        assert p.get_imports(prefix=prefix) == {f"from {prefix}.types import File", "from dataclasses import astuple"}

        p.required = False
        assert p.get_imports(prefix=prefix) == {
            "from typing import Optional",
            f"from {prefix}.types import File",
            "from dataclasses import astuple",
        }


class TestListProperty:
    def test_get_type_string(self, mocker):
        from openapi_python_client.openapi_parser.properties import ListProperty

        inner_property = mocker.MagicMock()
        inner_type_string = mocker.MagicMock()
        inner_property.get_type_string.return_value = inner_type_string
        p = ListProperty(name="test", required=True, default=None, inner_property=inner_property)

        assert p.get_type_string() == f"List[{inner_type_string}]"
        p.required = False
        assert p.get_type_string() == f"Optional[List[{inner_type_string}]]"

    def test_get_type_imports(self, mocker):
        from openapi_python_client.openapi_parser.properties import ListProperty

        inner_property = mocker.MagicMock()
        inner_import = mocker.MagicMock()
        inner_property.get_imports.return_value = {inner_import}
        prefix = mocker.MagicMock()
        p = ListProperty(name="test", required=True, default=None, inner_property=inner_property)

        assert p.get_imports(prefix=prefix) == {
            inner_import,
            "from typing import List",
        }
        p.required = False
        assert p.get_imports(prefix=prefix) == {
            inner_import,
            "from typing import List",
            "from typing import Optional",
        }


class TestEnumProperty:
    def test___post_init__(self, mocker):
        name = mocker.MagicMock()

        snake_case = mocker.patch(f"openapi_python_client.utils.snake_case")
        from openapi_python_client.openapi_parser.properties import EnumProperty

        enum_property = EnumProperty(
            name=name,
            required=True,
            default="second",
            values={"FIRST": "first", "SECOND": "second"},
            reference=(mocker.MagicMock(class_name="MyTestEnum")),
        )

        assert enum_property.default == "MyTestEnum.SECOND"
        assert enum_property.python_name == snake_case(name)

    def test_get_type_string(self, mocker):
        fake_reference = mocker.MagicMock(class_name="MyTestEnum")
        mocker.patch(f"{MODULE_NAME}.Reference.from_ref", return_value=fake_reference)

        from openapi_python_client.openapi_parser.properties import EnumProperty

        enum_property = EnumProperty(
            name="test", required=True, default=None, values={}, reference=mocker.MagicMock(class_name="MyTestEnum")
        )

        assert enum_property.get_type_string() == "MyTestEnum"
        enum_property.required = False
        assert enum_property.get_type_string() == "Optional[MyTestEnum]"

    def test_get_imports(self, mocker):
        fake_reference = mocker.MagicMock(class_name="MyTestEnum", module_name="my_test_enum")
        mocker.patch(f"{MODULE_NAME}.Reference.from_ref", return_value=fake_reference)
        prefix = mocker.MagicMock()

        from openapi_python_client.openapi_parser.properties import EnumProperty

        enum_property = EnumProperty(name="test", required=True, default=None, values={}, reference=fake_reference)

        assert enum_property.get_imports(prefix=prefix) == {
            f"from {prefix}.{fake_reference.module_name} import {fake_reference.class_name}"
        }

        enum_property.required = False
        assert enum_property.get_imports(prefix=prefix) == {
            f"from {prefix}.{fake_reference.module_name} import {fake_reference.class_name}",
            "from typing import Optional",
        }

    def test_transform(self, mocker):
        name = "thePropertyName"
        mocker.patch(f"{MODULE_NAME}.Reference.from_ref")

        from openapi_python_client.openapi_parser.properties import EnumProperty

        enum_property = EnumProperty(name=name, required=True, default=None, values={}, reference=mocker.MagicMock())

        assert enum_property.transform() == f"the_property_name.value"

    def test_values_from_list(self):
        from openapi_python_client.openapi_parser.properties import EnumProperty

        data = ["abc", "123", "a23", "1bc"]

        result = EnumProperty.values_from_list(data)

        assert result == {
            "ABC": "abc",
            "VALUE_1": "123",
            "A23": "a23",
            "VALUE_3": "1bc",
        }


class TestRefProperty:
    def test_get_type_string(self, mocker):
        from openapi_python_client.openapi_parser.properties import RefProperty

        ref_property = RefProperty(
            name="test", required=True, default=None, reference=mocker.MagicMock(class_name="MyRefClass")
        )

        assert ref_property.get_type_string() == "MyRefClass"

        ref_property.required = False
        assert ref_property.get_type_string() == "Optional[MyRefClass]"

    def test_get_imports(self, mocker):
        fake_reference = mocker.MagicMock(class_name="MyRefClass", module_name="my_test_enum")
        prefix = mocker.MagicMock()

        from openapi_python_client.openapi_parser.properties import RefProperty

        p = RefProperty(name="test", required=True, default=None, reference=fake_reference)

        assert p.get_imports(prefix=prefix) == {
            f"from {prefix}.{fake_reference.module_name} import {fake_reference.class_name}",
            "from typing import Dict",
            "from typing import cast",
        }

        p.required = False
        assert p.get_imports(prefix=prefix) == {
            f"from {prefix}.{fake_reference.module_name} import {fake_reference.class_name}",
            "from typing import Dict",
            "from typing import cast",
            "from typing import Optional",
        }

    def test_transform(self, mocker):
        from openapi_python_client.openapi_parser.properties import RefProperty

        ref_property = RefProperty(name="super_unique_name", required=True, default=None, reference=mocker.MagicMock())

        assert ref_property.transform() == "super_unique_name.to_dict()"


class TestDictProperty:
    def test_get_imports(self, mocker):
        from openapi_python_client.openapi_parser.properties import DictProperty

        name = mocker.MagicMock()
        mocker.patch(f"openapi_python_client.utils.snake_case")
        prefix = mocker.MagicMock()
        p = DictProperty(name=name, required=True, default=None)
        assert p.get_imports(prefix=prefix) == {
            "from typing import Dict",
        }

        p.required = False
        assert p.get_imports(prefix=prefix) == {
            "from typing import Optional",
            "from typing import Dict",
        }


class TestPropertyFromDict:
    def test_property_from_dict_enum(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = {
            "enum": mocker.MagicMock(),
        }
        EnumProperty = mocker.patch(f"{MODULE_NAME}.EnumProperty")
        from_ref = mocker.patch(f"{MODULE_NAME}.Reference.from_ref")

        from openapi_python_client.openapi_parser.properties import property_from_dict

        p = property_from_dict(name=name, required=required, data=data)

        EnumProperty.values_from_list.assert_called_once_with(data["enum"])
        EnumProperty.assert_called_once_with(
            name=name, required=required, values=EnumProperty.values_from_list(), default=None, reference=from_ref()
        )
        assert p == EnumProperty()

        EnumProperty.reset_mock()
        data["default"] = mocker.MagicMock()

        property_from_dict(
            name=name, required=required, data=data,
        )
        EnumProperty.assert_called_once_with(
            name=name,
            required=required,
            values=EnumProperty.values_from_list(),
            default=data["default"],
            reference=from_ref(),
        )

    def test_property_from_dict_ref(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = {
            "$ref": mocker.MagicMock(),
        }
        from_ref = mocker.patch(f"{MODULE_NAME}.Reference.from_ref")
        RefProperty = mocker.patch(f"{MODULE_NAME}.RefProperty")

        from openapi_python_client.openapi_parser.properties import property_from_dict

        p = property_from_dict(name=name, required=required, data=data)

        from_ref.assert_called_once_with(data["$ref"])
        RefProperty.assert_called_once_with(name=name, required=required, reference=from_ref(), default=None)
        assert p == RefProperty()

    def test_property_from_dict_string(self, mocker):
        _string_based_property = mocker.patch(f"{MODULE_NAME}._string_based_property")
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = {
            "type": "string",
        }
        from openapi_python_client.openapi_parser.properties import property_from_dict

        p = property_from_dict(name=name, required=required, data=data)

        assert p == _string_based_property.return_value
        _string_based_property.assert_called_once_with(name=name, required=required, data=data)

    @pytest.mark.parametrize(
        "openapi_type,python_type",
        [
            ("number", "FloatProperty"),
            ("integer", "IntProperty"),
            ("boolean", "BooleanProperty"),
            ("object", "DictProperty"),
        ],
    )
    def test_property_from_dict_simple_types(self, mocker, openapi_type, python_type):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = {
            "type": openapi_type,
        }
        clazz = mocker.patch(f"{MODULE_NAME}.{python_type}")

        from openapi_python_client.openapi_parser.properties import property_from_dict

        p = property_from_dict(name=name, required=required, data=data)

        clazz.assert_called_once_with(name=name, required=required, default=None)
        assert p == clazz()

        # Test optional values
        clazz.reset_mock()
        data["default"] = mocker.MagicMock()

        property_from_dict(
            name=name, required=required, data=data,
        )
        clazz.assert_called_once_with(name=name, required=required, default=data["default"])

    def test_property_from_dict_array(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = {
            "type": "array",
            "items": {"type": "number", "default": "0.0"},
        }
        ListProperty = mocker.patch(f"{MODULE_NAME}.ListProperty")
        FloatProperty = mocker.patch(f"{MODULE_NAME}.FloatProperty")

        from openapi_python_client.openapi_parser.properties import property_from_dict

        p = property_from_dict(name=name, required=required, data=data)

        FloatProperty.assert_called_once_with(name=f"{name}_item", required=True, default="0.0")
        ListProperty.assert_called_once_with(
            name=name, required=required, default=None, inner_property=FloatProperty.return_value
        )
        assert p == ListProperty.return_value

    def test_property_from_dict_unsupported_type(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = {
            "type": mocker.MagicMock(),
        }

        from openapi_python_client.openapi_parser.properties import property_from_dict

        with pytest.raises(ValueError):
            property_from_dict(name=name, required=required, data=data)


class TestStringBasedProperty:
    def test__string_based_property_no_format(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = {
            "type": "string",
        }
        StringProperty = mocker.patch(f"{MODULE_NAME}.StringProperty")

        from openapi_python_client.openapi_parser.properties import _string_based_property

        p = _string_based_property(name=name, required=required, data=data)

        StringProperty.assert_called_once_with(name=name, required=required, pattern=None, default=None)
        assert p == StringProperty.return_value

        # Test optional values
        StringProperty.reset_mock()
        data["default"] = mocker.MagicMock()
        data["pattern"] = mocker.MagicMock()

        _string_based_property(
            name=name, required=required, data=data,
        )
        StringProperty.assert_called_once_with(
            name=name, required=required, pattern=data["pattern"], default=data["default"]
        )

    def test__string_based_property_datetime_format(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = {
            "type": "string",
            "format": "date-time",
        }
        DateTimeProperty = mocker.patch(f"{MODULE_NAME}.DateTimeProperty")

        from openapi_python_client.openapi_parser.properties import _string_based_property

        p = _string_based_property(name=name, required=required, data=data)

        DateTimeProperty.assert_called_once_with(name=name, required=required, default=None)
        assert p == DateTimeProperty.return_value

        # Test optional values
        DateTimeProperty.reset_mock()
        data["default"] = mocker.MagicMock()

        _string_based_property(
            name=name, required=required, data=data,
        )
        DateTimeProperty.assert_called_once_with(name=name, required=required, default=data["default"])

    def test__string_based_property_date_format(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = {
            "type": "string",
            "format": "date",
        }
        DateProperty = mocker.patch(f"{MODULE_NAME}.DateProperty")

        from openapi_python_client.openapi_parser.properties import _string_based_property

        p = _string_based_property(name=name, required=required, data=data)
        DateProperty.assert_called_once_with(name=name, required=required, default=None)
        assert p == DateProperty.return_value

        # Test optional values
        DateProperty.reset_mock()
        data["default"] = mocker.MagicMock()

        _string_based_property(
            name=name, required=required, data=data,
        )
        DateProperty.assert_called_once_with(name=name, required=required, default=data["default"])

    def test__string_based_property_binary_format(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = {
            "type": "string",
            "format": "binary",
        }
        FileProperty = mocker.patch(f"{MODULE_NAME}.FileProperty")

        from openapi_python_client.openapi_parser.properties import _string_based_property

        p = _string_based_property(name=name, required=required, data=data)
        FileProperty.assert_called_once_with(name=name, required=required, default=None)
        assert p == FileProperty.return_value

        # Test optional values
        FileProperty.reset_mock()
        data["default"] = mocker.MagicMock()

        _string_based_property(
            name=name, required=required, data=data,
        )
        FileProperty.assert_called_once_with(name=name, required=required, default=data["default"])

    def test__string_based_property_unsupported_format(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = {
            "type": "string",
            "format": mocker.MagicMock(),
        }

        from openapi_python_client.openapi_parser.properties import _string_based_property

        with pytest.raises(ValueError):
            _string_based_property(name=name, required=required, data=data)
