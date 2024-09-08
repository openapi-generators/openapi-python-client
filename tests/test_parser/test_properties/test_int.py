from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties import IntProperty
from openapi_python_client.parser.properties.protocol import Value
from openapi_python_client.utils import PythonIdentifier


def test_invalid_default():
    err = IntProperty.build(
        default="not a float",
        description=None,
        example=None,
        required=False,
        python_name="not_a_float",
        name="not_a_float",
    )

    assert isinstance(err, PropertyError)


def test_convert_from_string():
    assert IntProperty.convert_value("1") == Value(python_code="1", raw_value="1")


def test_invalid_type_default():
    err = IntProperty.build(
        default=True,
        description=None,
        example=None,
        required=False,
        python_name=PythonIdentifier("not_a_float", ""),
        name="not_a_float",
    )

    assert isinstance(err, PropertyError)
