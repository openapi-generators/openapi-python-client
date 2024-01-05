from openapi_python_client.parser.properties import AnyProperty


def test_default():
    AnyProperty.build(
        name="test",
        required=True,
        default=42,
        python_name="test",
        description="test",
        example="test",
    )
