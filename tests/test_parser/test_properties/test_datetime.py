from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties import DateTimeProperty


def test_invalid_default_value():
    err = DateTimeProperty.build(
        default="not a date",
        description=None,
        example=None,
        required=False,
        python_name="not_a_date",
        name="not_a_date",
    )

    assert isinstance(err, PropertyError)


def test_default_with_bad_type():
    err = DateTimeProperty.build(
        default=123,
        description=None,
        example=None,
        required=False,
        python_name="not_a_date",
        name="not_a_date",
    )

    assert isinstance(err, PropertyError)
