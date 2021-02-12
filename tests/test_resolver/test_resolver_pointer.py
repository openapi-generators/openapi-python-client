import pytest


def get_data_set():
    # https://tools.ietf.org/html/rfc6901
    return {
        "valid_pointers": [
            "/myElement",
            "/definitions/myElement",
            "",
            "/foo",
            "/foo/0",
            "/",
            "/a~1b",
            "/c%d",
            "/e^f",
            "/g|h",
            "/i\\j" '/k"l',
            "/ ",
            "/m~0n",
            "/m~01",
        ],
        "invalid_pointers": ["../foo", "foobar", None],
        "tokens_by_pointer": {
            "/myElement": ["", "myElement"],
            "/definitions/myElement": ["", "definitions", "myElement"],
            "": [""],
            "/foo": ["", "foo"],
            "/foo/0": ["", "foo", "0"],
            "/": ["", ""],
            "/a~1b": ["", "a/b"],
            "/c%d": ["", "c%d"],
            "/e^f": ["", "e^f"],
            "/g|h": ["", "g|h"],
            "/i\\j": ["", "i\\j"],
            '/k"l': ["", 'k"l'],
            "/ ": ["", " "],
            "/m~0n": ["", "m~n"],
            "/m~01": ["", "m~1"],
        },
    }


def test___init__():
    from openapi_python_client.resolver.pointer import Pointer

    data_set = get_data_set()

    for pointer_str in data_set["valid_pointers"]:
        p = Pointer(pointer_str)
        assert p.value != None
        assert p.value == pointer_str

    for pointer_str in data_set["invalid_pointers"]:
        with pytest.raises(ValueError):
            p = Pointer(pointer_str)


def test_token():
    from openapi_python_client.resolver.pointer import Pointer

    data_set = get_data_set()

    for pointer_str in data_set["tokens_by_pointer"].keys():
        p = Pointer(pointer_str)
        expected_tokens = data_set["tokens_by_pointer"][pointer_str]

        for idx, token in enumerate(p.tokens()):
            assert expected_tokens[idx] == token


def test_parent():
    from openapi_python_client.resolver.pointer import Pointer

    data_set = get_data_set()

    for pointer_str in data_set["tokens_by_pointer"].keys():
        p = Pointer(pointer_str)
        expected_tokens = data_set["tokens_by_pointer"][pointer_str]

        while p.parent is not None:
            p = p.parent
            expected_tokens.pop()
            assert p.tokens()[-1] == expected_tokens[-1]
            assert len(p.tokens()) == len(expected_tokens)

        assert len(expected_tokens) == 1
        assert expected_tokens[-1] == ""


def test__unescape_and__escape():
    from openapi_python_client.resolver.pointer import Pointer

    escaped_unescaped_values = [("/m~0n", "/m~n"), ("/m~01", "/m~1"), ("/a~1b", "/a/b"), ("/foobar", "/foobar")]

    for escaped, unescaped in escaped_unescaped_values:
        assert Pointer(escaped).unescapated_value == unescaped
