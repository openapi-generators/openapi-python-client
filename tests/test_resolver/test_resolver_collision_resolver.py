import pathlib
import urllib
import urllib.parse

import pytest


def test__collision_resolver_get_schema_from_ref():

    from openapi_python_client.resolver.collision_resolver import CollisionResolver

    root_schema = {"foo": {"$ref": "first_instance.yaml#/foo"}}

    external_schemas = {"/home/user/first_instance.yaml": {"food": {"description": "food_first_description"}}}

    errors = []

    CollisionResolver(root_schema, external_schemas, errors, "/home/user").resolve()

    assert len(errors) == 1
    assert errors == ["Did not find data corresponding to the reference first_instance.yaml#/foo"]


def test__collision_resolver_duplicate_schema():

    from openapi_python_client.resolver.collision_resolver import CollisionResolver

    root_schema = {
        "foo": {"$ref": "first_instance.yaml#/foo"},
        "bar": {"$ref": "second_instance.yaml#/bar/foo"},
    }

    external_schemas = {
        "/home/user/first_instance.yaml": {"foo": {"description": "foo_first_description"}},
        "/home/user/second_instance.yaml": {"bar": {"foo": {"description": "foo_first_description"}}},
    }

    errors = []

    CollisionResolver(root_schema, external_schemas, errors, "/home/user").resolve()

    assert len(errors) == 1
    assert errors == ["Found a duplicate schema in first_instance.yaml#/foo and second_instance.yaml#/bar/foo"]


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
        "array": ["array_item_one", "array_item_two"],
        "last": {"$ref": "first_instance.yaml#/fourth_instance"},
        "baz": {"$ref": "fifth_instance.yaml#/foo"},
    }

    external_schemas = {
        "/home/user/first_instance.yaml": {
            "foo": {"description": "foo_first_description"},
            "bar": {"foo": {"description": "nested foo"}},
            "fourth_instance": {"$ref": "fourth_instance.yaml#/foo"},
        },
        "/home/user/second_instance.yaml": {
            "foo": {"description": "foo_second_description"},
            "another_local_ref": {"$ref": "#/foo"},
        },
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
        "array": ["array_item_one", "array_item_two"],
        "last": {"$ref": "first_instance.yaml#/fourth_instance"},
        "baz": {"$ref": "fifth_instance.yaml#/foo_2"},
    }

    external_schemas_result = {
        "/home/user/first_instance.yaml": {
            "foo": {"description": "foo_first_description"},
            "bar": {"foo": {"description": "nested foo"}},
            "fourth_instance": {"$ref": "fourth_instance.yaml#/foo_4"},
        },
        "/home/user/second_instance.yaml": {
            "foo_2": {"description": "foo_second_description"},
            "another_local_ref": {"$ref": "#/foo_2"},
        },
        "/home/user/third_instance.yaml": {"foo_3": {"description": "foo_third_description"}},
        "/home/user/fourth_instance.yaml": {"foo_4": {"description": "foo_fourth_description"}},
        "/home/user/fifth_instance.yaml": {"foo_2": {"description": "foo_second_description"}},
    }

    errors = []

    CollisionResolver(root_schema, external_schemas, errors, "/home/user").resolve()

    assert len(errors) == 0
    assert root_schema == root_schema_result
    assert external_schemas == external_schemas_result


def test__collision_resolver_deep_root_keys():

    from openapi_python_client.resolver.collision_resolver import CollisionResolver

    root_schema = {
        "foobar": {"$ref": "first_instance.yaml#/bar/foo"},
        "barfoo": {"$ref": "second_instance.yaml#/bar/foo"},
        "barfoobar": {"$ref": "second_instance.yaml#/barfoobar"},
    }

    external_schemas = {
        "/home/user/first_instance.yaml": {
            "bar": {"foo": {"description": "foo_first_description"}},
        },
        "/home/user/second_instance.yaml": {
            "bar": {"foo": {"description": "foo_second_description"}},
            "barfoobar": {
                "type": "object",
                "allOf": [{"description": "first_description"}, {"description": "second_description"}],
            },
        },
    }

    root_schema_result = {
        "foobar": {"$ref": "first_instance.yaml#/bar/foo"},
        "barfoo": {"$ref": "second_instance.yaml#/bar/foo_2"},
        "barfoobar": {"$ref": "second_instance.yaml#/barfoobar"},
    }

    external_schemas_result = {
        "/home/user/first_instance.yaml": {
            "bar": {"foo": {"description": "foo_first_description"}},
        },
        "/home/user/second_instance.yaml": {
            "bar": {"foo_2": {"description": "foo_second_description"}},
            "barfoobar": {
                "type": "object",
                "allOf": [{"description": "first_description"}, {"description": "second_description"}],
            },
        },
    }

    errors = []

    CollisionResolver(root_schema, external_schemas, errors, "/home/user").resolve()

    assert len(errors) == 0
    assert root_schema == root_schema_result
    assert external_schemas == external_schemas_result
