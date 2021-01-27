import pytest


@pytest.mark.parametrize(
    "no_optional,nullable,required,expected",
    [
        (False, False, False, "Union[Unset, MyClass]"),
        (False, False, True, "MyClass"),
        (False, True, False, "Union[Unset, None, MyClass]"),
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
        references=[],
        description="",
        optional_properties=[],
        required_properties=[],
        relative_imports=set(),
        additional_properties=False,
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
        references=[],
        description="",
        optional_properties=[],
        required_properties=[],
        relative_imports=set(),
        additional_properties=False,
    )

    assert prop.get_imports(prefix="..") == {
        "from typing import Optional",
        "from typing import Union",
        "from ..types import UNSET, Unset",
        "from ..models.my_module import MyClass",
        "from typing import Dict",
        "from typing import cast",
    }


def test_resolve_references(mocker):
    import openapi_python_client.schema as oai
    from openapi_python_client.parser.properties import build_model_property

    schemas = {
        "RefA": oai.Schema.construct(
            title=mocker.MagicMock(),
            description=mocker.MagicMock(),
            required=["String"],
            properties={
                "String": oai.Schema.construct(type="string"),
                "Enum": oai.Schema.construct(type="string", enum=["aValue"]),
                "DateTime": oai.Schema.construct(type="string", format="date-time"),
            },
        ),
        "RefB": oai.Schema.construct(
            title=mocker.MagicMock(),
            description=mocker.MagicMock(),
            required=["DateTime"],
            properties={
                "Int": oai.Schema.construct(type="integer"),
                "DateTime": oai.Schema.construct(type="string", format="date-time"),
                "Float": oai.Schema.construct(type="number", format="float"),
            },
        ),
        # Intentionally no properties defined
        "RefC": oai.Schema.construct(
            title=mocker.MagicMock(),
            description=mocker.MagicMock(),
        ),
    }

    model_schema = oai.Schema.construct(
        allOf=[
            oai.Reference.construct(ref="#/components/schemas/RefA"),
            oai.Reference.construct(ref="#/components/schemas/RefB"),
            oai.Reference.construct(ref="#/components/schemas/RefC"),
            oai.Schema.construct(
                title=mocker.MagicMock(),
                description=mocker.MagicMock(),
                required=["Float"],
                properties={
                    "String": oai.Schema.construct(type="string"),
                    "Float": oai.Schema.construct(type="number", format="float"),
                },
            ),
        ]
    )

    components = {**schemas, "Model": model_schema}

    from openapi_python_client.parser.properties import Schemas

    schemas_holder = Schemas()
    model, schemas_holder = build_model_property(
        data=model_schema, name="Model", required=True, schemas=schemas_holder, parent_name=None
    )
    model.resolve_references(components, schemas_holder)
    assert sorted(p.name for p in model.required_properties) == ["DateTime", "Float", "String"]
    assert all(p.required for p in model.required_properties)
    assert sorted(p.name for p in model.optional_properties) == ["Enum", "Int"]
    assert all(not p.required for p in model.optional_properties)


def test_resolve_references_nested_allof(mocker):
    import openapi_python_client.schema as oai
    from openapi_python_client.parser.properties import build_model_property

    schemas = {
        "RefA": oai.Schema.construct(
            title=mocker.MagicMock(),
            description=mocker.MagicMock(),
            required=["String"],
            properties={
                "String": oai.Schema.construct(type="string"),
                "Enum": oai.Schema.construct(type="string", enum=["aValue"]),
                "DateTime": oai.Schema.construct(type="string", format="date-time"),
            },
        ),
        "RefB": oai.Schema.construct(
            title=mocker.MagicMock(),
            description=mocker.MagicMock(),
            required=["DateTime"],
            properties={
                "Int": oai.Schema.construct(type="integer"),
                "DateTime": oai.Schema.construct(type="string", format="date-time"),
                "Float": oai.Schema.construct(type="number", format="float"),
            },
        ),
        # Intentionally no properties defined
        "RefC": oai.Schema.construct(
            title=mocker.MagicMock(),
            description=mocker.MagicMock(),
        ),
    }

    model_schema = oai.Schema.construct(
        type="object",
        properties={
            "Key": oai.Schema.construct(
                allOf=[
                    oai.Reference.construct(ref="#/components/schemas/RefA"),
                    oai.Reference.construct(ref="#/components/schemas/RefB"),
                    oai.Reference.construct(ref="#/components/schemas/RefC"),
                    oai.Schema.construct(
                        title=mocker.MagicMock(),
                        description=mocker.MagicMock(),
                        required=["Float"],
                        properties={
                            "String": oai.Schema.construct(type="string"),
                            "Float": oai.Schema.construct(type="number", format="float"),
                        },
                    ),
                ]
            ),
        },
    )

    components = {**schemas, "Model": model_schema}

    from openapi_python_client.parser.properties import ModelProperty, Schemas

    schemas_holder = Schemas()
    model, schemas_holder = build_model_property(
        data=model_schema, name="Model", required=True, schemas=schemas_holder, parent_name=None
    )
    model.resolve_references(components, schemas_holder)
    assert sorted(p.name for p in model.required_properties) == []
    assert sorted(p.name for p in model.optional_properties) == ["Key"]
    assert all(not p.required for p in model.optional_properties)

    key_property = model.optional_properties[0]
    assert isinstance(key_property, ModelProperty)
    key_property.resolve_references(components, schemas_holder)
    assert sorted(p.name for p in key_property.required_properties) == ["DateTime", "Float", "String"]
    assert all(p.required for p in key_property.required_properties)
    assert sorted(p.name for p in key_property.optional_properties) == ["Enum", "Int"]
    assert all(not p.required for p in key_property.optional_properties)
