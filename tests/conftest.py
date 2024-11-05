from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

import pytest
from mypy.semanal_shared import Protocol

from openapi_python_client import Config, MetaType
from openapi_python_client import schema as oai
from openapi_python_client.config import ConfigFile
from openapi_python_client.parser.properties import (
    AnyProperty,
    BooleanProperty,
    Class,
    DateProperty,
    DateTimeProperty,
    EnumProperty,
    FileProperty,
    IntProperty,
    ListProperty,
    LiteralEnumProperty,
    ModelProperty,
    NoneProperty,
    StringProperty,
    UnionProperty,
)
from openapi_python_client.parser.properties.float import FloatProperty
from openapi_python_client.parser.properties.model_property import ModelDetails
from openapi_python_client.parser.properties.protocol import PropertyType, Value
from openapi_python_client.schema.openapi_schema_pydantic import Parameter
from openapi_python_client.schema.parameter_location import ParameterLocation
from openapi_python_client.utils import ClassName, PythonIdentifier


@pytest.fixture(scope="session")
def config() -> Config:
    """Create a default config for when it doesn't matter"""
    return Config.from_sources(
        ConfigFile(),
        MetaType.POETRY,
        document_source=Path("openapi.yaml"),
        file_encoding="utf-8",
        overwrite=False,
        output_path=None,
    )


class ModelFactory(Protocol):
    def __call__(self, *args, **kwargs): ...


@pytest.fixture
def model_property_factory() -> ModelFactory:
    """
    This fixture surfaces in the test as a function which manufactures ModelProperties with defaults.

    You can pass the same params into this as the ModelProperty constructor to override defaults.
    """
    from openapi_python_client.parser.properties import Class

    def _factory(**kwargs):
        kwargs = _common_kwargs(kwargs)
        kwargs = {
            "description": "",
            "class_info": Class(name=ClassName("MyClass", ""), module_name=PythonIdentifier("my_module", "")),
            "data": oai.Schema.model_construct(),
            "roots": set(),
            "python_name": "",
            "example": "",
            **kwargs,
        }
        # shortcuts for setting attributes within ModelDetails
        if "details" not in kwargs:
            detail_args = {}
            for arg_name in [
                "required_properties",
                "optional_properties",
                "additional_properties",
                "relative_imports",
                "lazy_imports",
            ]:
                if arg_name in kwargs:
                    detail_args[arg_name] = kwargs[arg_name]
                    kwargs.pop(arg_name)
            kwargs["details"] = ModelDetails(**detail_args)

        return ModelProperty(**kwargs)

    return _factory


def _simple_factory(
    cls: type[PropertyType], default_kwargs: dict | Callable[[dict], dict] | None = None
) -> Callable[..., PropertyType]:
    def _factory(**kwargs):
        kwargs = _common_kwargs(kwargs)
        defaults = default_kwargs
        if defaults:
            if callable(defaults):
                defaults = defaults(kwargs)
            kwargs = {**defaults, **kwargs}
        rv = cls(**kwargs)
        return rv

    return _factory


class SimpleFactory(Protocol[PropertyType]):
    def __call__(
        self,
        *,
        default: Value | None = None,
        name: str | None = None,
        required: bool | None = None,
        description: str | None = None,
        example: str | None = None,
    ) -> PropertyType: ...


class EnumFactory(Protocol[PropertyType]):
    def __call__(
        self,
        *,
        default: Value | None = None,
        name: str | None = None,
        required: bool | None = None,
        values: dict[str, str | int] | None = None,
        class_info: Class | None = None,
        value_type: type | None = None,
        python_name: PythonIdentifier | None = None,
        description: str | None = None,
        example: str | None = None,
    ) -> PropertyType: ...


@pytest.fixture
def enum_property_factory() -> EnumFactory[EnumProperty]:
    """
    This fixture surfaces in the test as a function which manufactures EnumProperties with defaults.

    You can pass the same params into this as the EnumProerty constructor to override defaults.
    """
    from openapi_python_client.parser.properties import Class

    return _simple_factory(
        EnumProperty,
        lambda kwargs: {
            "class_info": Class(name=kwargs["name"], module_name=kwargs["name"]),
            "values": {},
            "value_type": str,
        },
    )


