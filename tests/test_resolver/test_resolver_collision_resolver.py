import pathlib
import urllib
import urllib.parse

import pytest


def test__collision_resolver():

    from openapi_python_client.resolver.collision_resolver import CollisionResolver

    root_schema = {
        "foobar": {"$ref": "first_instance.yaml#/foo"},
        "barfoo": {"$ref": "second_instance.yaml#/foo"},
        "barbarfoo": {"$ref": "third_instance.yaml#/foo"},
        "foobarfoo": {"$ref": "second_instance.yaml#/foo"},
        "barfoobar": {"$ref": "first_instance.yaml#/bar/foo"},
        "localref": {"$ref": "#/local_ref"},
        "local_ref": {"description": "a local ref"},
        "last": {"$ref": "first_instance.yaml#/fourth_instance"},
        "baz": {"$ref": "fifth_instance.yaml#/foo"},
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
        "/home/user/fifth_instance.yaml": {"foo": {"description": "foo_second_description"}},
    }

    root_schema_result = {
        "foobar": {"$ref": "first_instance.yaml#/foo"},
        "barfoo": {"$ref": "second_instance.yaml#/foo_2"},
        "barbarfoo": {"$ref": "third_instance.yaml#/foo_3"},
        "foobarfoo": {"$ref": "second_instance.yaml#/foo_2"},
        "barfoobar": {"$ref": "first_instance.yaml#/bar/foo"},
        "localref": {"$ref": "#/local_ref"},
        "local_ref": {"description": "a local ref"},
        "last": {"$ref": "first_instance.yaml#/fourth_instance"},
        "baz": {"$ref": "fifth_instance.yaml#/foo_2"},
    }

    external_schemas_result = {
        "/home/user/first_instance.yaml": {
            "foo": {"description": "foo_first_description"},
            "bar": {"foo": {"description": "nested foo"}},
            "fourth_instance": {"$ref": "fourth_instance.yaml#/foo_4"},
        },
        "/home/user/second_instance.yaml": {"foo_2": {"description": "foo_second_description"}},
        "/home/user/third_instance.yaml": {"foo_3": {"description": "foo_third_description"}},
        "/home/user/fourth_instance.yaml": {"foo_4": {"description": "foo_fourth_description"}},
        "/home/user/fifth_instance.yaml": {"foo_2": {"description": "foo_second_description"}},
    }

    errors = []

    CollisionResolver(root_schema, external_schemas, errors, "/home/user").resolve()

    assert len(errors) == 0
    assert root_schema == root_schema_result
    assert external_schemas == external_schemas_result
