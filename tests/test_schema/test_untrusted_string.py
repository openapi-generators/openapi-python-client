from pydantic import BaseModel

from openapi_python_client.schema.ref import Ref
from openapi_python_client.schema.untrusted_string import UntrustedString


class Model(BaseModel):
    untrusted: UntrustedString


class RefModel(BaseModel):
    ref: Ref


def test_ref_json_serialization():
    """Ref must serialize to its raw value in JSON mode so error messages can include it."""
    m = RefModel.model_validate({"ref": "#/components/schemas/Foo"})
    assert m.model_dump_json() == '{"ref":"#/components/schemas/Foo"}'


def test_untrusted_string_deserialization():
    m = Model.model_validate_json('{"untrusted":"hello"}')
    assert m.untrusted.get_untrusted_value() == "hello"


def test_untrusted_string_json_serialization():
    """UntrustedString must serialize to its raw value in JSON mode so error messages can include it."""
    m = Model.model_validate_json('{"untrusted":"hello"}')
    assert m.model_dump_json() == '{"untrusted":"hello"}'
    # Python mode keeps the wrapper intact so it can't leak into generated code
    assert isinstance(m.model_dump()["untrusted"], UntrustedString)
