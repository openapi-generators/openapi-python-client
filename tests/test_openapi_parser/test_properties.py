import pytest


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

    def test_get_type_string_fails_when_no_type_nor_reference(self, mocker):
        from openapi_python_client.openapi_parser.properties import ListProperty

        p = ListProperty(name="test", required=True, default=None, type=None, reference=None)

        with pytest.raises(ValueError):
            p.get_type_string()
