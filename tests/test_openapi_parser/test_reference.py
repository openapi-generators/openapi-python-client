def test_from_ref():
    from openapi_python_client.parser.reference import Reference

    r = Reference.from_ref("#/components/schemas/PingResponse")

    assert r.class_name == "PingResponse"
    assert r.module_name == "ping_response"


def test_from_ref_class_overrides():
    from openapi_python_client.parser.reference import Reference, class_overrides

    ref = "#/components/schemas/_MyResponse"
    class_overrides["_MyResponse"] = Reference(class_name="MyResponse", module_name="my_response")

    assert Reference.from_ref(ref) == class_overrides["_MyResponse"]
