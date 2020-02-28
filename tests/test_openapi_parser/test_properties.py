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
        p = Property(name=name, required=True, default=None)
        get_type_string = mocker.patch.object(p, "get_type_string")

        assert p.to_string() == f"{name}: {get_type_string()}"
        p.required = False
        assert p.to_string() == f"{name}: {get_type_string()} = None"

        p.default = "TEST"
        assert p.to_string() == f"{name}: {get_type_string()} = TEST"

    def test_transform(self, mocker):
        from openapi_python_client.openapi_parser.properties import Property

        name = mocker.MagicMock()
        p = Property(name=name, required=True, default=None)
        assert p.transform() == name

    def test_constructor_from_dict(self, mocker):
        from openapi_python_client.openapi_parser.properties import Property

        name = mocker.MagicMock()
        p = Property(name=name, required=True, default=None)
        dict_name = mocker.MagicMock()

        assert p.constructor_from_dict(dict_name) == f'{dict_name}["{name}"]'

        p.required = False
        assert p.constructor_from_dict(dict_name) == f'{dict_name}.get("{name}")'


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


class TestListProperty:
    def test_get_type_string_when_type(self):
        from openapi_python_client.openapi_parser.properties import ListProperty

        p = ListProperty(name="test", required=True, default=None, type="MyTestType", reference=None)

        assert p.get_type_string() == "List[MyTestType]"
        p.required = False
        assert p.get_type_string() == "Optional[List[MyTestType]]"

    def test_get_type_string_when_reference(self, mocker):
        from openapi_python_client.openapi_parser.properties import ListProperty, Reference

        reference = mocker.MagicMock(autospec=Reference)
        reference.class_name = "MyTestClassName"
        p = ListProperty(name="test", required=True, default=None, type=None, reference=reference)

        assert p.get_type_string() == "List[MyTestClassName]"
        p.required = False
        assert p.get_type_string() == "Optional[List[MyTestClassName]]"

    def test_get_type_string_fails_when_no_type_nor_reference(self):
        from openapi_python_client.openapi_parser.properties import ListProperty

        p = ListProperty(name="test", required=True, default=None, type=None, reference=None)

        with pytest.raises(ValueError):
            p.get_type_string()


class TestEnumProperty:
    def test___post_init__(self, mocker):
        name = mocker.MagicMock()
        fake_reference = mocker.MagicMock(class_name="MyTestEnum")
        Reference = mocker.patch(f"{MODULE_NAME}.Reference", return_value=fake_reference)

        from openapi_python_client.openapi_parser.properties import EnumProperty

        enum_property = EnumProperty(
            name=name, required=True, default="second", values={"FIRST": "first", "SECOND": "second"}
        )

        Reference.assert_called_once_with(name)
        assert enum_property.default == "MyTestEnum.SECOND"

    def test_get_type_string(self, mocker):
        fake_reference = mocker.MagicMock(class_name="MyTestEnum")
        mocker.patch(f"{MODULE_NAME}.Reference", return_value=fake_reference)

        from openapi_python_client.openapi_parser.properties import EnumProperty

        enum_property = EnumProperty(name="test", required=True, default=None, values={})

        assert enum_property.get_type_string() == "MyTestEnum"
        enum_property.required = False
        assert enum_property.get_type_string() == "Optional[MyTestEnum]"

    def test_transform(self, mocker):
        name = mocker.MagicMock()
        mocker.patch(f"{MODULE_NAME}.Reference")

        from openapi_python_client.openapi_parser.properties import EnumProperty

        enum_property = EnumProperty(name=name, required=True, default=None, values={})

        assert enum_property.transform() == f"{name}.value"

    def test_constructor_from_dict(self, mocker):
        fake_reference = mocker.MagicMock(class_name="MyTestEnum")
        mocker.patch(f"{MODULE_NAME}.Reference", return_value=fake_reference)

        from openapi_python_client.openapi_parser.properties import EnumProperty

        enum_property = EnumProperty(name="test_enum", required=True, default=None, values={})

        assert (
            enum_property.constructor_from_dict("my_dict")
            == 'MyTestEnum(my_dict["test_enum"]) if "test_enum" in my_dict else None'
        )

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

    def test_transform(self, mocker):
        from openapi_python_client.openapi_parser.properties import RefProperty

        ref_property = RefProperty(name="super_unique_name", required=True, default=None, reference=mocker.MagicMock())

        assert ref_property.transform() == "super_unique_name.to_dict()"


