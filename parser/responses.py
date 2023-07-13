from __future__ import annotations
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from parser.endpoints import EndpointCollection, Endpoint, Response

from parser.models import DataPropertyPath
from openapi_python_client.utils import count_by_length


def process_responses(endpoint_collection: "EndpointCollection") -> None:
    """Process all responses in schemas"""
    all_endpoints = endpoint_collection.all_endpoints_to_render
    table_ranks: Dict[str, int] = {}
    for endpoint in all_endpoints:
        _process_response_list(endpoint.data_response, endpoint, endpoint_collection)
        response = endpoint.data_response
        unique_models = set(t.name for t in response.content_schema.crawled_properties.object_properties.values())
        table_ranks[endpoint.table_name] = max(table_ranks.get(endpoint.table_name, 0), len(unique_models))
    for endpoint in all_endpoints:
        endpoint.rank = table_ranks[endpoint.table_name]


def _process_response_list(
    response: Response,
    endpoint: Endpoint,
    endpoints: EndpointCollection,
) -> None:
    if not response.list_properties:
        return
    if () in response.list_properties:  # Response is a top level list
        response.list_property = DataPropertyPath((), response.list_properties[()])
        return

    level_counts = count_by_length(response.list_properties.keys())

    # Get list properties max 2 levels down
    props_first_levels = [
        (path, prop) for path, prop in sorted(response.list_properties.items(), key=lambda k: len(k)) if len(path) <= 2
    ]

    # If there is only one list property 1 or 2 levels down, this is the list
    for path, prop in props_first_levels:
        levels = len(path)
        if level_counts[levels] == 1:
            response.list_property = DataPropertyPath(path, prop)
    parent = endpoints.find_immediate_parent(endpoint.path)
    if parent and not parent.required_parameters:
        response.list_property = None
