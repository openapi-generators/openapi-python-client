from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties import DateProperty
from openapi_python_client.parser.properties.protocol import Value


def test_invalid_default_value():
    err = DateProperty.build(
        default="not a date",
        description=None,
        example=None,
        required=False,
        python_name="not_a_date",
        name="not_a_date",
    )

    assert isinstance(err, PropertyError)


def test_default_with_bad_type():
    err = DateProperty.build(
        default=123,
        description=None,
        example=None,
        required=False,
        python_name="not_a_date",
        name="not_a_date",
    )

    assert isinstance(err, PropertyError)


def test_dont_recheck_value():
    DateProperty.convert_value(Value("not a date but trust me"))
