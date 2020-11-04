import pytest

import openapi_python_client.schema as oai
from openapi_python_client.parser.errors import ParseError, PropertyError, ValidationError

MODULE_NAME = "openapi_python_client.parser.properties"


class TestProperty:
    def test___post_init(self, mocker):
        from openapi_python_client.parser.properties import Property

        validate_default = mocker.patch(f"{MODULE_NAME}.Property._validate_default")

        Property(name="a name", required=True, default=None, nullable=False)
        validate_default.assert_not_called()

        Property(name="a name", required=True, default="the default value", nullable=False)
        validate_default.assert_called_with(default="the default value")

    def test_get_type_string(self):
        from openapi_python_client.parser.properties import Property

        p = Property(name="test", required=True, default=None, nullable=False)
        p._type_string = "TestType"

        base_type_string = f"TestType"

        assert p.get_type_string() == base_type_string

        p.nullable = True
        assert p.get_type_string() == f"Optional[{base_type_string}]"

        p.required = False
        assert p.get_type_string() == f"Union[Unset, Optional[{base_type_string}]]"

        p.nullable = False
        assert p.get_type_string() == f"Union[Unset, {base_type_string}]"

    def test_to_string(self, mocker):
        from openapi_python_client.parser.properties import Property

        name = "test"
        p = Property(name=name, required=True, default=None, nullable=False)
        get_type_string = mocker.patch.object(p, "get_type_string")

        assert p.to_string() == f"{name}: {get_type_string()}"

        p.required = False
        assert p.to_string() == f"{name}: {get_type_string()} = UNSET"

        p.required = True
        p.nullable = True
        assert p.to_string() == f"{name}: {get_type_string()} = None"

        p.default = "TEST"
        assert p.to_string() == f"{name}: {get_type_string()} = TEST"

    def test_get_imports(self):
        from openapi_python_client.parser.properties import Property

        p = Property(name="test", required=True, default=None, nullable=False)
        assert p.get_imports(prefix="") == set()

        p.required = False
        assert p.get_imports(prefix="") == {"from typing import Union, Optional", "from types import UNSET, Unset"}

    def test__validate_default(self):
        from openapi_python_client.parser.properties import Property

        # should be okay if default isn't specified
        p = Property(name="a name", required=True, default=None, nullable=False)

        with pytest.raises(ValidationError):
            p._validate_default("a default value")

        with pytest.raises(ValidationError):
            Property(name="a name", required=True, default="", nullable=False)


class TestStringProperty:
    def test_get_type_string(self):
        from openapi_python_client.parser.properties import StringProperty

        p = StringProperty(name="test", required=True, default=None, nullable=False)

        base_type_string = f"str"

        assert p.get_type_string() == base_type_string

        p.nullable = True
        assert p.get_type_string() == f"Optional[{base_type_string}]"

        p.required = False
        assert p.get_type_string() == f"Union[Unset, Optional[{base_type_string}]]"

        p.nullable = False
        assert p.get_type_string() == f"Union[Unset, {base_type_string}]"

    def test__validate_default(self):
        from openapi_python_client.parser.properties import StringProperty

        p = StringProperty(name="a name", required=True, default="the default value", nullable=False)
        assert p.default == "'the default value'"


class TestDateTimeProperty:
    def test_get_imports(self):
        from openapi_python_client.parser.properties import DateTimeProperty

        p = DateTimeProperty(name="test", required=True, default=None, nullable=False)
        assert p.get_imports(prefix="...") == {
            "import datetime",
            "from typing import cast",
            "from dateutil.parser import isoparse",
        }

        p.required = False
        assert p.get_imports(prefix="...") == {
            "import datetime",
            "from typing import cast",
            "from dateutil.parser import isoparse",
            "from typing import Union, Optional",
            "from ...types import UNSET, Unset",
        }

        p.nullable = True
        assert p.get_imports(prefix="...") == {
            "import datetime",
            "from typing import cast",
            "from dateutil.parser import isoparse",
            "from typing import Union, Optional",
            "from ...types import UNSET, Unset",
        }

    def test__validate_default(self):
        from openapi_python_client.parser.properties import DateTimeProperty

        with pytest.raises(ValidationError):
            DateTimeProperty(name="a name", required=True, default="not a datetime", nullable=False)

        p = DateTimeProperty(name="a name", required=True, default="2017-07-21T17:32:28Z", nullable=False)
        assert p.default == "isoparse('2017-07-21T17:32:28Z')"


