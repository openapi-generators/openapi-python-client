import attr

import openapi_python_client.schema as oai
from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties import ListProperty
from openapi_python_client.schema import DataType


def test_build_list_property_no_items(config):
    from openapi_python_client.parser import properties

    name = "list_prop"
    required = True
    data = oai.Schema(type=DataType.ARRAY)
    schemas = properties.Schemas()

    p, new_schemas = ListProperty.build(
        name=name,
        required=required,
        data=data,
        schemas=schemas,
        parent_name="parent",
        config=config,
        process_properties=True,
        roots={"root"},
    )

    assert p == PropertyError(data=data, detail="type array must have items defined")
    assert new_schemas == schemas


def test_build_list_property_invalid_items(config):
    from openapi_python_client.parser import properties

    name = "name"
    required = True
    data = oai.Schema(
        type=DataType.ARRAY,
        items=oai.Reference(ref="doesnt exist"),
    )
    schemas = properties.Schemas(errors=["error"])
    process_properties = False
    roots = {"root"}

    p, new_schemas = ListProperty.build(
        name=name,
        required=required,
        data=data,
        schemas=attr.evolve(schemas),
        parent_name="parent",
        config=config,
        roots=roots,
        process_properties=process_properties,
    )

    assert isinstance(p, PropertyError)
    assert p.data == data.items
    assert p.header.startswith(f"invalid data in items of array {name}")
    assert new_schemas == schemas


def test_build_list_property(any_property_factory, config):
    from openapi_python_client.parser import properties

    name = "prop"
    data = oai.Schema(
        type=DataType.ARRAY,
        items=oai.Schema(),
    )
    schemas = properties.Schemas(errors=["error"])

    p, new_schemas = ListProperty.build(
        name=name,
        required=True,
        data=data,
        schemas=schemas,
        parent_name="parent",
        config=config,
        roots={"root"},
        process_properties=True,
    )

    assert isinstance(p, properties.ListProperty)
    assert p.inner_property == any_property_factory(name=f"{name}_item")
    assert new_schemas == schemas
