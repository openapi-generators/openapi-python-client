import pathlib
import urllib
import urllib.parse

import pytest


def test___init__invalid_data(mocker):
    from openapi_python_client.resolver.schema_resolver import SchemaResolver

    with pytest.raises(ValueError):
        SchemaResolver(None)

    invalid_url = "foobar"
    with pytest.raises(ValueError):
        SchemaResolver(invalid_url)

    invalid_url = 42
    with pytest.raises(urllib.error.URLError):
        SchemaResolver(invalid_url)

    invalid_url = mocker.Mock()
    with pytest.raises(urllib.error.URLError):
        SchemaResolver(invalid_url)


def test__init_with_filepath(mocker):
    mocker.patch("openapi_python_client.resolver.schema_resolver.SchemaResolver._isapath", return_value=True)
    mocker.patch("openapi_python_client.resolver.schema_resolver.DataLoader.load", return_value={})
    path = mocker.MagicMock()

    from openapi_python_client.resolver.schema_resolver import SchemaResolver

    resolver = SchemaResolver(path)
    resolver.resolve()

    path.absolute().read_bytes.assert_called_once()


def test__init_with_url(mocker):
    mocker.patch("openapi_python_client.resolver.schema_resolver.DataLoader.load", return_value={})
    url_parse = mocker.patch(
        "urllib.parse.urlparse",
        return_value=urllib.parse.ParseResult(
            scheme="http", netloc="foobar.io", path="foo", params="", query="", fragment="/bar"
        ),
    )
    get = mocker.patch("httpx.get")

    url = mocker.MagicMock()

    from openapi_python_client.resolver.schema_resolver import SchemaResolver

    resolver = SchemaResolver(url)
    resolver.resolve()

    url_parse.assert_called_once_with(url)
    get.assert_called_once()


def test__resolve_schema_references_with_path(mocker):
    read_bytes = mocker.patch("pathlib.Path.read_bytes")

    from openapi_python_client.resolver.schema_resolver import SchemaResolver

    path = pathlib.Path("/foo/bar/foobar")
    path_parent = str(path.parent)
    schema = {"foo": {"$ref": "foobar#/foobar"}}
    external_schemas = {}
    errors = []

    def _datalaod_mocked_result(path, data):
        if path == "/foo/bar/foobar":
            return {"foobar": "bar", "bar": {"$ref": "bar#/foobar"}, "local": {"$ref": "#/toto"}}

        if path == "/foo/bar/bar":
            return {"foobar": "bar", "bar": {"$ref": "../bar#/foobar"}}

        if path == "/foo/bar":
            return {"foobar": "bar/bar", "bar": {"$ref": "/barfoo.io/foobar#foobar"}}

        if path == "/barfoo.io/foobar":
            return {"foobar": "barfoo.io/foobar", "bar": {"$ref": "./bar#foobar"}}

        if path == "/barfoo.io/bar":
            return {"foobar": "barfoo.io/bar", "bar": {"$ref": "/bar.foo/foobar"}}

        if path == "/bar.foo/foobar":
            return {"foobar": "bar.foo/foobar", "bar": {"$ref": "/foo.bar/foobar"}}

        if path == "/foo.bar/foobar":
            return {"foobar": "foo.bar/foobar", "bar": {"$ref": "/foo/bar/foobar"}}  # Loop to first path

        raise ValueError(f"Unexpected path {path}")

    mocker.patch("openapi_python_client.resolver.schema_resolver.DataLoader.load", _datalaod_mocked_result)
    resolver = SchemaResolver(path)
    resolver._resolve_schema_references(path_parent, schema, external_schemas, errors, True)

    assert len(errors) == 0
    assert "/foo/bar/foobar" in external_schemas
    assert "/foo/bar/bar" in external_schemas
    assert "/foo/bar" in external_schemas
    assert "/barfoo.io/foobar" in external_schemas
    assert "/barfoo.io/bar" in external_schemas
    assert "/bar.foo/foobar" in external_schemas
    assert "/foo.bar/foobar" in external_schemas


def test__resolve_schema_references_with_url(mocker):
    get = mocker.patch("httpx.get")

    from openapi_python_client.resolver.schema_resolver import SchemaResolver

    url = "http://foobar.io/foo/bar/foobar"
    url_parent = "http://foobar.io/foo/bar/"
    schema = {"foo": {"$ref": "foobar#/foobar"}}
    external_schemas = {}
    errors = []

    def _datalaod_mocked_result(url, data):
        if url == "http://foobar.io/foo/bar/foobar":
            return {"foobar": "bar", "bar": {"$ref": "bar#/foobar"}, "local": {"$ref": "#/toto"}}

        if url == "http://foobar.io/foo/bar/bar":
            return {"foobar": "bar", "bar": {"$ref": "../bar#/foobar"}}

        if url == "http://foobar.io/foo/bar":
            return {"foobar": "bar/bar", "bar": {"$ref": "//barfoo.io/foobar#foobar"}}

        if url == "http://barfoo.io/foobar":
            return {"foobar": "barfoo.io/foobar", "bar": {"$ref": "./bar#foobar"}}

        if url == "http://barfoo.io/bar":
            return {"foobar": "barfoo.io/bar", "bar": {"$ref": "https://bar.foo/foobar"}}

        if url == "https://bar.foo/foobar":
            return {"foobar": "bar.foo/foobar", "bar": {"$ref": "//foo.bar/foobar"}}

        if url == "https://foo.bar/foobar":
            return {"foobar": "foo.bar/foobar", "bar": {"$ref": "http://foobar.io/foo/bar/foobar"}}  # Loop to first uri

        raise ValueError(f"Unexpected url {url}")

    mocker.patch("openapi_python_client.resolver.schema_resolver.DataLoader.load", _datalaod_mocked_result)

    resolver = SchemaResolver(url)
    resolver._resolve_schema_references(url_parent, schema, external_schemas, errors, True)

    assert len(errors) == 0
    assert "http://foobar.io/foo/bar/bar" in external_schemas
    assert "http://foobar.io/foo/bar" in external_schemas
    assert "http://barfoo.io/foobar" in external_schemas
    assert "http://barfoo.io/foobar" in external_schemas
    assert "http://barfoo.io/bar" in external_schemas
    assert "https://bar.foo/foobar" in external_schemas
    assert "https://foo.bar/foobar" in external_schemas


