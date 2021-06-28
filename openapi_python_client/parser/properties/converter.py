""" Utils for converting default values into valid Python """
__all__ = ["convert", "convert_chain"]

from typing import Any, Callable, Dict, Iterable, Optional, TypeVar

from dateutil.parser import isoparse

from ... import utils
from ..errors import ValidationError

T = TypeVar("T")


def convert(type_string: str, value: Any) -> Optional[Any]:
    """
    Used by properties to convert some value into a valid value for the type_string.

    Args:
        type_string: The string of the actual type that this default will be in the generated client.
        value: The default value to try to convert.

    Returns:
        The converted value if conversion was successful, or None of the value was None.

    Raises:
        ValidationError if value could not be converted for type_string.
    """
    if value is None:
        return None
    if type_string not in _CONVERTERS:
        raise ValidationError()
    try:
        return _CONVERTERS[type_string](value)
    except (KeyError, ValueError, AttributeError) as e:
        raise ValidationError from e


def convert_chain(type_strings: Iterable[str], value: Any) -> Optional[Any]:
    """
    Used by properties which support multiple possible converters (Unions).

    Args:
        type_strings: Iterable of all the supported type_strings.
        value: The default value to try to convert.

    Returns:
        The converted value if conversion was successful, or None of the value was None.

    Raises:
        ValidationError if value could not be converted for type_string.
    """
    for type_string in type_strings:
        try:
            val = convert(type_string, value)
            return val
        except ValidationError:
            continue
    raise ValidationError()


def _convert_string(value: Any) -> Optional[str]:
    if isinstance(value, str):
        value = utils.remove_string_escapes(value)
    return repr(value)


def _convert_datetime(value: str) -> Optional[str]:
    isoparse(value)  # Make sure it works
    return f"isoparse({value!r})"


def _convert_date(value: str) -> Optional[str]:
    isoparse(value).date()
    return f"isoparse({value!r}).date()"


_CONVERTERS: Dict[str, Callable[[Any], Optional[Any]]] = {
    "str": _convert_string,
    "datetime.datetime": _convert_datetime,
    "datetime.date": _convert_date,
    "float": float,
    "int": int,
    "bool": bool,
}
