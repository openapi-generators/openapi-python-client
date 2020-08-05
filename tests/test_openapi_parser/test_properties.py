import pytest

import openapi_python_client.schema as oai
from openapi_python_client.parser.errors import PropertyError

MODULE_NAME = "openapi_python_client.parser.properties"


class TestProperty:
    def test_get_type_string(self):
        from openapi_python_client.parser.properties import Property

        p = Property(name="test", required=True, default=None)
        p._type_string = "TestType"

        assert p.get_type_string() == "TestType"
        p.required = False
        assert p.get_type_string() == "Optional[TestType]"

    def test_to_string(self, mocker):
        from openapi_python_client.parser.properties import Property

        name = mocker.MagicMock()
        snake_case = mocker.patch("openapi_python_client.utils.snake_case")
        p = Property(name=name, required=True, default=None)
        get_type_string = mocker.patch.object(p, "get_type_string")

        assert p.to_string() == f"{snake_case(name)}: {get_type_string()}"
        p.required = False
        assert p.to_string() == f"{snake_case(name)}: {get_type_string()} = None"

        p.default = "TEST"
        assert p.to_string() == f"{snake_case(name)}: {get_type_string()} = TEST"

    def test_get_imports(self, mocker):
        from openapi_python_client.parser.properties import Property

        name = mocker.MagicMock()
        mocker.patch("openapi_python_client.utils.snake_case")
        p = Property(name=name, required=True, default=None)
        assert p.get_imports(prefix="") == set()

        p.required = False
        assert p.get_imports(prefix="") == {"from typing import Optional"}


class TestStringProperty:
    def test___post_init__(self):
        from openapi_python_client.parser.properties import StringProperty

        sp = StringProperty(name="test", required=True, default="A Default Value",)

        assert sp.default == '"A Default Value"'

    def test_get_type_string(self):
        from openapi_python_client.parser.properties import StringProperty

        p = StringProperty(name="test", required=True, default=None)

        assert p.get_type_string() == "str"
        p.required = False
        assert p.get_type_string() == "Optional[str]"


class TestDateTimeProperty:
    def test_get_imports(self, mocker):
        from openapi_python_client.parser.properties import DateTimeProperty

        name = mocker.MagicMock()
        mocker.patch("openapi_python_client.utils.snake_case")
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
    def test_get_imports(self, mocker):
        from openapi_python_client.parser.properties import DateProperty

        name = mocker.MagicMock()
        mocker.patch("openapi_python_client.utils.snake_case")
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
    def test_get_imports(self, mocker):
        from openapi_python_client.parser.properties import FileProperty

        name = mocker.MagicMock()
        mocker.patch("openapi_python_client.utils.snake_case")
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
        from openapi_python_client.parser.properties import ListProperty

        inner_property = mocker.MagicMock()
        inner_type_string = mocker.MagicMock()
        inner_property.get_type_string.return_value = inner_type_string
        p = ListProperty(name="test", required=True, default=None, inner_property=inner_property)

        assert p.get_type_string() == f"List[{inner_type_string}]"
        p.required = False
        assert p.get_type_string() == f"Optional[List[{inner_type_string}]]"

        p = ListProperty(name="test", required=True, default=[], inner_property=inner_property)
        assert p.default == f"field(default_factory=lambda: cast(List[{inner_type_string}], []))"

    def test_get_type_imports(self, mocker):
        from openapi_python_client.parser.properties import ListProperty

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

        p.default = mocker.MagicMock()
        assert p.get_imports(prefix=prefix) == {
            inner_import,
            "from typing import Optional",
            "from typing import List",
            "from typing import cast",
            "from dataclasses import field",
        }


