import pytest

from openapi_python_client.parser.errors import ValidationError
from openapi_python_client.parser.properties.converter import convert, convert_chain


def test_convert_none():
    assert convert("blah", None) is None


def test_convert_bad_type():
    with pytest.raises(ValidationError):
        assert convert("blah", "blah")


def test_convert_exception():
    with pytest.raises(ValidationError):
        assert convert("datetime.datetime", "blah")


def test_convert_str():
    # This looks ugly, but it outputs in jinja as '\\"str\\"'
    # The extra escape of " is not necessary but the code is overly cautious
    assert convert("str", '"str"') == "'\\\\\"str\\\\\"'"


def test_convert_datetime():
    assert convert("datetime.datetime", "2021-01-20") == "isoparse('2021-01-20')"


def test_convert_date():
    assert convert("datetime.date", "2021-01-20") == "isoparse('2021-01-20').date()"


def test_convert_chain_no_valid():
    with pytest.raises(ValidationError):
        convert_chain(("int",), "a")


def test_convert_chain():
    assert convert_chain(("int", "bool"), "a")
