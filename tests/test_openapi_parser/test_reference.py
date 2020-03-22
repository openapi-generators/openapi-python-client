def test_from_ref():
    from openapi_python_client.openapi_parser.reference import Reference

    r = Reference.from_ref("#/components/schemas/PingResponse")

    assert r.class_name == "PingResponse"
    assert r.module_name == "ping_response"