class TestUnionProperty:
    def test_get_type_string(self, mocker):
        from openapi_python_client.parser.properties import UnionProperty

        inner_property_1 = mocker.MagicMock()
        inner_property_1.get_type_string.return_value = "inner_type_string_1"
        inner_property_2 = mocker.MagicMock()
        inner_property_2.get_type_string.return_value = "inner_type_string_2"
        p = UnionProperty(
            name="test", required=True, default=None, inner_properties=[inner_property_1, inner_property_2]
        )

        assert p.get_type_string() == "Union[inner_type_string_1, inner_type_string_2]"
        p.required = False
        assert p.get_type_string() == "Optional[Union[inner_type_string_1, inner_type_string_2]]"

    def test_get_type_imports(self, mocker):
        from openapi_python_client.parser.properties import UnionProperty

        inner_property_1 = mocker.MagicMock()
        inner_import_1 = mocker.MagicMock()
        inner_property_1.get_imports.return_value = {inner_import_1}
        inner_property_2 = mocker.MagicMock()
        inner_import_2 = mocker.MagicMock()
        inner_property_2.get_imports.return_value = {inner_import_2}
        prefix = mocker.MagicMock()
        p = UnionProperty(
            name="test", required=True, default=None, inner_properties=[inner_property_1, inner_property_2]
        )

        assert p.get_imports(prefix=prefix) == {
            inner_import_1,
            inner_import_2,
            "from typing import Union",
        }
        p.required = False
        assert p.get_imports(prefix=prefix) == {
            inner_import_1,
            inner_import_2,
            "from typing import Union",
            "from typing import Optional",
        }


class TestEnumProperty:
    def test___post_init__(self, mocker):
        name = mocker.MagicMock()

        snake_case = mocker.patch("openapi_python_client.utils.snake_case")
        fake_reference = mocker.MagicMock(class_name="MyTestEnum")
        deduped_reference = mocker.MagicMock(class_name="Deduped")
        from_ref = mocker.patch(
            f"{MODULE_NAME}.Reference.from_ref", side_effect=[fake_reference, deduped_reference, deduped_reference]
        )
        from openapi_python_client.parser import properties

        fake_dup_enum = mocker.MagicMock()
        properties._existing_enums = {"MyTestEnum": fake_dup_enum}
        values = {"FIRST": "first", "SECOND": "second"}

        enum_property = properties.EnumProperty(
            name=name, required=True, default="second", values=values, title="a_title",
        )

        assert enum_property.default == "Deduped.SECOND"
        assert enum_property.python_name == snake_case(name)
        from_ref.assert_has_calls([mocker.call("a_title"), mocker.call("MyTestEnum1")])
        assert enum_property.reference == deduped_reference
        assert properties._existing_enums == {"MyTestEnum": fake_dup_enum, "Deduped": enum_property}

        # Test encountering exactly the same Enum again
        assert (
            properties.EnumProperty(name=name, required=True, default="second", values=values, title="a_title",)
            == enum_property
        )
        assert properties._existing_enums == {"MyTestEnum": fake_dup_enum, "Deduped": enum_property}

        # What if an Enum exists with the same name, but has the same values? Don't dedupe that.
        fake_dup_enum.values = values
        from_ref.reset_mock()
        from_ref.side_effect = [fake_reference]
        enum_property = properties.EnumProperty(
            name=name, required=True, default="second", values=values, title="a_title",
        )
        assert enum_property.default == "MyTestEnum.SECOND"
        assert enum_property.python_name == snake_case(name)
        from_ref.assert_called_once_with("a_title")
        assert enum_property.reference == fake_reference
        assert len(properties._existing_enums) == 2

        properties._existing_enums = {}

    def test_get_type_string(self, mocker):
        fake_reference = mocker.MagicMock(class_name="MyTestEnum")
        mocker.patch(f"{MODULE_NAME}.Reference.from_ref", return_value=fake_reference)

        from openapi_python_client.parser import properties

        enum_property = properties.EnumProperty(name="test", required=True, default=None, values={}, title="a_title")

        assert enum_property.get_type_string() == "MyTestEnum"
        enum_property.required = False
        assert enum_property.get_type_string() == "Optional[MyTestEnum]"
        properties._existing_enums = {}

    def test_get_imports(self, mocker):
        fake_reference = mocker.MagicMock(class_name="MyTestEnum", module_name="my_test_enum")
        mocker.patch(f"{MODULE_NAME}.Reference.from_ref", return_value=fake_reference)
        prefix = mocker.MagicMock()

        from openapi_python_client.parser import properties

        enum_property = properties.EnumProperty(name="test", required=True, default=None, values={}, title="a_title")

        assert enum_property.get_imports(prefix=prefix) == {
            f"from {prefix}.{fake_reference.module_name} import {fake_reference.class_name}"
        }

        enum_property.required = False
        assert enum_property.get_imports(prefix=prefix) == {
            f"from {prefix}.{fake_reference.module_name} import {fake_reference.class_name}",
            "from typing import Optional",
        }
        properties._existing_enums = {}

    def test_values_from_list(self):
        from openapi_python_client.parser.properties import EnumProperty

        data = ["abc", "123", "a23", "1bc"]

        result = EnumProperty.values_from_list(data)

        assert result == {
            "ABC": "abc",
            "VALUE_1": "123",
            "A23": "a23",
            "VALUE_3": "1bc",
        }

    def test_values_from_list_duplicate(self):
        from openapi_python_client.parser.properties import EnumProperty

        data = ["abc", "123", "a23", "abc"]

        with pytest.raises(ValueError):
            EnumProperty.values_from_list(data)

    def test_get_all_enums(self, mocker):
        from openapi_python_client.parser import properties

        properties._existing_enums = mocker.MagicMock()
        assert properties.EnumProperty.get_all_enums() == properties._existing_enums
        properties._existing_enums = {}

    def test_get_enum(self):
        from openapi_python_client.parser import properties

        properties._existing_enums = {"test": "an enum"}
        assert properties.EnumProperty.get_enum("test") == "an enum"
        properties._existing_enums = {}


