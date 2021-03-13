import pytest

import openapi_python_client.schema as oai
from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties import DateTimeProperty, ModelProperty, StringProperty
from openapi_python_client.parser.reference import Reference


@pytest.mark.parametrize(
    "no_optional,nullable,required,expected",
    [
        (False, False, False, "Union[MyClass, Unset]"),
        (False, False, True, "MyClass"),
        (False, True, False, "Union[Optional[MyClass], Unset]"),
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


class TestBuildModelProperty:
    @pytest.mark.parametrize(
        "additional_properties_schema, expected_additional_properties",
        [
            (True, True),
            (oai.Schema.construct(), True),
            (None, True),
            (False, False),
            (
                oai.Schema.construct(type="string"),
                StringProperty(name="AdditionalProperty", required=True, nullable=False, default=None),
            ),
        ],
    )
    def test_additional_schemas(self, additional_properties_schema, expected_additional_properties):
        from openapi_python_client.parser.properties import Schemas, build_model_property

        data = oai.Schema.construct(
            additionalProperties=additional_properties_schema,
        )

        model, _ = build_model_property(
            data=data,
            name="prop",
            schemas=Schemas(),
            required=True,
            parent_name="parent",
        )

        assert model.additional_properties == expected_additional_properties

    def test_happy_path(self):
        from openapi_python_client.parser.properties import Schemas, build_model_property

        data = oai.Schema.construct(
            required=["req"],
            title="MyModel",
            properties={
                "req": oai.Schema.construct(type="string"),
                "opt": oai.Schema(type="string", format="date-time"),
            },
            description="A class called MyModel",
            nullable=False,
        )
        schemas = Schemas(models={"OtherModel": None})

        model, new_schemas = build_model_property(
            data=data,
            name="prop",
            schemas=schemas,
            required=True,
            parent_name="parent",
        )

        assert new_schemas != schemas
        assert new_schemas.models == {
            "OtherModel": None,
            "ParentMyModel": model,
        }
        assert model == ModelProperty(
            name="prop",
            required=True,
            nullable=False,
            default=None,
            reference=Reference(class_name="ParentMyModel", module_name="parent_my_model"),
            required_properties=[StringProperty(name="req", required=True, nullable=False, default=None)],
            optional_properties=[DateTimeProperty(name="opt", required=False, nullable=False, default=None)],
            description=data.description,
            relative_imports={
                "from dateutil.parser import isoparse",
                "from typing import cast",
                "import datetime",
                "from ..types import UNSET, Unset",
                "from typing import Union",
            },
            additional_properties=True,
        )

    def test_model_name_conflict(self):
        from openapi_python_client.parser.properties import Schemas, build_model_property

        data = oai.Schema.construct()
        schemas = Schemas(models={"OtherModel": None})

        err, new_schemas = build_model_property(
            data=data,
            name="OtherModel",
            schemas=schemas,
            required=True,
            parent_name=None,
        )

        assert new_schemas == schemas
        assert err == PropertyError(detail='Attempted to generate duplicate models with name "OtherModel"', data=data)

    def test_bad_props_return_error(self):
        from openapi_python_client.parser.properties import Schemas, build_model_property

        data = oai.Schema(
            properties={
                "bad": oai.Schema(type="not_real"),
            },
        )
        schemas = Schemas()

        err, new_schemas = build_model_property(
            data=data,
            name="prop",
            schemas=schemas,
            required=True,
            parent_name=None,
        )

        assert new_schemas == schemas
        assert err == PropertyError(detail="unknown type not_real", data=oai.Schema(type="not_real"))

    def test_bad_additional_props_return_error(self):
        from openapi_python_client.parser.properties import Schemas, build_model_property

        additional_properties = oai.Schema(
            type="object",
            properties={
                "bad": oai.Schema(type="not_real"),
            },
        )
        data = oai.Schema(additionalProperties=additional_properties)
        schemas = Schemas()

        err, new_schemas = build_model_property(
            data=data,
            name="prop",
            schemas=schemas,
            required=True,
            parent_name=None,
        )

        assert new_schemas == schemas
        assert err == PropertyError(detail="unknown type not_real", data=oai.Schema(type="not_real"))
