from typing import Callable

import pytest

from openapi_python_client.parser.properties import EnumProperty, ModelProperty


@pytest.fixture
def model_property_factory() -> Callable[..., ModelProperty]:
    """
    This fixture surfaces in the test as a function which manufactures ModelProperties with defaults.

    You can pass the same params into this as the ModelProperty constructor to override defaults.
    """
    from openapi_python_client.parser.properties import Class

    def _factory(**kwargs):
        kwargs = {
            "name": "",
            "description": "",
            "required": True,
            "nullable": True,
            "default": None,
            "class_info": Class(name="", module_name=""),
            "required_properties": [],
            "optional_properties": [],
            "relative_imports": set(),
            "additional_properties": False,
            **kwargs,
        }
        return ModelProperty(**kwargs)

    return _factory


@pytest.fixture
def enum_property_factory() -> Callable[..., EnumProperty]:
    """
    This fixture surfaces in the test as a function which manufactures EnumProperties with defaults.

    You can pass the same params into this as the EnumProerty constructor to override defaults.
    """
    from openapi_python_client.parser.properties import Class

    def _factory(**kwargs):
        kwargs = {
            "name": "test",
            "required": True,
            "nullable": False,
            "default": None,
            "class_info": Class(name="", module_name=""),
            "values": {},
            "value_type": str,
            **kwargs,
        }
        return EnumProperty(**kwargs)

    return _factory
