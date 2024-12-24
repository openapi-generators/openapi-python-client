import attr

import openapi_python_client.schema as oai
from openapi_python_client.parser.errors import ParseError, PropertyError
from openapi_python_client.parser.properties import ListProperty
from openapi_python_client.parser.properties.schemas import ReferencePath
from openapi_python_client.schema import DataType
from openapi_python_client.utils import ClassName


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
        roots={ReferencePath("root")},
    )

    assert p == PropertyError(data=data, detail="type array must have items or prefixItems defined")
    assert new_schemas == schemas


def test_build_list_property_invalid_items(config):
    from openapi_python_client.parser import properties

    name = "name"
    required = True
    data = oai.Schema(
        type=DataType.ARRAY,
        items=oai.Reference.model_validate({"$ref": "doesnt exist"}),
    )
    schemas = properties.Schemas(errors=[ParseError("error")])
    process_properties = False
    roots: set[ReferencePath | ClassName] = {ReferencePath("root")}

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
    schemas = properties.Schemas(errors=[ParseError("error")])

    p, new_schemas = ListProperty.build(
        name=name,
        required=True,
        data=data,
        schemas=schemas,
        parent_name="parent",
        config=config,
        roots={ReferencePath("root")},
        process_properties=True,
    )

    assert isinstance(p, properties.ListProperty)
    assert p.inner_property == any_property_factory(name=f"{name}_item")
    assert new_schemas == schemas


def test_build_list_property_single_prefix_item(any_property_factory, config):
    from openapi_python_client.parser import properties

    name = "prop"
    data = oai.Schema(
        type=DataType.ARRAY,
        prefixItems=[oai.Schema()],
    )
    schemas = properties.Schemas(errors=[ParseError("error")])

    p, new_schemas = ListProperty.build(
        name=name,
        required=True,
        data=data,
        schemas=schemas,
        parent_name="parent",
        config=config,
        roots={ReferencePath("root")},
        process_properties=True,
    )

    assert isinstance(p, properties.ListProperty)
    assert p.inner_property == any_property_factory(name=f"{name}_item")
    assert new_schemas == schemas


def test_build_list_property_items_and_prefix_items(
    union_property_factory,
    string_property_factory,
    none_property_factory,
    int_property_factory,
    config,
):
    from openapi_python_client.parser import properties

    name = "list_prop"
    required = True
    data = oai.Schema(
        type=DataType.ARRAY,
        items=oai.Schema(type=DataType.INTEGER),
        prefixItems=[oai.Schema(type=DataType.STRING), oai.Schema(type=DataType.NULL)],
    )
    schemas = properties.Schemas()

    p, new_schemas = ListProperty.build(
        name=name,
        required=required,
        data=data,
        schemas=schemas,
        parent_name="parent",
        config=config,
        process_properties=True,
        roots={ReferencePath("root")},
    )

    assert isinstance(p, properties.ListProperty)
    assert p.inner_property == union_property_factory(
        name=f"{name}_item",
        inner_properties=[
            string_property_factory(name=f"{name}_item_type_0"),
            none_property_factory(name=f"{name}_item_type_1"),
            int_property_factory(name=f"{name}_item_type_2"),
        ],
    )
    assert new_schemas == schemas


def test_build_list_property_prefix_items_only(any_property_factory, config):
    from openapi_python_client.parser import properties

    name = "list_prop"
    required = True
    data = oai.Schema(type=DataType.ARRAY, prefixItems=[oai.Schema()])
    schemas = properties.Schemas()

    p, new_schemas = ListProperty.build(
        name=name,
        required=required,
        data=data,
        schemas=schemas,
        parent_name="parent",
        config=config,
        process_properties=True,
        roots={ReferencePath("root")},
    )

    assert isinstance(p, properties.ListProperty)
    assert p.inner_property == any_property_factory(name=f"{name}_item")
    assert new_schemas == schemas
