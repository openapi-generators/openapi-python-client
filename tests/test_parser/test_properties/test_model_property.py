import pytest


@pytest.mark.parametrize(
    "no_optional,nullable,required,json,expected",
    [
        (False, False, False, False, "Union[Unset, MyClass]"),
        (False, False, True, False, "MyClass"),
        (False, True, False, False, "Union[Unset, None, MyClass]"),
        (False, True, True, False, "Optional[MyClass]"),
        (True, False, False, False, "MyClass"),
        (True, False, True, False, "MyClass"),
        (True, True, False, False, "MyClass"),
        (True, True, True, False, "MyClass"),
        (False, False, True, True, "Dict[str, Any]"),
    ],
)
def test_get_type_string(no_optional, nullable, required, json, expected):
    from openapi_python_client.parser.properties import ModelProperty, Reference

    prop = ModelProperty(
        name="prop",
        required=required,
        nullable=nullable,
        default=None,
        reference=Reference(class_name="MyClass", module_name="my_module"),
        description="",
        optional_properties=[],
        required_properties=[],
        relative_imports=set(),
        additional_properties=False,
    )

    assert prop.get_type_string(no_optional=no_optional, json=json) == expected


def test_get_imports():
    from openapi_python_client.parser.properties import ModelProperty, Reference

    prop = ModelProperty(
        name="prop",
        required=False,
        nullable=True,
        default=None,
        reference=Reference(class_name="MyClass", module_name="my_module"),
        description="",
        optional_properties=[],
        required_properties=[],
        relative_imports=set(),
        additional_properties=False,
    )

    assert prop.get_imports(prefix="..") == {
        "from typing import Optional",
        "from typing import Union",
        "from ..types import UNSET, Unset",
        "from ..models.my_module import MyClass",
        "from typing import Dict",
        "from typing import cast",
    }
