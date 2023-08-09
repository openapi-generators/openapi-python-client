"""JSONPath helpers."""

from __future__ import annotations

import typing as t
from functools import lru_cache

from jsonpath_ng.ext import parse

if t.TYPE_CHECKING:
    import jsonpath_ng


def extract_jsonpath(
    expression: str,
    input: dict | list,  # noqa: A002
) -> t.Generator[t.Any, None, None]:
    """Extract records from an input based on a JSONPath expression.

    Args:
        expression: JSONPath expression to match against the input.
        input: JSON object or array to extract records from.

    Yields:
        Records matched with JSONPath expression.
    """
    compiled_jsonpath = _compile_jsonpath(expression)

    match: jsonpath_ng.DatumInContext
    for match in compiled_jsonpath.find(input):
        yield match.value


@lru_cache(maxsize=128)
def _compile_jsonpath(expression: str) -> jsonpath_ng.JSONPath:
    """Parse a JSONPath expression and cache the result.

    Args:
        expression: A string representing a JSONPath expression.

    Returns:
        A compiled JSONPath object.
    """
    return parse(expression)
