import urllib

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
