from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties import FloatProperty
from openapi_python_client.parser.properties.protocol import Value


def test_invalid_default():
    err = FloatProperty.build(
        default="not a float",
        description=None,
        example=None,
        required=False,
        python_name="not_a_float",
        name="not_a_float",
    )

    assert isinstance(err, PropertyError)


def test_convert_from_string():
    val = FloatProperty.convert_value("1.0")
    assert isinstance(val, Value)
    assert val == "1.0"
    assert FloatProperty.convert_value("1") == "1.0"


def test_convert_from_float():
    val = FloatProperty.convert_value(1.0)
    assert isinstance(val, Value)
    assert val == "1.0"
    assert FloatProperty.convert_value(1) == "1.0"


def test_invalid_type_default():
    err = FloatProperty.build(
        default=True,
        description=None,
        example=None,
        required=False,
        python_name="not_a_float",
        name="not_a_float",
    )

    assert isinstance(err, PropertyError)
