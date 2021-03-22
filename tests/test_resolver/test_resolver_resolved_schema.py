import pathlib
import urllib
import urllib.parse

import pytest


def test__resolved_schema_with_resolved_external_references():

    from openapi_python_client.resolver.resolved_schema import ResolvedSchema

    root_schema = {"foobar": {"$ref": "foobar.yaml#/foo"}}

    external_schemas = {
        "/home/user/foobar.yaml": {"foo": {"$ref": "/home/user/foobar_2.yaml#/foo"}},
        "/home/user/foobar_2.yaml": {"foo": {"description": "foobar_description"}},
    }
    errors = []

    resolved_schema = ResolvedSchema(root_schema, external_schemas, errors, "/home/user").schema

    assert len(errors) == 0
    assert "foo" in resolved_schema
    assert "foobar" in resolved_schema
    assert "$ref" in resolved_schema["foobar"]
    assert "#/foo" in resolved_schema["foobar"]["$ref"]
    assert "description" in resolved_schema["foo"]
    assert "foobar_description" in resolved_schema["foo"]["description"]


def test__resolved_schema_with_depth_refs():

    from openapi_python_client.resolver.resolved_schema import ResolvedSchema

    root_schema = {"foo": {"$ref": "foo.yaml#/foo"}, "bar": {"$ref": "bar.yaml#/bar"}}

    external_schemas = {
        "/home/user/foo.yaml": {"foo": {"$ref": "bar.yaml#/bar"}},
        "/home/user/bar.yaml": {"bar": {"description": "bar"}},
    }

    errors = []

    expected_result = {"foo": {"$ref": "#/bar"}, "bar": {"description": "bar"}}

    resolved_schema = ResolvedSchema(root_schema, external_schemas, errors, "/home/user").schema

    assert len(errors) == 0
    assert resolved_schema == expected_result


def test__resolved_schema_with_duplicate_ref():

    from openapi_python_client.resolver.resolved_schema import ResolvedSchema

    root_schema = {
        "foo": {"$ref": "foobar.yaml#/foo"},
        "bar": {"$ref": "foobar.yaml#/foo"},
        "list": [{"foobar": {"$ref": "foobar.yaml#/bar"}}, {"barfoo": {"$ref": "foobar.yaml#/bar2/foo"}}],
    }

    external_schemas = {
        "/home/user/foobar.yaml": {
            "foo": {"description": "foo_description"},
            "bar": {"$ref": "#/foo"},
            "bar2": {"foo": {"description": "foo_second_description"}},
        },
    }

    errors = []

    resolved_schema = ResolvedSchema(root_schema, external_schemas, errors, "/home/user").schema

    assert len(errors) == 0


def test__resolved_schema_with_malformed_schema():

    from openapi_python_client.resolver.resolved_schema import ResolvedSchema

    root_schema = {
        "paths": {
            "/foo/bar": {"$ref": "inexistant.yaml#/paths/~1foo~1bar"},
            "/bar": {"$ref": "foobar.yaml#/paths/~1bar"},
        },
        "foo": {"$ref": "inexistant.yaml#/foo"},
    }

    external_schemas = {
        "/home/user/foobar.yaml": {
            "paths": {
                "/foo/bar": {"description": "foobar_description"},
            },
        },
    }

    errors = []

    resolved_schema = ResolvedSchema(root_schema, external_schemas, errors, "/home/user").schema

    assert len(errors) == 4
    assert errors == [
        "Failed to resolve remote reference > /home/user/inexistant.yaml",
        "Failed to read remote value /paths//bar, in remote ref /home/user/foobar.yaml",
        "Failed to resolve remote reference > /home/user/inexistant.yaml",
        "Failed to resolve remote reference > /home/user/inexistant.yaml",
    ]


def test__resolved_schema_with_remote_paths():

    from openapi_python_client.resolver.resolved_schema import ResolvedSchema

    root_schema = {
        "paths": {
            "/foo/bar": {"$ref": "foobar.yaml#/paths/~1foo~1bar"},
            "/foo/bar2": {"$ref": "#/bar2"},
        },
        "bar2": {"description": "bar2_description"},
    }

    external_schemas = {
        "/home/user/foobar.yaml": {
            "paths": {
                "/foo/bar": {"description": "foobar_description"},
            },
        },
    }

    expected_result = {
        "paths": {"/foo/bar": {"description": "foobar_description"}, "/foo/bar2": {"$ref": "#/bar2"}},
        "bar2": {"description": "bar2_description"},
    }

    errors = []

    resolved_schema = ResolvedSchema(root_schema, external_schemas, errors, "/home/user").schema

    assert len(errors) == 0
    assert resolved_schema == expected_result


def test__resolved_schema_with_absolute_paths():

    from openapi_python_client.resolver.resolved_schema import ResolvedSchema

    root_schema = {"foobar": {"$ref": "foobar.yaml#/foo"}, "barfoo": {"$ref": "../barfoo.yaml#/bar"}}

    external_schemas = {
        "/home/user/foobar.yaml": {"foo": {"description": "foobar_description"}},
        "/home/barfoo.yaml": {"bar": {"description": "barfoo_description"}},
    }

    errors = []

    resolved_schema = ResolvedSchema(root_schema, external_schemas, errors, "/home/user").schema

    assert len(errors) == 0
    assert "foo" in resolved_schema
    assert "bar" in resolved_schema
    assert "foobar" in resolved_schema
    assert "barfoo" in resolved_schema
    assert "$ref" in resolved_schema["foobar"]
    assert "#/foo" in resolved_schema["foobar"]["$ref"]
    assert "$ref" in resolved_schema["barfoo"]
    assert "#/bar" in resolved_schema["barfoo"]["$ref"]
    assert "description" in resolved_schema["foo"]
    assert "foobar_description" in resolved_schema["foo"]["description"]
    assert "description" in resolved_schema["bar"]
    assert "barfoo_description" in resolved_schema["bar"]["description"]
