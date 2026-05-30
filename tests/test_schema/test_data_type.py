import pydantic
import pytest

import openapi_python_client.schema as oai


class TestDataType:
    def test_schema_bad_types(self):
        with pytest.raises(pydantic.ValidationError):
            oai.Schema(type="bad_type")

        with pytest.raises(pydantic.ValidationError):
            oai.Schema(anyOf=[{"type": "garbage"}])

        with pytest.raises(pydantic.ValidationError):
            oai.Schema(
                properties={
                    "bad": oai.Schema(type="not_real"),
                },
            )

    @pytest.mark.parametrize(
        "type_",
        (
            "string",
            "number",
            "integer",
            "boolean",
            "array",
            "object",
        ),
    )
    def test_schema_happy(self, type_):
        assert oai.Schema(type=type_).type == type_
