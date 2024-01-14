from pathlib import Path
from typing import Any, Callable, Dict

import pytest

from openapi_python_client import Config, MetaType
from openapi_python_client import schema as oai
from openapi_python_client.config import ConfigFile
from openapi_python_client.parser.properties import (
    AnyProperty,
    BooleanProperty,
    DateProperty,
    DateTimeProperty,
    EnumProperty,
    FileProperty,
    IntProperty,
    ListProperty,
    ModelProperty,
    NoneProperty,
    StringProperty,
    UnionProperty,
)
from openapi_python_client.schema.openapi_schema_pydantic import Parameter
from openapi_python_client.schema.parameter_location import ParameterLocation


@pytest.fixture(scope="session")
def config() -> Config:
    """Create a default config for when it doesn't matter"""
    return Config.from_sources(
        ConfigFile(), MetaType.POETRY, document_source=Path("openapi.yaml"), file_encoding="utf-8"
    )


@pytest.fixture
def model_property_factory() -> Callable[..., ModelProperty]:
    """
    This fixture surfaces in the test as a function which manufactures ModelProperties with defaults.

    You can pass the same params into this as the ModelProperty constructor to override defaults.
    """
    from openapi_python_client.parser.properties import Class

    def _factory(**kwargs):
        kwargs = _common_kwargs(kwargs)
        kwargs = {
            "description": "",
            "class_info": Class(name="MyClass", module_name="my_module"),
            "data": oai.Schema.model_construct(),
            "roots": set(),
            "required_properties": None,
            "optional_properties": None,
            "relative_imports": None,
            "lazy_imports": None,
            "additional_properties": None,
            "python_name": "",
            "example": "",
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
        kwargs = _common_kwargs(kwargs)
        kwargs = {
            "class_info": Class(name=kwargs["name"], module_name=kwargs["name"]),
            "values": {},
            "value_type": str,
            **kwargs,
        }
        return EnumProperty(**kwargs)

    return _factory


@pytest.fixture
def any_property_factory() -> Callable[..., AnyProperty]:
    """
    This fixture surfaces in the test as a function which manufactures AnyProperty with defaults.

    You can pass the same params into this as the AnyProperty constructor to override defaults.
    """

    def _factory(**kwargs):
        kwargs = _common_kwargs(kwargs)
        return AnyProperty(**kwargs)

    return _factory


@pytest.fixture
def string_property_factory() -> Callable[..., StringProperty]:
    """
    This fixture surfaces in the test as a function which manufactures StringProperties with defaults.

    You can pass the same params into this as the StringProperty constructor to override defaults.
    """

    def _factory(**kwargs):
        kwargs = _common_kwargs(kwargs)
        return StringProperty(**kwargs)

    return _factory


@pytest.fixture
def int_property_factory() -> Callable[..., IntProperty]:
    """
    This fixture surfaces in the test as a function which manufactures StringProperties with defaults.

    You can pass the same params into this as the StringProperty constructor to override defaults.
    """

    def _factory(**kwargs):
        kwargs = _common_kwargs(kwargs)
        return IntProperty(**kwargs)

    return _factory


@pytest.fixture
def none_property_factory() -> Callable[..., NoneProperty]:
    """
    This fixture surfaces in the test as a function which manufactures StringProperties with defaults.

    You can pass the same params into this as the StringProperty constructor to override defaults.
    """

    def _factory(**kwargs):
        kwargs = _common_kwargs(kwargs)
        return NoneProperty(**kwargs)

    return _factory


@pytest.fixture
def boolean_property_factory() -> Callable[..., BooleanProperty]:
    """
    This fixture surfaces in the test as a function which manufactures StringProperties with defaults.

    You can pass the same params into this as the StringProperty constructor to override defaults.
    """

    def _factory(**kwargs):
        kwargs = _common_kwargs(kwargs)
        return BooleanProperty(**kwargs)

    return _factory


@pytest.fixture
def date_time_property_factory() -> Callable[..., DateTimeProperty]:
    """
    This fixture surfaces in the test as a function which manufactures DateTimeProperties with defaults.

    You can pass the same params into this as the DateTimeProperty constructor to override defaults.
    """

    def _factory(**kwargs):
        kwargs = _common_kwargs(kwargs)
        return DateTimeProperty(**kwargs)

    return _factory


@pytest.fixture
def date_property_factory() -> Callable[..., DateProperty]:
    """
    This fixture surfaces in the test as a function which manufactures DateProperties with defaults.

    You can pass the same params into this as the DateProperty constructor to override defaults.
    """

    def _factory(**kwargs):
        kwargs = _common_kwargs(kwargs)
        return DateProperty(**kwargs)

    return _factory


@pytest.fixture
def file_property_factory() -> Callable[..., FileProperty]:
    """
    This fixture surfaces in the test as a function which manufactures FileProperties with defaults.

    You can pass the same params into this as the FileProperty constructor to override defaults.
    """

    def _factory(**kwargs):
        kwargs = _common_kwargs(kwargs)
        return FileProperty(**kwargs)

    return _factory


@pytest.fixture
def list_property_factory(string_property_factory) -> Callable[..., ListProperty]:
    """
    This fixture surfaces in the test as a function which manufactures ListProperties with defaults.

    You can pass the same params into this as the ListProperty constructor to override defaults.
    """

    def _factory(**kwargs):
        kwargs = _common_kwargs(kwargs)
        if "inner_property" not in kwargs:
            kwargs["inner_property"] = string_property_factory()
        return ListProperty(**kwargs)

    return _factory


@pytest.fixture
def union_property_factory(date_time_property_factory, string_property_factory) -> Callable[..., UnionProperty]:
    """
    This fixture surfaces in the test as a function which manufactures UnionProperties with defaults.

    You can pass the same params into this as the UnionProperty constructor to override defaults.
    """

    def _factory(**kwargs):
        kwargs = _common_kwargs(kwargs)
        if "inner_properties" not in kwargs:
            kwargs["inner_properties"] = [date_time_property_factory(), string_property_factory()]
        return UnionProperty(**kwargs)

    return _factory


@pytest.fixture
def param_factory() -> Callable[..., Parameter]:
    """
    This fixture surfaces in the test as a function which manufactures a Parameter with defaults.

    You can pass the same params into this as the Parameter constructor to override defaults.
    """

    def _factory(**kwargs):
        kwargs = {
            "name": "",
            "in": ParameterLocation.QUERY,
            **kwargs,
        }
        return Parameter(**kwargs)

    return _factory


def _common_kwargs(kwargs: Dict[str, Any]) -> Dict[str, Any]:
    kwargs = {
        "name": "test",
        "required": True,
        "default": None,
        "description": None,
        "example": None,
        **kwargs,
    }
    if not kwargs.get("python_name"):
        kwargs["python_name"] = kwargs["name"]
    return kwargs
