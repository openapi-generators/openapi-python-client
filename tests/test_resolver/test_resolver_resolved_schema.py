import pathlib
import urllib
import urllib.parse

import pytest


def test__resolved_schema_with_resolved_external_references():

    from openapi_python_client.resolver.resolved_schema import ResolvedSchema

    root_schema = {"foobar": {"$ref": "foobar.yaml#/foo"}}
    external_schemas = {"/home/user/foobar.yaml": {"foo": {"description": "foobar_description"}}}
    errors = []

    resolved_schema = ResolvedSchema(root_schema, external_schemas, errors, "/home/user").schema

    assert len(errors) == 0
    assert "foo" in resolved_schema
    assert "foobar" in resolved_schema
    assert "$ref" in resolved_schema["foobar"]
    assert "#/foo" in resolved_schema["foobar"]["$ref"]
    assert "description" in resolved_schema["foo"]
    assert "foobar_description" in resolved_schema["foo"]["description"]


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


def test__resolved_schema_with_conflicts():

    from openapi_python_client.resolver.resolved_schema import ResolvedSchema

    root_schema = {
        "foobar": {"$ref": "first_instance.yaml#/foo"},
        "barfoo": {"$ref": "second_instance.yaml#/foo"},
        "foobarfoo": {"$ref": "second_instance.yaml#/foo"},
        "barfoobar": {"$ref": "first_instance.yaml#/foo"},
    }

    external_schemas = {
        "/home/user/first_instance.yaml": {"foo": {"description": "foo_first_description"}},
        "/home/user/second_instance.yaml": {"foo": {"description": "foo_second_description"}},
    }

    current_result = {
        "foobar": {"$ref": "#/foo"},
        "barfoo": {"$ref": "#/foo"},
        "foobarfoo": {"$ref": "#/foo"},
        "barfoobar": {"$ref": "#/foo"},
        "foo": {"description": "foo_first_description"},
    }

    desired_result = {
        "foobar": {"$ref": "#/foo"},
        "barfoo": {"$ref": "#/foo2"},
        "foobarfoo": {"$ref": "#/foo2"},
        "barfoobar": {"$ref": "#/foo"},
        "foo": {"description": "foo_first_description"},
        "foo2": {"description": "foo_second_description"},
    }

    errors = []

    resolved_schema = ResolvedSchema(root_schema, external_schemas, errors, "/home/user").schema

    print(resolved_schema)
    assert len(errors) == 0
    assert resolved_schema == desired_result