class TestDateProperty:
    def test_get_imports(self):
        from openapi_python_client.parser.properties import DateProperty

        p = DateProperty(name="test", required=True, default=None, nullable=False)
        assert p.get_imports(prefix="...") == {
            "import datetime",
            "from typing import cast",
            "from dateutil.parser import isoparse",
        }

        p.required = False
        assert p.get_imports(prefix="...") == {
            "import datetime",
            "from typing import cast",
            "from dateutil.parser import isoparse",
            "from typing import Union, Optional",
            "from ...types import UNSET, Unset",
        }

        p.nullable = True
        assert p.get_imports(prefix="...") == {
            "import datetime",
            "from typing import cast",
            "from dateutil.parser import isoparse",
            "from typing import Union, Optional",
            "from ...types import UNSET, Unset",
        }

    def test__validate_default(self):
        from openapi_python_client.parser.properties import DateProperty

        with pytest.raises(ValidationError):
            DateProperty(name="a name", required=True, default="not a date", nullable=False)

        p = DateProperty(name="a name", required=True, default="1010-10-10", nullable=False)
        assert p.default == "isoparse('1010-10-10').date()"


class TestFileProperty:
    def test_get_imports(self):
        from openapi_python_client.parser.properties import FileProperty

        prefix = "..."
        p = FileProperty(name="test", required=True, default=None, nullable=False)
        assert p.get_imports(prefix=prefix) == {
            "from ...types import File",
        }

        p.required = False
        assert p.get_imports(prefix=prefix) == {
            "from ...types import File",
            "from typing import Union, Optional",
            "from ...types import UNSET, Unset",
        }

        p.nullable = True
        assert p.get_imports(prefix=prefix) == {
            "from ...types import File",
            "from typing import Union, Optional",
            "from ...types import UNSET, Unset",
        }

    def test__validate_default(self):
        from openapi_python_client.parser.properties import FileProperty

        # should be okay if default isn't specified
        FileProperty(name="a name", required=True, default=None, nullable=False)

        with pytest.raises(ValidationError):
            FileProperty(name="a name", required=True, default="", nullable=False)


class TestFloatProperty:
    def test__validate_default(self):
        from openapi_python_client.parser.properties import FloatProperty

        # should be okay if default isn't specified
        FloatProperty(name="a name", required=True, default=None, nullable=False)

        p = FloatProperty(name="a name", required=True, default="123.123", nullable=False)
        assert p.default == 123.123

        with pytest.raises(ValidationError):
            FloatProperty(name="a name", required=True, default="not a float", nullable=False)


class TestIntProperty:
    def test__validate_default(self):
        from openapi_python_client.parser.properties import IntProperty

        # should be okay if default isn't specified
        IntProperty(name="a name", required=True, default=None, nullable=False)

        p = IntProperty(name="a name", required=True, default="123", nullable=False)
        assert p.default == 123

        with pytest.raises(ValidationError):
            IntProperty(name="a name", required=True, default="not an int", nullable=False)


class TestBooleanProperty:
    def test__validate_default(self):
        from openapi_python_client.parser.properties import BooleanProperty

        # should be okay if default isn't specified
        BooleanProperty(name="a name", required=True, default=None, nullable=False)

        p = BooleanProperty(name="a name", required=True, default="Literally anything will work", nullable=False)
        assert p.default == True


class TestListProperty:
    def test_get_type_string(self, mocker):
        from openapi_python_client.parser.properties import ListProperty

        inner_property = mocker.MagicMock()
        inner_type_string = mocker.MagicMock()
        inner_property.get_type_string.return_value = inner_type_string
        p = ListProperty(name="test", required=True, default=None, inner_property=inner_property, nullable=False)

        base_type_string = f"List[{inner_type_string}]"

        assert p.get_type_string() == base_type_string

        p.nullable = True
        assert p.get_type_string() == f"Optional[{base_type_string}]"

        p.required = False
        assert p.get_type_string() == f"Union[Unset, Optional[{base_type_string}]]"

        p.nullable = False
        assert p.get_type_string() == f"Union[Unset, {base_type_string}]"

    def test_get_type_imports(self, mocker):
        from openapi_python_client.parser.properties import ListProperty

        inner_property = mocker.MagicMock()
        inner_import = mocker.MagicMock()
        inner_property.get_imports.return_value = {inner_import}
        prefix = "..."
        p = ListProperty(name="test", required=True, default=None, inner_property=inner_property, nullable=False)

        assert p.get_imports(prefix=prefix) == {
            inner_import,
            "from typing import List",
        }

        p.required = False
        assert p.get_imports(prefix=prefix) == {
            inner_import,
            "from typing import List",
            "from typing import Union, Optional",
            "from ...types import UNSET, Unset",
        }

        p.nullable = True
        assert p.get_imports(prefix=prefix) == {
            inner_import,
            "from typing import List",
            "from typing import Union, Optional",
            "from ...types import UNSET, Unset",
        }

    def test__validate_default(self, mocker):
        from openapi_python_client.parser.properties import ListProperty

        inner_property = mocker.MagicMock()

        p = ListProperty(name="a name", required=True, default=["x"], inner_property=inner_property, nullable=False)
        assert p.default is None


