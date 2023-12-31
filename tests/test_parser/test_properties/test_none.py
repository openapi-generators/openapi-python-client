from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties import NoneProperty
from openapi_python_client.parser.properties.protocol import Value


def test_default():
    err = NoneProperty.build(
        default="not None",
        description=None,
        example=None,
        required=False,
        python_name="not_none",
        name="not_none",
    )

    assert isinstance(err, PropertyError)


def test_dont_retest_values():
    prop = NoneProperty.build(
        default=Value("not None"),
        description=None,
        example=None,
        required=False,
        python_name="not_none",
        name="not_none",
    )

    assert isinstance(prop, NoneProperty)
