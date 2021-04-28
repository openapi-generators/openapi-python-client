import pytest


def test_class_from_string_default_config():
    from openapi_python_client import Config
    from openapi_python_client.parser.properties import Class

    class_ = Class.from_string(string="#/components/schemas/PingResponse", config=Config())

    assert class_.name == "PingResponse"
    assert class_.module_name == "ping_response"


@pytest.mark.parametrize(
    "class_override, module_override, expected_class, expected_module",
    (
        (None, None, "MyResponse", "my_response"),
        ("MyClass", None, "MyClass", "my_class"),
        ("MyClass", "some_module", "MyClass", "some_module"),
        (None, "some_module", "MyResponse", "some_module"),
    ),
)
def test_class_from_string(class_override, module_override, expected_class, expected_module):
    from openapi_python_client.config import ClassOverride, Config
    from openapi_python_client.parser.properties import Class

    ref = "#/components/schemas/MyResponse"
    config = Config(
        class_overrides={"MyResponse": ClassOverride(class_name=class_override, module_name=module_override)}
    )

    result = Class.from_string(string=ref, config=config)
    assert result.name == expected_class
    assert result.module_name == expected_module