class TestUnionProperty:
    def test_get_type_string(self, mocker):
        from openapi_python_client.parser.properties import UnionProperty

        inner_property_1 = mocker.MagicMock()
        inner_property_1.get_type_string.return_value = "inner_type_string_1"
        inner_property_2 = mocker.MagicMock()
        inner_property_2.get_type_string.return_value = "inner_type_string_2"
        p = UnionProperty(
            name="test",
            required=True,
            default=None,
            inner_properties=[inner_property_1, inner_property_2],
            nullable=False,
        )

        base_type_string = f"Union[inner_type_string_1, inner_type_string_2]"

        assert p.get_type_string() == base_type_string

        p.nullable = True
        assert p.get_type_string() == f"Optional[{base_type_string}]"

        p.required = False
        assert p.get_type_string() == f"Union[Unset, Optional[{base_type_string}]]"

        p.nullable = False
        assert p.get_type_string() == f"Union[Unset, {base_type_string}]"

    def test_get_type_imports(self, mocker):
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
            "from typing import Union",
        }

        p.required = False
        assert p.get_imports(prefix=prefix) == {
            inner_import_1,
            inner_import_2,
            "from typing import Union",
            "from typing import Union, Optional",
            "from ...types import UNSET, Unset",
        }

        p.nullable = True
        assert p.get_imports(prefix=prefix) == {
            inner_import_1,
            inner_import_2,
            "from typing import Union",
            "from typing import Union, Optional",
            "from ...types import UNSET, Unset",
        }

    def test__validate_default(self, mocker):
        from openapi_python_client.parser.properties import UnionProperty

        inner_property_1 = mocker.MagicMock()
        inner_property_1.get_type_string.return_value = "inner_type_string_1"
        inner_property_1._validate_default.side_effect = ValidationError()
        inner_property_2 = mocker.MagicMock()
        inner_property_2.get_type_string.return_value = "inner_type_string_2"
        inner_property_2._validate_default.return_value = "the default value"
        p = UnionProperty(
            name="test",
            required=True,
            default="a value",
            inner_properties=[inner_property_1, inner_property_2],
            nullable=False,
        )

        assert p.default == "the default value"

        inner_property_2._validate_default.side_effect = ValidationError()

        with pytest.raises(ValidationError):
            UnionProperty(
                name="test",
                required=True,
                default="a value",
                inner_properties=[inner_property_1, inner_property_2],
                nullable=False,
            )


