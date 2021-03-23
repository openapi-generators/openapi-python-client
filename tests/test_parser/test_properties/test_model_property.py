from typing import Callable

import pytest

import openapi_python_client.schema as oai
from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties import DateTimeProperty, ModelProperty, StringProperty
from openapi_python_client.parser.reference import Reference


@pytest.mark.parametrize(
    "no_optional,nullable,required,json,expected",
    [
        (False, False, False, False, "Union[Unset, MyClass]"),
        (False, False, True, False, "MyClass"),
        (False, True, False, False, "Union[Unset, None, MyClass]"),
        (False, True, True, False, "Optional[MyClass]"),
        (True, False, False, False, "MyClass"),
        (True, False, True, False, "MyClass"),
        (True, True, False, False, "MyClass"),
        (True, True, True, False, "MyClass"),
        (False, False, True, True, "Dict[str, Any]"),
    ],
)
def test_get_type_string(no_optional, nullable, required, json, expected):
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

    assert prop.get_type_string(no_optional=no_optional, json=json) == expected


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


@pytest.fixture
def model_property() -> Callable[..., ModelProperty]:
    from openapi_python_client.parser.reference import Reference

    def _factory(**kwargs):
        kwargs = {
            "name": "",
            "description": "",
            "required": True,
            "nullable": True,
            "default": None,
            "reference": Reference(class_name="", module_name=""),
            "required_properties": [],
            "optional_properties": [],
            "relative_imports": set(),
            "additional_properties": False,
            **kwargs,
        }
        return ModelProperty(**kwargs)

    return _factory


def string_property(**kwargs) -> StringProperty:
    kwargs = {
        "name": "",
        "required": True,
        "nullable": True,
        "default": None,
        **kwargs,
    }
    return StringProperty(**kwargs)


class TestProcessProperties:
    def test_conflicting_properties_different_types(self, model_property):
        from openapi_python_client.parser.properties import Schemas
        from openapi_python_client.parser.properties.model_property import _process_properties

        data = oai.Schema.construct(allOf=[oai.Reference.construct(ref="First"), oai.Reference.construct(ref="Second")])
        schemas = Schemas(
            models={
                "First": model_property(
                    optional_properties=[StringProperty(name="prop", required=True, nullable=True, default=None)]
                ),
                "Second": model_property(
                    optional_properties=[DateTimeProperty(name="prop", required=True, nullable=True, default=None)]
                ),
            }
        )

        result = _process_properties(data=data, schemas=schemas, class_name="")

        assert isinstance(result, PropertyError)

    def test_conflicting_properties_same_types(self, model_property):
        from openapi_python_client.parser.properties import Schemas
        from openapi_python_client.parser.properties.model_property import _process_properties

        data = oai.Schema.construct(allOf=[oai.Reference.construct(ref="First"), oai.Reference.construct(ref="Second")])
        schemas = Schemas(
            models={
                "First": model_property(optional_properties=[string_property(default="abc")]),
                "Second": model_property(optional_properties=[string_property()]),
            }
        )

        result = _process_properties(data=data, schemas=schemas, class_name="")

        assert isinstance(result, PropertyError)

    def test_duplicate_properties(self, model_property):
        from openapi_python_client.parser.properties import Schemas
        from openapi_python_client.parser.properties.model_property import _process_properties

        data = oai.Schema.construct(allOf=[oai.Reference.construct(ref="First"), oai.Reference.construct(ref="Second")])
        prop = string_property()
        schemas = Schemas(
            models={
                "First": model_property(optional_properties=[prop]),
                "Second": model_property(optional_properties=[prop]),
            }
        )

        result = _process_properties(data=data, schemas=schemas, class_name="")

        assert result.optional_props == [prop], "There should only be one copy of duplicate properties"

    @pytest.mark.parametrize("first_nullable", [True, False])
    @pytest.mark.parametrize("second_nullable", [True, False])
    @pytest.mark.parametrize("first_required", [True, False])
    @pytest.mark.parametrize("second_required", [True, False])
    def test_mixed_requirements(self, model_property, first_nullable, second_nullable, first_required, second_required):
        from openapi_python_client.parser.properties import Schemas
        from openapi_python_client.parser.properties.model_property import _process_properties

        data = oai.Schema.construct(allOf=[oai.Reference.construct(ref="First"), oai.Reference.construct(ref="Second")])
        schemas = Schemas(
            models={
                "First": model_property(
                    optional_properties=[string_property(required=first_required, nullable=first_nullable)]
                ),
                "Second": model_property(
                    optional_properties=[string_property(required=second_required, nullable=second_nullable)]
                ),
            }
        )

        result = _process_properties(data=data, schemas=schemas, class_name="")

        nullable = first_nullable and second_nullable
        required = first_required or second_required
        expected_prop = string_property(
            nullable=nullable,
            required=required,
        )

        if nullable or not required:
            assert result.optional_props == [expected_prop]
        else:
            assert result.required_props == [expected_prop]

    def test_direct_properties_non_ref(self):
        from openapi_python_client.parser.properties import Schemas
        from openapi_python_client.parser.properties.model_property import _process_properties

        data = oai.Schema.construct(
            allOf=[
                oai.Schema.construct(
                    required=["first"],
                    properties={
                        "first": oai.Schema.construct(type="string"),
                        "second": oai.Schema.construct(type="string"),
                    },
                )
            ]
        )
        schemas = Schemas()

        result = _process_properties(data=data, schemas=schemas, class_name="")

        assert result.optional_props == [string_property(name="second", required=False, nullable=False)]
        assert result.required_props == [string_property(name="first", required=True, nullable=False)]
