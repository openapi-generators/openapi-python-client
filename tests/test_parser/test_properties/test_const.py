import pytest

from openapi_python_client.parser.properties import ConstProperty
from openapi_python_client.strings import PythonCode, PythonIdentifier


@pytest.mark.parametrize(
    ("const", "expected"),
    [("auto", "str"), (1, "int"), (1.5, "float"), (True, "bool")],
)
def test_get_instance_type_string(const, expected):
    prop = ConstProperty.build(
        const=const,
        default=None,
        name="prop",
        python_name=PythonIdentifier("prop", ""),
        required=True,
        description=None,
    )

    assert isinstance(prop, ConstProperty)
    assert prop.get_instance_type_string() == PythonCode(expected)