class TestEnumProperty:
    def test___post_init__(self, mocker):
        name = "test"

        fake_reference = mocker.MagicMock(class_name="MyTestEnum")
        deduped_reference = mocker.MagicMock(class_name="Deduped")
        from_ref = mocker.patch(
            f"{MODULE_NAME}.Reference.from_ref", side_effect=[fake_reference, deduped_reference, deduped_reference]
        )
        from openapi_python_client.parser import properties

        fake_dup_enum = mocker.MagicMock()
        values = {"FIRST": "first", "SECOND": "second"}

        enum_property = properties.EnumProperty(
            name=name,
            required=True,
            default="second",
            values=values,
            title="a_title",
            nullable=False,
            existing_enums={"MyTestEnum": fake_dup_enum},
        )

        assert enum_property.default == "Deduped.SECOND"
        assert enum_property.python_name == name
        from_ref.assert_has_calls([mocker.call("a_title"), mocker.call("MyTestEnum1")])
        assert enum_property.reference == deduped_reference

        # Test encountering exactly the same Enum again
        assert (
            properties.EnumProperty(
                name=name,
                required=True,
                default="second",
                values=values,
                title="a_title",
                nullable=False,
                existing_enums={"MyTestEnum": fake_dup_enum, "Deduped": enum_property},
            )
            == enum_property
        )

        # What if an Enum exists with the same name, but has the same values? Don't dedupe that.
        fake_dup_enum.values = values
        from_ref.reset_mock()
        from_ref.side_effect = [fake_reference]
        enum_property = properties.EnumProperty(
            name=name,
            required=True,
            default="second",
            values=values,
            title="a_title",
            nullable=False,
            existing_enums={"MyTestEnum": fake_dup_enum, "Deduped": enum_property},
        )
        assert enum_property.default == "MyTestEnum.SECOND"
        assert enum_property.python_name == name
        from_ref.assert_called_once_with("a_title")
        assert enum_property.reference == fake_reference

    def test_get_type_string(self, mocker):
        fake_reference = mocker.MagicMock(class_name="MyTestEnum")
        mocker.patch(f"{MODULE_NAME}.Reference.from_ref", return_value=fake_reference)

        from openapi_python_client.parser import properties

        p = properties.EnumProperty(
            name="test", required=True, default=None, values={}, title="a_title", nullable=False, existing_enums={}
        )

        base_type_string = f"MyTestEnum"

        assert p.get_type_string() == base_type_string

        p.nullable = True
        assert p.get_type_string() == f"Optional[{base_type_string}]"

        p.required = False
        assert p.get_type_string() == f"Union[Unset, Optional[{base_type_string}]]"

        p.nullable = False
        assert p.get_type_string() == f"Union[Unset, {base_type_string}]"

    def test_get_imports(self, mocker):
        fake_reference = mocker.MagicMock(class_name="MyTestEnum", module_name="my_test_enum")
        mocker.patch(f"{MODULE_NAME}.Reference.from_ref", return_value=fake_reference)
        prefix = "..."

        from openapi_python_client.parser import properties

        enum_property = properties.EnumProperty(
            name="test", required=True, default=None, values={}, title="a_title", nullable=False, existing_enums={}
        )

        assert enum_property.get_imports(prefix=prefix) == {
            f"from {prefix}models.{fake_reference.module_name} import {fake_reference.class_name}",
        }

        enum_property.required = False
        assert enum_property.get_imports(prefix=prefix) == {
            f"from {prefix}models.{fake_reference.module_name} import {fake_reference.class_name}",
            "from typing import Union, Optional",
            "from ...types import UNSET, Unset",
        }

        enum_property.nullable = True
        assert enum_property.get_imports(prefix=prefix) == {
            f"from {prefix}models.{fake_reference.module_name} import {fake_reference.class_name}",
            "from typing import Union, Optional",
            "from ...types import UNSET, Unset",
        }

    def test_values_from_list(self):
        from openapi_python_client.parser.properties import EnumProperty

        data = ["abc", "123", "a23", "1bc", 4, -3, "a Thing WIth spaces"]

        result = EnumProperty.values_from_list(data)

        assert result == {
            "ABC": "abc",
            "VALUE_1": "123",
            "A23": "a23",
            "VALUE_3": "1bc",
            "VALUE_4": 4,
            "VALUE_NEGATIVE_3": -3,
            "A_THING_WITH_SPACES": "a Thing WIth spaces",
        }

    def test_values_from_list_duplicate(self):
        from openapi_python_client.parser.properties import EnumProperty

        data = ["abc", "123", "a23", "abc"]

        with pytest.raises(ValueError):
            EnumProperty.values_from_list(data)

    def test__validate_default(self, mocker):
        fake_reference = mocker.MagicMock(class_name="MyTestEnum", module_name="my_test_enum")
        mocker.patch(f"{MODULE_NAME}.Reference.from_ref", return_value=fake_reference)

        from openapi_python_client.parser import properties

        enum_property = properties.EnumProperty(
            name="test",
            required=True,
            default="test",
            values={"TEST": "test"},
            title="a_title",
            nullable=False,
            existing_enums={},
        )
        assert enum_property.default == "MyTestEnum.TEST"

        with pytest.raises(ValidationError):
            properties.EnumProperty(
                name="test",
                required=True,
                default="bad_val",
                values={"TEST": "test"},
                title="a_title",
                nullable=False,
                existing_enums={},
            )


# class TestRefProperty:
#     def test_template(self, mocker):
#         from openapi_python_client.parser.properties import RefProperty
#
#         ref_property = RefProperty(
#             name="test",
#             required=True,
#             default=None,
#             reference=mocker.MagicMock(class_name="MyRefClass"),
#             nullable=False,
#         )
#
#         assert ref_property.template == "ref_property.pyi"
#
#         mocker.patch(f"{MODULE_NAME}.EnumProperty.get_enum", return_value="an enum")
#
#         assert ref_property.template == "enum_property.pyi"
#
#     def test_get_type_string(self, mocker):
#         from openapi_python_client.parser.properties import RefProperty
#
#         ref_property = RefProperty(
#             name="test",
#             required=True,
#             default=None,
#             reference=mocker.MagicMock(class_name="MyRefClass"),
#             nullable=False,
#         )
#
#         assert ref_property.get_type_string() == "MyRefClass"
#
#         ref_property.required = False
#         assert ref_property.get_type_string() == "Optional[MyRefClass]"
#
#     def test_get_imports(self, mocker):
#         fake_reference = mocker.MagicMock(class_name="MyRefClass", module_name="my_test_enum")
#         prefix = mocker.MagicMock()
#
#         from openapi_python_client.parser.properties import RefProperty
#
#         p = RefProperty(name="test", required=True, default=None, reference=fake_reference, nullable=False)
#
#         assert p.get_imports(prefix=prefix) == {
#             f"from {prefix}models.{fake_reference.module_name} import {fake_reference.class_name}",
#             "from typing import Dict",
#             "from typing import cast",
#         }
#
#         p.required = False
#         assert p.get_imports(prefix=prefix) == {
#             f"from {prefix}models.{fake_reference.module_name} import {fake_reference.class_name}",
#             "from typing import Dict",
#             "from typing import cast",
#             "from typing import Optional",
#         }
#
#     def test__validate_default(self, mocker):
#         from openapi_python_client.parser.properties import RefProperty
#
#         with pytest.raises(ValidationError):
#             RefProperty(name="a name", required=True, default="", reference=mocker.MagicMock(), nullable=False)
#
#         enum_property = mocker.MagicMock()
#         enum_property._validate_default.return_value = "val1"
#         mocker.patch(f"{MODULE_NAME}.EnumProperty.get_enum", return_value=enum_property)
#         p = RefProperty(name="a name", required=True, default="", reference=mocker.MagicMock(), nullable=False)
#         assert p.default == "val1"


