import pytest

from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties import BooleanProperty
from openapi_python_client.utils import PythonIdentifier


def test_invalid_default_value() -> None:
    err = BooleanProperty.build(
        default="not a boolean",
        description=None,
        example=None,
        required=False,
        python_name=PythonIdentifier("not_a_boolean", ""),
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
def test_string_default(value, expected) -> None:
    prop = BooleanProperty.build(
        default=value,
        description=None,
        example=None,
        required=False,
        python_name="not_a_boolean",
        name="not_a_boolean",
    )

    assert isinstance(prop, BooleanProperty)
    assert prop.default.python_code == expected


def test_bool_default() -> None:
    prop = BooleanProperty.build(
        default=True,
        description=None,
        example=None,
        required=False,
        python_name="not_a_boolean",
        name="not_a_boolean",
    )

    assert isinstance(prop, BooleanProperty)
    assert prop.default.python_code == "True"
