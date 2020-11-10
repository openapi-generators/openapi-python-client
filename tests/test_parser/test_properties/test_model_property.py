import pytest


@pytest.mark.parametrize(
    "no_optional,nullable,required,expected",
    [
        (False, False, False, "Union[MyClass, Unset]"),
        (False, False, True, "MyClass"),
        (False, True, False, "Union[Optional[MyClass], Unset]"),
        (False, True, True, "Optional[MyClass]"),
        (True, False, False, "MyClass"),
        (True, False, True, "MyClass"),
        (True, True, False, "MyClass"),
        (True, True, True, "MyClass"),
    ],
)
def test_get_type_string(no_optional, nullable, required, expected):
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
    )

    assert prop.get_type_string(no_optional=no_optional) == expected


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
    )

    assert prop.get_imports(prefix="..") == {
        "from typing import Optional",
        "from typing import Union",
        "from ..types import UNSET, Unset",
        "from ..models.my_module import MyClass",
        "from typing import Dict",
        "from typing import cast",
    }
