import openapi_python_client.schema as oai
from openapi_python_client import Config
from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties import EnumProperty, Schemas


def test_conflict():
    data = oai.Schema()
    schemas = Schemas()

    _, schemas = EnumProperty.build(
        data=data, name="Existing", required=True, schemas=schemas, enum=["a"], parent_name="", config=Config()
    )
    err, new_schemas = EnumProperty.build(
        data=data,
        name="Existing",
        required=True,
        schemas=schemas,
        enum=["a", "b"],
        parent_name="",
        config=Config(),
    )

    assert schemas == new_schemas
    assert err == PropertyError(detail="Found conflicting enums named Existing with incompatible values.", data=data)


def test_no_values():
    data = oai.Schema()
    schemas = Schemas()

    err, new_schemas = EnumProperty.build(
        data=data, name="Existing", required=True, schemas=schemas, enum=[], parent_name=None, config=Config()
    )

    assert schemas == new_schemas
    assert err == PropertyError(detail="No values provided for Enum", data=data)


def test_bad_default_value():
    data = oai.Schema(default="B")
    schemas = Schemas()

    err, new_schemas = EnumProperty.build(
        data=data, name="Existing", required=True, schemas=schemas, enum=["A"], parent_name=None, config=Config()
    )

    assert schemas == new_schemas
    assert err == PropertyError(detail="Value B is not valid for enum Existing", data=data)


def test_bad_default_type():
    data = oai.Schema(default=123)
    schemas = Schemas()

    err, new_schemas = EnumProperty.build(
        data=data, name="Existing", required=True, schemas=schemas, enum=["A"], parent_name=None, config=Config()
    )

    assert schemas == new_schemas
    assert isinstance(err, PropertyError)
