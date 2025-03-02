import re
from typing import Any, Union

from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties.property import Property


def assert_prop_error(
    p: Union[Property, PropertyError],
    message_regex: str,
    data: Any = None,
) -> None:
    assert isinstance(p, PropertyError)
    assert re.search(message_regex, p.detail)
    if data is not None:
        assert p.data == data
