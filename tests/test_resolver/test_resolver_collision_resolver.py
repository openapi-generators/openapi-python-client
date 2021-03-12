import pathlib
import urllib
import urllib.parse

import pytest


def test__collision_resolver():

    from openapi_python_client.resolver.collision_resolver import CollisionResolver
    from openapi_python_client.resolver.resolved_schema import ResolvedSchema

    root_schema = {
        "foobar": {"$ref": "first_instance.yaml#/foo"},
        "barfoo": {"$ref": "second_instance.yaml#/foo"},
        "barbarfoo": {"$ref": "third_instance.yaml#/foo"},
        "foobarfoo": {"$ref": "second_instance.yaml#/foo"},
        "barfoobar": {"$ref": "first_instance.yaml#/bar/foo"},
        "localref": {"$ref": "#/local_ref"},
        "local_ref": {"description": "a local ref"},
        "last": {"$ref": "first_instance.yaml#/fourth_instance"},
    }

    external_schemas = {
        "/home/user/first_instance.yaml": {
            "foo": {"description": "foo_first_description"},
            "bar": {"foo": {"description": "nested foo"}},
            "fourth_instance": {"$ref": "fourth_instance.yaml#/foo"},
        },
        "/home/user/second_instance.yaml": {"foo": {"description": "foo_second_description"}},
        "/home/user/third_instance.yaml": {"foo": {"description": "foo_third_description"}},
        "/home/user/fourth_instance.yaml": {"foo": {"description": "foo_fourth_description"}},
    }

    desired_result = {
        "foobar": {"$ref": "#/foo"},
        "barfoo": {"$ref": "#/foo_2"},
        "barbarfoo": {"$ref": "#/foo_3"},
        "foobarfoo": {"$ref": "#/foo_2"},
        "barfoobar": {"$ref": "#/bar/foo"},
        "localref": {"$ref": "#/local_ref"},
        "local_ref": {"description": "a local ref"},
        "last": {"$ref": "#/fourth_instance"},
        "foo": {"description": "foo_first_description"},
        "foo_2": {"description": "foo_second_description"},
        "foo_3": {"description": "foo_third_description"},
        "bar": {"foo": {"description": "nested foo"}},
        "foo_4": {"description": "foo_fourth_description"},
        "fourth_instance": {"$ref": "#/foo_4"},
    }
    errors = []

    CollisionResolver(root_schema, external_schemas, errors, "/home/user").resolve()
    resolved_schema = ResolvedSchema(root_schema, external_schemas, errors, "/home/user").schema

    print(resolved_schema)
    assert len(errors) == 0
    assert resolved_schema == desired_result