class TestDictProperty:
    def test_get_imports(self, mocker):
        from openapi_python_client.parser.properties import DictProperty

        prefix = "..."
        p = DictProperty(name="test", required=True, default=None, nullable=False)
        assert p.get_imports(prefix=prefix) == {
            "from typing import Dict",
        }

        p.required = False
        assert p.get_imports(prefix=prefix) == {
            "from typing import Dict",
            "from typing import Union, Optional",
            "from ...types import UNSET, Unset",
        }

        p.nullable = False
        assert p.get_imports(prefix=prefix) == {
            "from typing import Dict",
            "from typing import Union, Optional",
            "from ...types import UNSET, Unset",
        }

        p.default = mocker.MagicMock()
        assert p.get_imports(prefix=prefix) == {
            "from typing import Dict",
            "from typing import cast",
            "from dataclasses import field",
            "from typing import Union, Optional",
            "from ...types import UNSET, Unset",
        }

    def test__validate_default(self):
        from openapi_python_client.parser.properties import DictProperty

        p = DictProperty(name="a name", required=True, default={"key": "value"}, nullable=False)

        assert p.default is None


class TestPropertyFromData:
    def test_property_from_data_enum(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = mocker.MagicMock(title=None)
        EnumProperty = mocker.patch(f"{MODULE_NAME}.EnumProperty")
        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=name)

        from openapi_python_client.parser.properties import Schemas, property_from_data

        schemas = Schemas(enums={"blah": mocker.MagicMock()})

        prop, new_schemas = property_from_data(name=name, required=required, data=data, schemas=schemas)

        EnumProperty.values_from_list.assert_called_once_with(data.enum)
        EnumProperty.assert_called_once_with(
            name=name,
            required=required,
            values=EnumProperty.values_from_list(),
            default=data.default,
            title=name,
            nullable=data.nullable,
            existing_enums=schemas.enums,
        )
        assert prop == EnumProperty.return_value
        assert schemas != new_schemas, "Provided Schemas was mutated"
        assert new_schemas.enums == {
            "blah": new_schemas.enums["blah"],
            EnumProperty.return_value.reference.class_name: EnumProperty.return_value,
        }

    def test_property_from_data_ref_enum(self, mocker):
        from openapi_python_client.parser.properties import Schemas, property_from_data

        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Reference.construct(ref=mocker.MagicMock())
        from_ref = mocker.patch(f"{MODULE_NAME}.Reference.from_ref")
        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=name)
        enum = mocker.MagicMock()
        schemas = Schemas(enums={from_ref.return_value.class_name: enum})

        prop, new_schemas = property_from_data(name=name, required=required, data=data, schemas=schemas)

        from_ref.assert_called_once_with(data.ref)
        assert prop == enum
        assert schemas == new_schemas

    def test_property_from_data_ref_model(self, mocker):
        from openapi_python_client.parser.properties import Schemas, property_from_data

        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Reference.construct(ref=mocker.MagicMock())
        from_ref = mocker.patch(f"{MODULE_NAME}.Reference.from_ref")
        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=name)
        model = mocker.MagicMock()
        schemas = Schemas(models={from_ref.return_value.class_name: model})

        prop, new_schemas = property_from_data(name=name, required=required, data=data, schemas=schemas)

        from_ref.assert_called_once_with(data.ref)
        assert prop == model
        assert schemas == new_schemas

    def test_property_from_data_ref_not_found(self, mocker):
        from openapi_python_client.parser.properties import PropertyError, Schemas, property_from_data

        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Reference.construct(ref=mocker.MagicMock())
        from_ref = mocker.patch(f"{MODULE_NAME}.Reference.from_ref")
        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=name)
        schemas = Schemas()

        prop, new_schemas = property_from_data(name=name, required=required, data=data, schemas=schemas)

        from_ref.assert_called_once_with(data.ref)
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

        p, new_schemas = property_from_data(name=name, required=required, data=data, schemas=schemas)

        assert p == _string_based_property.return_value
        assert schemas == new_schemas
        _string_based_property.assert_called_once_with(name=name, required=required, data=data)

    @pytest.mark.parametrize(
        "openapi_type,python_type",
        [
            ("number", "FloatProperty"),
            ("integer", "IntProperty"),
            ("boolean", "BooleanProperty"),
        ],
    )
    def test_property_from_data_simple_types(self, mocker, openapi_type, python_type):
        from openapi_python_client.parser.properties import Schemas, property_from_data

        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema.construct(type=openapi_type)
        clazz = mocker.patch(f"{MODULE_NAME}.{python_type}")
        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=name)
        schemas = Schemas()

        p, new_schemas = property_from_data(name=name, required=required, data=data, schemas=schemas)

        clazz.assert_called_once_with(name=name, required=required, default=None, nullable=False)
        assert p == clazz.return_value
        assert new_schemas == schemas

        # Test optional values
        clazz.reset_mock()
        data.default = mocker.MagicMock()
        data.nullable = mocker.MagicMock()

        property_from_data(
            name=name,
            required=required,
            data=data,
            schemas=schemas,
        )
        clazz.assert_called_once_with(name=name, required=required, default=data.default, nullable=data.nullable)

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

        response = property_from_data(name=name, required=required, data=data, schemas=schemas)

        assert response == build_list_property.return_value
        build_list_property.assert_called_once_with(data=data, name=name, required=required, schemas=schemas)

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

        response = property_from_data(name=name, required=required, data=data, schemas=schemas)

        assert response == build_union_property.return_value
        build_union_property.assert_called_once_with(data=data, name=name, required=required, schemas=schemas)

    def test_property_from_data_unsupported_type(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema.construct(type=mocker.MagicMock())

        from openapi_python_client.parser.errors import PropertyError
        from openapi_python_client.parser.properties import Schemas, property_from_data

        assert property_from_data(name=name, required=required, data=data, schemas=Schemas()) == (
            PropertyError(data=data, detail=f"unknown type {data.type}"),
            Schemas(),
        )

    def test_property_from_data_no_valid_props_in_data(self):
        from openapi_python_client.parser.errors import PropertyError
        from openapi_python_client.parser.properties import Schemas, property_from_data

        schemas = Schemas()
        data = oai.Schema()

        err, new_schemas = property_from_data(name="blah", required=True, data=data, schemas=schemas)

        assert err == PropertyError(data=data, detail="Schemas must either have one of enum, anyOf, or type defined.")
        assert new_schemas == schemas

    def test_property_from_data_validation_error(self, mocker):
        from openapi_python_client.parser.errors import PropertyError
        from openapi_python_client.parser.properties import Schemas, property_from_data

        mocker.patch(f"{MODULE_NAME}._property_from_data").side_effect = ValidationError()
        schemas = Schemas()

        data = oai.Schema()
        err, new_schemas = property_from_data(name="blah", required=True, data=data, schemas=schemas)
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

        p, new_schemas = properties.build_list_property(name=name, required=required, data=data, schemas=schemas)

        assert p == PropertyError(data=data, detail="type array must have items defined")
        assert new_schemas == schemas
        property_from_data.assert_not_called()

    def test_build_list_property_invalid_items(self, mocker):
        from openapi_python_client.parser import properties

        name = mocker.MagicMock()
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

        p, new_schemas = properties.build_list_property(name=name, required=required, data=data, schemas=schemas)

        assert p == PropertyError(data="blah", detail=f"invalid data in items of array {name}")
        assert new_schemas == second_schemas
        assert schemas != new_schemas, "Schema was mutated"
        property_from_data.assert_called_once_with(name=f"{name}_item", required=True, data=data.items, schemas=schemas)

    def test_build_list_property(self, mocker):
        from openapi_python_client.parser import properties

        name = mocker.MagicMock()
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

        p, new_schemas = properties.build_list_property(name=name, required=required, data=data, schemas=schemas)

        assert isinstance(p, properties.ListProperty)
        assert p.inner_property == property_from_data.return_value[0]
        assert new_schemas == second_schemas
        assert schemas != new_schemas, "Schema was mutated"
        property_from_data.assert_called_once_with(name=f"{name}_item", required=True, data=data.items, schemas=schemas)


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

        from openapi_python_client.parser.properties import property_from_data

        p = property_from_data(name=name, required=required, data=data)

        FloatProperty.assert_called_once_with(name=name, required=required, default="0.0", nullable=False)
        IntProperty.assert_called_once_with(name=name, required=required, default="0", nullable=False)
        UnionProperty.assert_called_once_with(
            name=name,
            required=required,
            default=None,
            inner_properties=[FloatProperty.return_value, IntProperty.return_value],
            nullable=False,
        )
        assert p == UnionProperty.return_value

    def test_property_from_data_union_bad_type(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema(anyOf=[{}])
        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=name)

        from openapi_python_client.parser.properties import property_from_data

        p = property_from_data(name=name, required=required, data=data)

        assert p == PropertyError(detail=f"Invalid property in union {name}", data=oai.Schema())


class TestStringBasedProperty:
    def test__string_based_property_no_format(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema.construct(type="string", nullable=mocker.MagicMock())
        StringProperty = mocker.patch(f"{MODULE_NAME}.StringProperty")

        from openapi_python_client.parser.properties import _string_based_property

        p = _string_based_property(name=name, required=required, data=data)

        StringProperty.assert_called_once_with(
            name=name, required=required, pattern=None, default=None, nullable=data.nullable
        )
        assert p == StringProperty.return_value

        # Test optional values
        StringProperty.reset_mock()
        data.default = mocker.MagicMock()
        data.pattern = mocker.MagicMock()

        _string_based_property(
            name=name,
            required=required,
            data=data,
        )
        StringProperty.assert_called_once_with(
            name=name, required=required, pattern=data.pattern, default=data.default, nullable=data.nullable
        )

    def test__string_based_property_datetime_format(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema.construct(type="string", schema_format="date-time", nullable=mocker.MagicMock())
        DateTimeProperty = mocker.patch(f"{MODULE_NAME}.DateTimeProperty")

        from openapi_python_client.parser.properties import _string_based_property

        p = _string_based_property(name=name, required=required, data=data)

        DateTimeProperty.assert_called_once_with(name=name, required=required, default=None, nullable=data.nullable)
        assert p == DateTimeProperty.return_value

        # Test optional values
        DateTimeProperty.reset_mock()
        data.default = mocker.MagicMock()

        _string_based_property(
            name=name,
            required=required,
            data=data,
        )
        DateTimeProperty.assert_called_once_with(
            name=name, required=required, default=data.default, nullable=data.nullable
        )

    def test__string_based_property_date_format(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema.construct(type="string", schema_format="date", nullable=mocker.MagicMock())
        DateProperty = mocker.patch(f"{MODULE_NAME}.DateProperty")

        from openapi_python_client.parser.properties import _string_based_property

        p = _string_based_property(name=name, required=required, data=data)
        DateProperty.assert_called_once_with(name=name, required=required, default=None, nullable=data.nullable)
        assert p == DateProperty.return_value

        # Test optional values
        DateProperty.reset_mock()
        data.default = mocker.MagicMock()

        _string_based_property(
            name=name,
            required=required,
            data=data,
        )
        DateProperty.assert_called_once_with(name=name, required=required, default=data.default, nullable=data.nullable)

    def test__string_based_property_binary_format(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema.construct(type="string", schema_format="binary", nullable=mocker.MagicMock())
        FileProperty = mocker.patch(f"{MODULE_NAME}.FileProperty")

        from openapi_python_client.parser.properties import _string_based_property

        p = _string_based_property(name=name, required=required, data=data)
        FileProperty.assert_called_once_with(name=name, required=required, default=None, nullable=data.nullable)
        assert p == FileProperty.return_value

        # Test optional values
        FileProperty.reset_mock()
        data.default = mocker.MagicMock()

        _string_based_property(
            name=name,
            required=required,
            data=data,
        )
        FileProperty.assert_called_once_with(name=name, required=required, default=data.default, nullable=data.nullable)

    def test__string_based_property_unsupported_format(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = oai.Schema.construct(type="string", schema_format=mocker.MagicMock())
        data.nullable = mocker.MagicMock()
        StringProperty = mocker.patch(f"{MODULE_NAME}.StringProperty")

        from openapi_python_client.parser.properties import _string_based_property

        p = _string_based_property(name=name, required=required, data=data)

        StringProperty.assert_called_once_with(
            name=name, required=required, pattern=None, default=None, nullable=data.nullable
        )
        assert p == StringProperty.return_value

        # Test optional values
        StringProperty.reset_mock()
        data.default = mocker.MagicMock()
        data.pattern = mocker.MagicMock()

        _string_based_property(
            name=name,
            required=required,
            data=data,
        )
        StringProperty.assert_called_once_with(
            name=name, required=required, pattern=data.pattern, default=data.default, nullable=data.nullable
        )


# def test_model_from_data(mocker):
#     from openapi_python_client.parser.properties import Property
#
#     in_data = oai.Schema.construct(
#         title=mocker.MagicMock(),
#         description=mocker.MagicMock(),
#         required=["RequiredEnum"],
#         properties={
#             "RequiredEnum": mocker.MagicMock(),
#             "OptionalDateTime": mocker.MagicMock(),
#         },
#     )
#     required_property = mocker.MagicMock(autospec=Property)
#     required_imports = mocker.MagicMock()
#     required_property.get_imports.return_value = {required_imports}
#     optional_property = mocker.MagicMock(autospec=Property)
#     optional_imports = mocker.MagicMock()
#     optional_property.get_imports.return_value = {optional_imports}
#     property_from_data = mocker.patch(
#         f"{MODULE_NAME}.property_from_data",
#         side_effect=[required_property, optional_property],
#     )
#     from_ref = mocker.patch(f"{MODULE_NAME}.Reference.from_ref")
#
#     from openapi_python_client.parser.properties import model_from_data
#
#     result = model_from_data(data=in_data, name=mocker.MagicMock())
#
#     from_ref.assert_called_once_with(in_data.title)
#     property_from_data.assert_has_calls(
#         [
#             mocker.call(name="RequiredEnum", required=True, data=in_data.properties["RequiredEnum"]),
#             mocker.call(name="OptionalDateTime", required=False, data=in_data.properties["OptionalDateTime"]),
#         ]
#     )
#     required_property.get_imports.assert_called_once_with(prefix="..")
#     optional_property.get_imports.assert_called_once_with(prefix="..")
#     assert result == Model(
#         reference=from_ref(),
#         required_properties=[required_property],
#         optional_properties=[optional_property],
#         relative_imports={
#             required_imports,
#             optional_imports,
#         },
#         description=in_data.description,
#     )
#
#
# def test_model_from_data_property_parse_error(mocker):
#     in_data = oai.Schema.construct(
#         title=mocker.MagicMock(),
#         description=mocker.MagicMock(),
#         required=["RequiredEnum"],
#         properties={
#             "RequiredEnum": mocker.MagicMock(),
#             "OptionalDateTime": mocker.MagicMock(),
#         },
#     )
#     parse_error = ParseError(data=mocker.MagicMock())
#     property_from_data = mocker.patch(
#         f"{MODULE_NAME}.property_from_data",
#         return_value=parse_error,
#     )
#     from_ref = mocker.patch(f"{MODULE_NAME}.Reference.from_ref")
#
#     from openapi_python_client.parser.model import model_from_data
#
#     result = model_from_data(data=in_data, name=mocker.MagicMock())
#
#     from_ref.assert_called_once_with(in_data.title)
#     property_from_data.assert_called_once_with(
#         name="RequiredEnum", required=True, data=in_data.properties["RequiredEnum"]
#     )
#
#     assert result == parse_error


def test_build_schemas(mocker):
    build_model_property = mocker.patch(f"{MODULE_NAME}.build_model_property")
    in_data = {"1": mocker.MagicMock(enum=None), "2": mocker.MagicMock(enum=None), "3": mocker.MagicMock(enum=None)}
    model_1 = mocker.MagicMock()
    schemas_1 = mocker.MagicMock()
    model_2 = mocker.MagicMock()
    schemas_2 = mocker.MagicMock()
    error = PropertyError()
    schemas_3 = mocker.MagicMock(errors=[])
    build_model_property.side_effect = [(model_1, schemas_1), (model_2, schemas_2), (error, schemas_3)]

    from openapi_python_client.parser.properties import Schemas, build_schemas

    result = build_schemas(components=in_data)

    build_model_property.assert_has_calls(
        [
            mocker.call(data=in_data["1"], name="1", schemas=Schemas(), required=True),
            mocker.call(data=in_data["2"], name="2", schemas=schemas_1, required=True),
            mocker.call(data=in_data["3"], name="3", schemas=schemas_2, required=True),
        ]
    )
    assert result == schemas_3
    assert result.errors == [error]


def test_build_parse_error_on_reference():
    from openapi_python_client.parser.openapi import build_schemas

    ref_schema = oai.Reference.construct()
    in_data = {"1": ref_schema}
    result = build_schemas(components=in_data)
    assert result.errors[0] == PropertyError(data=ref_schema, detail="Reference schemas are not supported.")


def test_build_enums(mocker):
    from openapi_python_client.parser.openapi import build_schemas

    build_model_property = mocker.patch(f"{MODULE_NAME}.build_model_property")
    schemas = mocker.MagicMock()
    build_enum_property = mocker.patch(f"{MODULE_NAME}.build_enum_property", return_value=(mocker.MagicMock(), schemas))
    in_data = {"1": mocker.MagicMock(enum=["val1", "val2", "val3"])}

    build_schemas(components=in_data)

    build_enum_property.assert_called()
    build_model_property.assert_not_called()
