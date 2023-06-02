import re
from typing import Any, Iterator, Optional
from urllib import parse

from dlt.common.jsonpath import TJsonPath, find_values
from dlt.common.typing import TDataItems


def extract_nested_data(response_data: Any, path: Optional[TJsonPath] = None) -> Iterator[Any]:
    """Extract nested response data from json path"""
    if not path:
        yield response_data
    else:
        for result in find_values(path, response_data):
            yield result


def extract_url_like_values(data: dict) -> Iterator[str]:
    url_pattern = r"(https?://[^\s/$.?#].[^\s]*)"  # Regex pattern to match URLs

    for key, value in data.items():
        if isinstance(value, dict):
            yield from extract_url_like_values(value)
        elif isinstance(value, str) and re.match(url_pattern, value):
            yield value


def extract_iterate_parent(
    data: TDataItems, property_name: str, path_param_name: str, endpoint_url: str
) -> Iterator[Any]:
    """Extract kwargs to use in transformer requests"""
    if not isinstance(data, list):
        data = [data]
    for item in data:
        property_value = item.get(property_name)
        if property_value is not None:
            yield {path_param_name: property_value}
            continue

        # Try looking for a URL property which matches the endpoint URL we're dealing with
        urls = extract_url_like_values(item)
        for url in urls:
            property_value = pluck_param_from_result_url(url, endpoint_url)
            if not property_value:
                continue
            else:
                break

        if property_value is not None:
            yield {path_param_name: property_value}
        else:
            raise ValueError(f"Could not find id parameter {path_param_name} (endpoint {endpoint_url}) in: {item}")


def pluck_param_from_result_url(result_url: str, endpoint_url: str):
    endpoint_url = endpoint_url.rstrip("/")
    rel_url = parse.urlparse(result_url).path.rstrip("/")
    rel_parts = rel_url.split("/")
    endpoint_parts = endpoint_url.split("/")

    if len(rel_parts) != len(endpoint_parts):
        return None

    prop_found = None
    for re_part, e_part in zip(rel_parts, endpoint_parts):
        if e_part.startswith("{"):
            prop_found = re_part
        else:
            if re_part != e_part:
                return None
    return prop_found
