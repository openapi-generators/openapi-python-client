from openapi_python_client.schema import DataType, Schema


def test_nullable_with_simple_type():
    schema = Schema.model_validate_json('{"type": "string", "nullable": true}')
    assert schema.type == [DataType.STRING, DataType.NULL]


def test_nullable_with_allof():
    schema = Schema.model_validate_json('{"allOf": [{"type": "string"}], "nullable": true}')
    assert schema.oneOf == [Schema(type=DataType.NULL), Schema(allOf=[Schema(type=DataType.STRING)])]
    assert schema.allOf == []
