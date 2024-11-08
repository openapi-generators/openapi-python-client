from typing import Type, Union

import pytest

import openapi_python_client.schema as oai
from openapi_python_client import Config
from openapi_python_client.parser.properties import LiteralEnumProperty, Schemas
from openapi_python_client.parser.properties.enum_property import EnumProperty

PropertyClass = Union[Type[EnumProperty], Type[LiteralEnumProperty]]


@pytest.fixture(params=[EnumProperty, LiteralEnumProperty])
def property_class(request) -> PropertyClass:
    return request.param


def test_conflict(config: Config, property_class: PropertyClass) -> None:
    # It'd be nice to move this test into generated_code_live_tests, but it's unclear
    # how to represent this error condition in an actual API spec.
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
