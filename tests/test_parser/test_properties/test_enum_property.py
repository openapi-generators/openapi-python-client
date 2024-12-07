from typing import Union

import pytest

import openapi_python_client.schema as oai
from openapi_python_client import Config
from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties import (
    EnumProperty,
    LiteralEnumProperty,
    NoneProperty,
    Schemas,
    UnionProperty,
)

PropertyClass = Union[type[EnumProperty], type[LiteralEnumProperty]]


@pytest.fixture(params=[EnumProperty, LiteralEnumProperty])
def property_class(request) -> PropertyClass:
    return request.param


def test_conflict(config: Config, property_class: PropertyClass) -> None:
    schemas = Schemas()

    _, schemas = property_class.build(
        data=oai.Schema(enum=["a"]), name="Existing", required=True, schemas=schemas, parent_name="", config=config
    )
    err, new_schemas = property_class.build(
        data=oai.Schema(enum=["a", "b"]),
        name="Existing",
        required=True,
        schemas=schemas,
        parent_name="",
        config=config,
    )

    assert schemas == new_schemas
    assert err.detail == "Found conflicting enums named Existing with incompatible values."


def test_bad_default_value(config: Config, property_class: PropertyClass) -> None:
    data = oai.Schema(default="B", enum=["A"])
    schemas = Schemas()

    err, new_schemas = property_class.build(
        data=data, name="Existing", required=True, schemas=schemas, parent_name="parent", config=config
    )

    assert schemas == new_schemas
    assert err == PropertyError(detail="Value B is not valid for enum Existing", data=data)


def test_bad_default_type(config: Config, property_class: PropertyClass) -> None:
    data = oai.Schema(default=123, enum=["A"])
    schemas = Schemas()

    err, new_schemas = property_class.build(
        data=data, name="Existing", required=True, schemas=schemas, parent_name="parent", config=config
    )

    assert schemas == new_schemas
    assert isinstance(err, PropertyError)


def test_mixed_types(config: Config, property_class: PropertyClass) -> None:
    data = oai.Schema(enum=["A", 1])
    schemas = Schemas()

    err, _ = property_class.build(
        data=data, name="Enum", required=True, schemas=schemas, parent_name="parent", config=config
    )

    assert isinstance(err, PropertyError)


def test_unsupported_type(config: Config, property_class: PropertyClass) -> None:
    data = oai.Schema(enum=[1.4, 1.5])
    schemas = Schemas()

    err, _ = property_class.build(
        data=data, name="Enum", required=True, schemas=schemas, parent_name="parent", config=config
    )

    assert isinstance(err, PropertyError)


def test_nullable_enum(config):
    data = oai.Schema(
        type="string",
        enum=["a", "b", None],
        nullable=True,
    )
    schemas = Schemas()

    p, _ = EnumProperty.build(
        data=data, name="prop1", required=True, schemas=schemas, parent_name="parent", config=config
    )

    assert isinstance(p, UnionProperty)
    assert len(p.inner_properties) == 2
    assert isinstance(p.inner_properties[0], NoneProperty)
    assert isinstance(p.inner_properties[1], EnumProperty)
    assert p.inner_properties[1].class_info.name == "ParentProp1"
