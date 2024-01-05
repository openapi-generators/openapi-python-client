import openapi_python_client.schema as oai
from openapi_python_client import Config
from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties import EnumProperty, Schemas


def test_conflict():
    schemas = Schemas()

    _, schemas = EnumProperty.build(
        data=oai.Schema(enum=["a"]), name="Existing", required=True, schemas=schemas, parent_name="", config=Config()
    )
    err, new_schemas = EnumProperty.build(
        data=oai.Schema(enum=["a", "b"]),
        name="Existing",
        required=True,
        schemas=schemas,
        parent_name="",
        config=Config(),
    )

    assert schemas == new_schemas
    assert err.detail == "Found conflicting enums named Existing with incompatible values."


def test_bad_default_value():
    data = oai.Schema(default="B", enum=["A"])
    schemas = Schemas()

    err, new_schemas = EnumProperty.build(
        data=data, name="Existing", required=True, schemas=schemas, parent_name="parent", config=Config()
    )

    assert schemas == new_schemas
    assert err == PropertyError(detail="Value B is not valid for enum Existing", data=data)


def test_bad_default_type():
    data = oai.Schema(default=123, enum=["A"])
    schemas = Schemas()

    err, new_schemas = EnumProperty.build(
        data=data, name="Existing", required=True, schemas=schemas, parent_name="parent", config=Config()
    )

    assert schemas == new_schemas
    assert isinstance(err, PropertyError)


def test_mixed_types():
    data = oai.Schema(enum=["A", 1])
    schemas = Schemas()

    err, _ = EnumProperty.build(
        data=data, name="Enum", required=True, schemas=schemas, parent_name="parent", config=Config()
    )

    assert isinstance(err, PropertyError)


def test_unsupported_type():
    data = oai.Schema(enum=[1.4, 1.5])
    schemas = Schemas()

    err, _ = EnumProperty.build(
        data=data, name="Enum", required=True, schemas=schemas, parent_name="parent", config=Config()
    )

    assert isinstance(err, PropertyError)