@pytest.fixture
def literal_enum_property_factory() -> EnumFactory[LiteralEnumProperty]:
    """
    This fixture surfaces in the test as a function which manufactures LiteralEnumProperties with defaults.

    You can pass the same params into this as the LiteralEnumProerty constructor to override defaults.
    """
    from openapi_python_client.parser.properties import Class

    return _simple_factory(
        LiteralEnumProperty,
        lambda kwargs: {
            "class_info": Class(name=kwargs["name"], module_name=kwargs["name"]),
            "values": set(),
            "value_type": str,
        },
    )


@pytest.fixture
def any_property_factory() -> SimpleFactory[AnyProperty]:
    """
    This fixture surfaces in the test as a function which manufactures AnyProperty with defaults.

    You can pass the same params into this as the AnyProperty constructor to override defaults.
    """

    return _simple_factory(AnyProperty)


@pytest.fixture
def string_property_factory() -> SimpleFactory[StringProperty]:
    """
    This fixture surfaces in the test as a function which manufactures StringProperties with defaults.

    You can pass the same params into this as the StringProperty constructor to override defaults.
    """

    return _simple_factory(StringProperty)


@pytest.fixture
def int_property_factory() -> SimpleFactory[IntProperty]:
    """
    This fixture surfaces in the test as a function which manufactures IntProperties with defaults.

    You can pass the same params into this as the IntProperty constructor to override defaults.
    """

    return _simple_factory(IntProperty)


@pytest.fixture
def float_property_factory() -> SimpleFactory[FloatProperty]:
    """
    This fixture surfaces in the test as a function which manufactures FloatProperties with defaults.

    You can pass the same params into this as the FloatProperty constructor to override defaults.
    """

    return _simple_factory(FloatProperty)


@pytest.fixture
def none_property_factory() -> SimpleFactory[NoneProperty]:
    """
    This fixture surfaces in the test as a function which manufactures NoneProperties with defaults.

    You can pass the same params into this as the NoneProperty constructor to override defaults.
    """

    return _simple_factory(NoneProperty)


@pytest.fixture
def boolean_property_factory() -> SimpleFactory[BooleanProperty]:
    """
    This fixture surfaces in the test as a function which manufactures BooleanProperties with defaults.

    You can pass the same params into this as the BooleanProperty constructor to override defaults.
    """

    return _simple_factory(BooleanProperty)


@pytest.fixture
def date_time_property_factory() -> SimpleFactory[DateTimeProperty]:
    """
    This fixture surfaces in the test as a function which manufactures DateTimeProperties with defaults.

    You can pass the same params into this as the DateTimeProperty constructor to override defaults.
    """

    return _simple_factory(DateTimeProperty)


@pytest.fixture
def date_property_factory() -> SimpleFactory[DateProperty]:
    """
    This fixture surfaces in the test as a function which manufactures DateProperties with defaults.

    You can pass the same params into this as the DateProperty constructor to override defaults.
    """

    return _simple_factory(DateProperty)


@pytest.fixture
def file_property_factory() -> SimpleFactory[FileProperty]:
    """
    This fixture surfaces in the test as a function which manufactures FileProperties with defaults.

    You can pass the same params into this as the FileProperty constructor to override defaults.
    """

    return _simple_factory(FileProperty)


@pytest.fixture
def list_property_factory(string_property_factory) -> SimpleFactory[ListProperty]:
    """
    This fixture surfaces in the test as a function which manufactures ListProperties with defaults.

    You can pass the same params into this as the ListProperty constructor to override defaults.
    """

    return _simple_factory(ListProperty, {"inner_property": string_property_factory()})


class UnionFactory(SimpleFactory):
    def __call__(
        self,
        *,
        default: Value | None = None,
        name: str | None = None,
        required: bool | None = None,
        inner_properties: list[PropertyType] | None = None,
    ) -> UnionProperty: ...


@pytest.fixture
def union_property_factory(date_time_property_factory, string_property_factory) -> UnionFactory:
    """
    This fixture surfaces in the test as a function which manufactures UnionProperties with defaults.

    You can pass the same params into this as the UnionProperty constructor to override defaults.
    """

    return _simple_factory(
        UnionProperty, {"inner_properties": [date_time_property_factory(), string_property_factory()]}
    )


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


def _common_kwargs(kwargs: dict[str, Any]) -> dict[str, Any]:
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
