from openapi_python_client.parser.properties import AnyProperty
from openapi_python_client.utils import PythonIdentifier


def test_default() -> None:
    AnyProperty.build(
        name="test",
        required=True,
        default=42,
        python_name=PythonIdentifier("test", ""),
        description="test",
        example="test",
    )
