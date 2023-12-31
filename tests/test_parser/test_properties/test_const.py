from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties import ConstProperty
from openapi_python_client.parser.properties.protocol import Value


def test_default_doesnt_match_const():
    err = ConstProperty.build(
        name="test",
        required=True,
        default="not the value",
        python_name="test",
        description=None,
        const="the value",
    )

    assert isinstance(err, PropertyError)


def test_non_string_const():
    prop = ConstProperty.build(
        name="test",
        required=True,
        default=123,
        python_name="test",
        description=None,
        const=123,
    )

    assert isinstance(prop, ConstProperty)


def test_const_already_converted():
    prop = ConstProperty.build(
        name="test",
        required=True,
        default=123,
        python_name="test",
        description=None,
        const=Value("123"),
    )

    assert isinstance(prop, ConstProperty)


def test_default_already_converted():
    prop = ConstProperty.build(
        name="test",
        required=True,
        default=Value("123"),
        python_name="test",
        description=None,
        const=123,
    )

    assert isinstance(prop, ConstProperty)
