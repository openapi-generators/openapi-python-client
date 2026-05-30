from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties import FileProperty


def test_no_default_allowed():
    # currently this is testing an unused code path:
    # https://github.com/openapi-generators/openapi-python-client/issues/1162
    err = FileProperty.build(
        default="not none",
        description=None,
        example=None,
        required=False,
        python_name="not_none",
        name="not_none",
    )

    assert isinstance(err, PropertyError)