class TestRefProperty:
    def test_template(self, mocker):
        from openapi_python_client.parser.properties import RefProperty

        ref_property = RefProperty(
            name="test", required=True, default=None, reference=mocker.MagicMock(class_name="MyRefClass")
        )

        assert ref_property.template == "ref_property.pyi"

        mocker.patch(f"{MODULE_NAME}.EnumProperty.get_enum", return_value="an enum")

        assert ref_property.template == "enum_property.pyi"

    def test_get_type_string(self, mocker):
        from openapi_python_client.parser.properties import RefProperty

        ref_property = RefProperty(
            name="test", required=True, default=None, reference=mocker.MagicMock(class_name="MyRefClass")
        )

        assert ref_property.get_type_string() == "MyRefClass"

        ref_property.required = False
        assert ref_property.get_type_string() == "Optional[MyRefClass]"

    def test_get_imports(self, mocker):
        fake_reference = mocker.MagicMock(class_name="MyRefClass", module_name="my_test_enum")
        prefix = mocker.MagicMock()

        from openapi_python_client.parser.properties import RefProperty

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


class TestDictProperty:
    def test___post_init__(self):
        from openapi_python_client.parser.properties import DictProperty

        p = DictProperty(name="blah", required=True, default={})
        assert p.default == "field(default_factory=lambda: cast(Dict[Any, Any], {}))"

    def test_get_imports(self, mocker):
        from openapi_python_client.parser.properties import DictProperty

        name = mocker.MagicMock()
        mocker.patch("openapi_python_client.utils.snake_case")
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

        p.default = mocker.MagicMock()
        assert p.get_imports(prefix=prefix) == {
            "from typing import Optional",
            "from typing import Dict",
            "from typing import cast",
            "from dataclasses import field",
        }


