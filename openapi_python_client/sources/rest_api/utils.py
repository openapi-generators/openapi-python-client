from functools import reduce
from operator import getitem
from typing import Any, Dict, Mapping, Sequence, Union


def join_url(base_url: str, path: str) -> str:
    if not base_url.endswith("/"):
        base_url += "/"
    return base_url + path.lstrip("/")


def create_nested_accessor(path: Union[str, Sequence[str]]) -> Any:
    if isinstance(path, (list, tuple)):
        return lambda d: reduce(getitem, path, d)
    return lambda d: d.get(path)