def test__resolve_schema_references_mix_path_and_url(mocker):
    read_bytes = mocker.patch("pathlib.Path.read_bytes")
    get = mocker.patch("httpx.get")

    from openapi_python_client.resolver.schema_resolver import SchemaResolver

    path = pathlib.Path("/foo/bar/foobar")
    path_parent = str(path.parent)
    schema = {"foo": {"$ref": "foobar#/foobar"}}
    external_schemas = {}
    errors = []

    def _datalaod_mocked_result(path, data):
        if path == "/foo/bar/foobar":
            return {"foobar": "bar", "bar": {"$ref": "bar#/foobar"}, "local": {"$ref": "#/toto"}}

        if path == "/foo/bar/bar":
            return {"foobar": "bar", "bar": {"$ref": "../bar#/foobar"}}

        if path == "/foo/bar":
            return {"foobar": "bar/bar", "bar": {"$ref": "//barfoo.io/foobar#foobar"}}

        if path == "http://barfoo.io/foobar":
            return {"foobar": "barfoo.io/foobar", "bar": {"$ref": "./bar#foobar"}}

        if path == "http://barfoo.io/bar":
            return {"foobar": "barfoo.io/bar", "bar": {"$ref": "https://bar.foo/foobar"}}

        if path == "https://bar.foo/foobar":
            return {"foobar": "bar.foo/foobar", "bar": {"$ref": "//foo.bar/foobar"}}

        if path == "https://foo.bar/foobar":
            return {"foobar": "foo.bar/foobar"}

        raise ValueError(f"Unexpected path {path}")

    mocker.patch("openapi_python_client.resolver.schema_resolver.DataLoader.load", _datalaod_mocked_result)
    resolver = SchemaResolver(path)
    resolver._resolve_schema_references(path_parent, schema, external_schemas, errors, True)

    assert len(errors) == 0
    assert "/foo/bar/foobar" in external_schemas
    assert "/foo/bar/bar" in external_schemas
    assert "/foo/bar" in external_schemas
    assert "http://barfoo.io/foobar" in external_schemas
    assert "http://barfoo.io/bar" in external_schemas
    assert "https://bar.foo/foobar" in external_schemas
    assert "https://foo.bar/foobar" in external_schemas


def test__resolve_schema_references_with_error(mocker):
    get = mocker.patch("httpx.get")

    import httpcore

    from openapi_python_client.resolver.schema_resolver import SchemaResolver

    url = "http://foobar.io/foo/bar/foobar"
    url_parent = "http://foobar.io/foo/bar/"
    schema = {"foo": {"$ref": "foobar#/foobar"}}
    external_schemas = {}
    errors = []

    def _datalaod_mocked_result(url, data):
        if url == "http://foobar.io/foo/bar/foobar":
            return {
                "foobar": "bar",
                "bar": {"$ref": "bar#/foobar"},
                "barfoor": {"$ref": "barfoo#foobar"},
                "local": {"$ref": "#/toto"},
            }

        if url == "http://foobar.io/foo/bar/bar":
            raise httpcore.NetworkError("mocked error")

        if url == "http://foobar.io/foo/bar/barfoo":
            return {"foobar": "foo/bar/barfoo", "bar": {"$ref": "//barfoo.io/foobar#foobar"}}

        if url == "http://barfoo.io/foobar":
            return {"foobar": "foobar"}

    mocker.patch("openapi_python_client.resolver.schema_resolver.DataLoader.load", _datalaod_mocked_result)
    resolver = SchemaResolver(url)
    resolver._resolve_schema_references(url_parent, schema, external_schemas, errors, True)

    assert len(errors) == 1
    assert errors[0] == "Failed to gather external reference data of bar#/foobar from http://foobar.io/foo/bar/bar"
    assert "http://foobar.io/foo/bar/bar" not in external_schemas
    assert "http://foobar.io/foo/bar/foobar" in external_schemas
    assert "http://foobar.io/foo/bar/barfoo" in external_schemas
    assert "http://barfoo.io/foobar" in external_schemas


def test___lookup_schema_references():
    from openapi_python_client.resolver.schema_resolver import SchemaResolver

    data_set = {
        "foo": {"$ref": "#/ref_1"},
        "bar": {"foobar": {"$ref": "#/ref_2"}},
        "foobar": [{"foo": {"$ref": "#/ref_3"}}, {"bar": [{"foobar": {"$ref": "#/ref_4"}}]}],
    }

    resolver = SchemaResolver("http://foobar.io")
    expected_references = sorted([f"#/ref_{x}" for x in range(1, 5)])
    references = sorted([x.value for x in resolver._lookup_schema_references(data_set)])

    for idx, ref in enumerate(references):
        assert expected_references[idx] == ref
