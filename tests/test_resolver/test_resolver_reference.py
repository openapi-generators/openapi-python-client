import pytest


def get_data_set():
    # https://swagger.io/docs/specification/using-ref/
    return {
        "local_references": ["#/definitions/myElement"],
        "remote_references": [
            "document.json#/myElement",
            "../document.json#/myElement",
            "../another-folder/document.json#/myElement",
        ],
        "url_references": [
            "http://path/to/your/resource",
            "http://path/to/your/resource.json#myElement",
            "//anotherserver.com/files/example.json",
        ],
        "relative_references": [
            "#/definitions/myElement",
            "document.json#/myElement",
            "../document.json#/myElement",
            "../another-folder/document.json#/myElement",
        ],
        "absolute_references": [
            "http://path/to/your/resource",
            "http://path/to/your/resource.json#myElement",
            "//anotherserver.com/files/example.json",
        ],
        "full_document_references": [
            "http://path/to/your/resource",
            "//anotherserver.com/files/example.json",
        ],
        "not_full_document_references": [
            "#/definitions/myElement",
            "document.json#/myElement",
            "../document.json#/myElement",
            "../another-folder/document.json#/myElement",
            "http://path/to/your/resource.json#myElement",
        ],
        "path_by_reference": {
            "#/definitions/myElement": "",
            "document.json#/myElement": "document.json",
            "../document.json#/myElement": "../document.json",
            "../another-folder/document.json#/myElement": "../another-folder/document.json",
            "http://path/to/your/resource": "http://path/to/your/resource",
            "http://path/to/your/resource.json#myElement": "http://path/to/your/resource.json",
            "//anotherserver.com/files/example.json": "//anotherserver.com/files/example.json",
        },
        "pointer_by_reference": {
            "#/definitions/myElement": "/definitions/myElement",
            "document.json#/myElement": "/myElement",
            "../document.json#/myElement": "/myElement",
            "../another-folder/document.json#/myElement": "/myElement",
            "http://path/to/your/resource": "",
            "http://path/to/your/resource.json#myElement": "/myElement",
            "//anotherserver.com/files/example.json": "",
        },
        "pointerparent_by_reference": {
            "#/definitions/myElement": "/definitions",
            "document.json#/myElement": "",
            "../document.json#/myElement": "",
            "../another-folder/document.json#/myElement": "",
            "http://path/to/your/resource": None,
            "http://path/to/your/resource.json#myElement": "",
            "//anotherserver.com/files/example.json": None,
        },
    }


def test_is_local():
    from openapi_python_client.resolver.reference import Reference

    data_set = get_data_set()

    for ref_str in data_set["local_references"]:
        ref = Reference(ref_str)
        assert ref.is_local() == True

    for ref_str in data_set["remote_references"]:
        ref = Reference(ref_str)
        assert ref.is_local() == False

    for ref_str in data_set["url_references"]:
        ref = Reference(ref_str)
        assert ref.is_local() == False


def test_is_remote():
    from openapi_python_client.resolver.reference import Reference

    data_set = get_data_set()

    for ref_str in data_set["local_references"]:
        ref = Reference(ref_str)
        assert ref.is_remote() == False

    for ref_str in data_set["remote_references"]:
        ref = Reference(ref_str)
        assert ref.is_remote() == True

    for ref_str in data_set["url_references"]:
        ref = Reference(ref_str)
        assert ref.is_remote() == True


def test_is_url():
    from openapi_python_client.resolver.reference import Reference

    data_set = get_data_set()

    for ref_str in data_set["local_references"]:
        ref = Reference(ref_str)
        assert ref.is_url() == False

    for ref_str in data_set["remote_references"]:
        ref = Reference(ref_str)
        assert ref.is_url() == False

    for ref_str in data_set["url_references"]:
        ref = Reference(ref_str)
        assert ref.is_url() == True


def test_is_absolute():
    from openapi_python_client.resolver.reference import Reference

    data_set = get_data_set()

    for ref_str in data_set["absolute_references"]:
        ref = Reference(ref_str)
        assert ref.is_absolute() == True

    for ref_str in data_set["relative_references"]:
        ref = Reference(ref_str)
        assert ref.is_absolute() == False


def test_is_relative():
    from openapi_python_client.resolver.reference import Reference

    data_set = get_data_set()

    for ref_str in data_set["absolute_references"]:
        ref = Reference(ref_str)
        assert ref.is_relative() == False

    for ref_str in data_set["relative_references"]:
        ref = Reference(ref_str)
        assert ref.is_relative() == True


def test_pointer():
    from openapi_python_client.resolver.reference import Reference

    data_set = get_data_set()

    for ref_str in data_set["pointer_by_reference"].keys():
        ref = Reference(ref_str)
        pointer = data_set["pointer_by_reference"][ref_str]
        assert ref.pointer.value == pointer


def test_pointer_parent():
    from openapi_python_client.resolver.reference import Reference

    data_set = get_data_set()

    for ref_str in data_set["pointerparent_by_reference"].keys():
        ref = Reference(ref_str)
        pointer_parent = data_set["pointerparent_by_reference"][ref_str]

        if pointer_parent is not None:
            assert ref.pointer.parent.value == pointer_parent
        else:
            assert ref.pointer.parent == None


def test_path():
    from openapi_python_client.resolver.reference import Reference

    data_set = get_data_set()

    for ref_str in data_set["path_by_reference"].keys():
        ref = Reference(ref_str)
        path = data_set["path_by_reference"][ref_str]
        assert ref.path == path


def test_is_full_document():
    from openapi_python_client.resolver.reference import Reference

    data_set = get_data_set()

    for ref_str in data_set["full_document_references"]:
        ref = Reference(ref_str)
        assert ref.is_full_document() == True
        assert ref.pointer.parent == None

    for ref_str in data_set["not_full_document_references"]:
        ref = Reference(ref_str)
        assert ref.is_full_document() == False
        assert ref.pointer.parent != None


def test_value():
    from openapi_python_client.resolver.reference import Reference

    ref = Reference("fooBaR")
    assert ref.value == "fooBaR"

    ref = Reference("FooBAR")
    assert ref.value == "FooBAR"
