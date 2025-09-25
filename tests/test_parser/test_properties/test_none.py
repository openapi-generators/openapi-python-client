from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties import NoneProperty
from openapi_python_client.parser.properties.protocol import Value
from openapi_python_client.utils import PythonIdentifier


def test_default():
    # currently this is testing an unused code path:
    # https://github.com/openapi-generators/openapi-python-client/issues/1162
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
        default=Value("not None", "not None"),
        description=None,
        example=None,
        required=False,
        python_name=PythonIdentifier("not_none", ""),
        name="not_none",
    )

    assert isinstance(prop, NoneProperty)