class TestPropertyFromDict:
    def test_property_from_dict_enum(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = {
            "enum": mocker.MagicMock(),
        }
        EnumProperty = mocker.patch(f"{MODULE_NAME}.EnumProperty")

        from openapi_python_client.openapi_parser.properties import property_from_dict

        p = property_from_dict(name=name, required=required, data=data)

        EnumProperty.values_from_list.assert_called_once_with(data["enum"])
        EnumProperty.assert_called_once_with(
            name=name, required=required, values=EnumProperty.values_from_list(), default=None
        )
        assert p == EnumProperty()

        EnumProperty.reset_mock()
        data["default"] = mocker.MagicMock()

        property_from_dict(
            name=name, required=required, data=data,
        )
        EnumProperty.assert_called_once_with(
            name=name, required=required, values=EnumProperty.values_from_list(), default=data["default"]
        )

    def test_property_from_dict_ref(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = {
            "$ref": mocker.MagicMock(),
        }
        Reference = mocker.patch(f"{MODULE_NAME}.Reference")
        RefProperty = mocker.patch(f"{MODULE_NAME}.RefProperty")

        from openapi_python_client.openapi_parser.properties import property_from_dict

        p = property_from_dict(name=name, required=required, data=data)

        Reference.assert_called_once_with(data["$ref"])
        RefProperty.assert_called_once_with(name=name, required=required, reference=Reference(), default=None)
        assert p == RefProperty()

    def test_property_from_dict_string_no_format(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = {
            "type": "string",
        }
        StringProperty = mocker.patch(f"{MODULE_NAME}.StringProperty")

        from openapi_python_client.openapi_parser.properties import property_from_dict

        p = property_from_dict(name=name, required=required, data=data)

        StringProperty.assert_called_once_with(name=name, required=required, pattern=None, default=None)
        assert p == StringProperty()

        # Test optional values
        StringProperty.reset_mock()
        data["default"] = mocker.MagicMock()
        data["pattern"] = mocker.MagicMock()

        property_from_dict(
            name=name, required=required, data=data,
        )
        StringProperty.assert_called_once_with(
            name=name, required=required, pattern=data["pattern"], default=data["default"]
        )

    def test_property_from_dict_string_datetime_format(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = {
            "type": "string",
            "format": "date-time",
        }
        DateTimeProperty = mocker.patch(f"{MODULE_NAME}.DateTimeProperty")

        from openapi_python_client.openapi_parser.properties import property_from_dict

        p = property_from_dict(name=name, required=required, data=data)

        DateTimeProperty.assert_called_once_with(name=name, required=required, default=None)
        assert p == DateTimeProperty()

        # Test optional values
        DateTimeProperty.reset_mock()
        data["default"] = mocker.MagicMock()

        property_from_dict(
            name=name, required=required, data=data,
        )
        DateTimeProperty.assert_called_once_with(name=name, required=required, default=data["default"])

    def test_property_from_dict_string_unsupported_format(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = {
            "type": "string",
            "format": mocker.MagicMock(),
        }

        from openapi_python_client.openapi_parser.properties import property_from_dict

        with pytest.raises(ValueError):
            property_from_dict(name=name, required=required, data=data)

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

    def test_property_from_dict_ref_array(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        ref = mocker.MagicMock()
        data = {
            "type": "array",
            "items": {"$ref": ref},
        }
        ListProperty = mocker.patch(f"{MODULE_NAME}.ListProperty")
        Reference = mocker.patch(f"{MODULE_NAME}.Reference")

        from openapi_python_client.openapi_parser.properties import property_from_dict

        p = property_from_dict(name=name, required=required, data=data)

        Reference.assert_called_once_with(ref)
        ListProperty.assert_called_once_with(
            name=name, required=required, default=None, type=None, reference=Reference()
        )
        assert p == ListProperty()

    @pytest.mark.parametrize(
        "openapi_type,python_type",
        [("string", "str"), ("number", "float"), ("integer", "int"), ("boolean", "bool"), ("object", "Dict"),],
    )
    def test_property_from_dict_simple_array(self, mocker, openapi_type, python_type):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = {
            "type": "array",
            "items": {"type": openapi_type},
        }
        ListProperty = mocker.patch(f"{MODULE_NAME}.ListProperty")

        from openapi_python_client.openapi_parser.properties import property_from_dict

        p = property_from_dict(name=name, required=required, data=data)

        ListProperty.assert_called_once_with(
            name=name, required=required, default=None, type=python_type, reference=None
        )
        assert p == ListProperty()

    def test_property_from_dict_unsupported_type(self, mocker):
        name = mocker.MagicMock()
        required = mocker.MagicMock()
        data = {
            "type": mocker.MagicMock(),
        }

        from openapi_python_client.openapi_parser.properties import property_from_dict

        with pytest.raises(ValueError):
            property_from_dict(name=name, required=required, data=data)
