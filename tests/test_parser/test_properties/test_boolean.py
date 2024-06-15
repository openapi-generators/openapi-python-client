import pytest

from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties import BooleanProperty


def test_invalid_default_value():
    err = BooleanProperty.build(
        default="not a boolean",
        description=None,
        example=None,
        required=False,
        python_name="not_a_boolean",
        name="not_a_boolean",
    )

    assert isinstance(err, PropertyError)


@pytest.mark.parametrize(
    ("value", "expected"),
    (
        ("true", "True"),
        ("True", "True"),
        ("false", "False"),
        ("False", "False"),
    ),
)
def test_string_default(value, expected):
    prop = BooleanProperty.build(
        default=value,
        description=None,
        example=None,
        required=False,
        python_name="not_a_boolean",
        name="not_a_boolean",
    )

    assert isinstance(prop, BooleanProperty)
    assert prop.default == expected


def test_bool_default():
    prop = BooleanProperty.build(
        default=True,
        description=None,
        example=None,
        required=False,
        python_name="not_a_boolean",
        name="not_a_boolean",
    )

    assert isinstance(prop, BooleanProperty)
    assert prop.default == "True"