class TestPropertyFromData:
    def test_property_from_data_enum(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = mocker.MagicMock(title=None)
        EnumProperty = mocker.patch(f"{MODULE_NAME}.EnumProperty")

        from openapi_python_client.parser.properties import property_from_data

        p = property_from_data(name=name, required=required, data=data)

        EnumProperty.values_from_list.assert_called_once_with(data.enum)
        EnumProperty.assert_called_once_with(
            name=name, required=required, values=EnumProperty.values_from_list(), default=data.default, title=name
        )
        assert p == EnumProperty()

        EnumProperty.reset_mock()
        data.title = mocker.MagicMock()

        property_from_data(
            name=name, required=required, data=data,
        )
        EnumProperty.assert_called_once_with(
            name=name, required=required, values=EnumProperty.values_from_list(), default=data.default, title=data.title
        )

    def test_property_from_data_ref(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Reference.construct(ref=mocker.MagicMock())
        from_ref = mocker.patch(f"{MODULE_NAME}.Reference.from_ref")
        RefProperty = mocker.patch(f"{MODULE_NAME}.RefProperty")

        from openapi_python_client.parser.properties import property_from_data

        p = property_from_data(name=name, required=required, data=data)

        from_ref.assert_called_once_with(data.ref)
        RefProperty.assert_called_once_with(name=name, required=required, reference=from_ref(), default=None)
        assert p == RefProperty()

    def test_property_from_data_string(self, mocker):
        _string_based_property = mocker.patch(f"{MODULE_NAME}._string_based_property")
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema.construct(type="string")
        from openapi_python_client.parser.properties import property_from_data

        p = property_from_data(name=name, required=required, data=data)

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
    def test_property_from_data_simple_types(self, mocker, openapi_type, python_type):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema.construct(type=openapi_type)
        clazz = mocker.patch(f"{MODULE_NAME}.{python_type}")

        from openapi_python_client.parser.properties import property_from_data

        p = property_from_data(name=name, required=required, data=data)

        clazz.assert_called_once_with(name=name, required=required, default=None)
        assert p == clazz()

        # Test optional values
        clazz.reset_mock()
        data.default = mocker.MagicMock()

        property_from_data(
            name=name, required=required, data=data,
        )
        clazz.assert_called_once_with(name=name, required=required, default=data.default)

    def test_property_from_data_array(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema(type="array", items={"type": "number", "default": "0.0"},)
        ListProperty = mocker.patch(f"{MODULE_NAME}.ListProperty")
        FloatProperty = mocker.patch(f"{MODULE_NAME}.FloatProperty")

        from openapi_python_client.parser.properties import property_from_data

        p = property_from_data(name=name, required=required, data=data)

        FloatProperty.assert_called_once_with(name=f"{name}_item", required=True, default="0.0")
        ListProperty.assert_called_once_with(
            name=name, required=required, default=None, inner_property=FloatProperty.return_value
        )
        assert p == ListProperty.return_value

    def test_property_from_data_array_no_items(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema(type="array")

        from openapi_python_client.parser.properties import property_from_data

        p = property_from_data(name=name, required=required, data=data)

        assert p == PropertyError(data=data, detail="type array must have items defined")

    def test_property_from_data_array_invalid_items(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema(type="array", items={},)

        from openapi_python_client.parser.properties import property_from_data

        p = property_from_data(name=name, required=required, data=data)

        assert p == PropertyError(data=oai.Schema(), detail=f"invalid data in items of array {name}")

    def test_property_from_data_union(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema(anyOf=[{"type": "number", "default": "0.0"}, {"type": "integer", "default": "0"},])
        UnionProperty = mocker.patch(f"{MODULE_NAME}.UnionProperty")
        FloatProperty = mocker.patch(f"{MODULE_NAME}.FloatProperty")
        IntProperty = mocker.patch(f"{MODULE_NAME}.IntProperty")

        from openapi_python_client.parser.properties import property_from_data

        p = property_from_data(name=name, required=required, data=data)

        FloatProperty.assert_called_once_with(name=name, required=required, default="0.0")
        IntProperty.assert_called_once_with(name=name, required=required, default="0")
        UnionProperty.assert_called_once_with(
            name=name,
            required=required,
            default=None,
            inner_properties=[FloatProperty.return_value, IntProperty.return_value],
        )
        assert p == UnionProperty.return_value

    def test_property_from_data_union_bad_type(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema(anyOf=[{}])

        from openapi_python_client.parser.properties import property_from_data

        p = property_from_data(name=name, required=required, data=data)

        assert p == PropertyError(detail=f"Invalid property in union {name}", data=oai.Schema())

    def test_property_from_data_unsupported_type(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema.construct(type=mocker.MagicMock())

        from openapi_python_client.parser.errors import PropertyError
        from openapi_python_client.parser.properties import property_from_data

        assert property_from_data(name=name, required=required, data=data) == PropertyError(
            data=data, detail=f"unknown type {data.type}"
        )

    def test_property_from_data_no_valid_props_in_data(self):
        from openapi_python_client.parser.errors import PropertyError
        from openapi_python_client.parser.properties import property_from_data

        data = oai.Schema()
        assert property_from_data(name="blah", required=True, data=data) == PropertyError(
            data=data, detail="Schemas must either have one of enum, anyOf, or type defined."
        )


class TestStringBasedProperty:
    def test__string_based_property_no_format(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema.construct(type="string")
        StringProperty = mocker.patch(f"{MODULE_NAME}.StringProperty")

        from openapi_python_client.parser.properties import _string_based_property

        p = _string_based_property(name=name, required=required, data=data)

        StringProperty.assert_called_once_with(name=name, required=required, pattern=None, default=None)
        assert p == StringProperty.return_value

        # Test optional values
        StringProperty.reset_mock()
        data.default = mocker.MagicMock()
        data.pattern = mocker.MagicMock()

        _string_based_property(
            name=name, required=required, data=data,
        )
        StringProperty.assert_called_once_with(name=name, required=required, pattern=data.pattern, default=data.default)

    def test__string_based_property_datetime_format(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema.construct(type="string", schema_format="date-time")
        DateTimeProperty = mocker.patch(f"{MODULE_NAME}.DateTimeProperty")

        from openapi_python_client.parser.properties import _string_based_property

        p = _string_based_property(name=name, required=required, data=data)

        DateTimeProperty.assert_called_once_with(name=name, required=required, default=None)
        assert p == DateTimeProperty.return_value

        # Test optional values
        DateTimeProperty.reset_mock()
        data.default = mocker.MagicMock()

        _string_based_property(
            name=name, required=required, data=data,
        )
        DateTimeProperty.assert_called_once_with(name=name, required=required, default=data.default)

    def test__string_based_property_date_format(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema.construct(type="string", schema_format="date")
        DateProperty = mocker.patch(f"{MODULE_NAME}.DateProperty")

        from openapi_python_client.parser.properties import _string_based_property

        p = _string_based_property(name=name, required=required, data=data)
        DateProperty.assert_called_once_with(name=name, required=required, default=None)
        assert p == DateProperty.return_value

        # Test optional values
        DateProperty.reset_mock()
        data.default = mocker.MagicMock()

        _string_based_property(
            name=name, required=required, data=data,
        )
        DateProperty.assert_called_once_with(name=name, required=required, default=data.default)

    def test__string_based_property_binary_format(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema.construct(type="string", schema_format="binary")
        FileProperty = mocker.patch(f"{MODULE_NAME}.FileProperty")

        from openapi_python_client.parser.properties import _string_based_property

        p = _string_based_property(name=name, required=required, data=data)
        FileProperty.assert_called_once_with(name=name, required=required, default=None)
        assert p == FileProperty.return_value

        # Test optional values
        FileProperty.reset_mock()
        data.default = mocker.MagicMock()

        _string_based_property(
            name=name, required=required, data=data,
        )
        FileProperty.assert_called_once_with(name=name, required=required, default=data.default)

    def test__string_based_property_unsupported_format(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema.construct(type="string", schema_format=mocker.MagicMock())
        StringProperty = mocker.patch(f"{MODULE_NAME}.StringProperty")

        from openapi_python_client.parser.properties import _string_based_property

        p = _string_based_property(name=name, required=required, data=data)

        StringProperty.assert_called_once_with(name=name, required=required, pattern=None, default=None)
        assert p == StringProperty.return_value

        # Test optional values
        StringProperty.reset_mock()
        data.default = mocker.MagicMock()
        data.pattern = mocker.MagicMock()

        _string_based_property(
            name=name, required=required, data=data,
        )
        StringProperty.assert_called_once_with(name=name, required=required, pattern=data.pattern, default=data.default)
