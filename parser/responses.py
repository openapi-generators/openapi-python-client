from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from parser.endpoints import EndpointCollection

from parser.models import traverse_properties


def process_responses(endpoint_collection: "EndpointCollection") -> None:
    """Process all responses in schemas"""
    # First pass identify all list properties
    for endpoint in endpoint_collection.endpoints:
        response = endpoint.data_response
        lists, models = traverse_properties(response.prop)
        response.list_properties.update(lists)
        response.model_properties.update(models)

    class_name_to_endpoints: Dict[str, Set["Endpoint"]] = {}

    for endpoint in endpoints.endpoints_by_name.values():
        for response in endpoint.responses:
            # for endpoint_name, responses in schemas.responses_by_endpoint.items():
            #     for response in responses:
            for prop in response.model_properties.values():
                items = class_name_to_endpoints.setdefault(prop.class_info.name, set())
                items.add(endpoints.endpoints_by_name[endpoint.name])

    all_endpoints = list(endpoints.endpoints_by_name.values())
    for endpoint in all_endpoints:
        resp = endpoint.responses[0]
        _process_response_list(resp, endpoint, endpoints, class_name_to_endpoints)

    # class_name_root_counts: Dict[str, int] = {}
    # for class_name, model in schemas.classes_by_name.items():
    #     for endpoint in all_endpoints:
    #         root_model = endpoint.root_model
    #         if not root_model:
    #             continue
    #         root_class_name = root_model.class_info.name
    #         if class_name != root_class_name:
    #             continue
    #         count = class_name_root_counts.setdefault(class_name, 0)
    #         class_name_root_counts[class_name] = count + 1

    all_root_models: Set[str] = set()
    for endpoint in all_endpoints:
        root_model = endpoint.root_model
        if root_model:
            all_root_models.add(root_model.class_info.name)

    # endpoint_counts = {key: len(value) for key, value in class_name_to_endpoints.items() if key in all_root_models}

    for endpoint in all_endpoints:
        resp = endpoint.responses[0]
        models_referenced = set(m.class_info.name for path, m in resp.model_properties.items())
        root_models = all_root_models.intersection(models_referenced)
        endpoint.rank = len(root_models)

    # ranks = [(endpoint.path, endpoint.rank) for endpoint in all_endpoints]
    # ranks_sorted = sorted(ranks, key=lambda x: x[1])


def _process_response_list(
    response: Response,
    endpoint: "Endpoint",
    endpoints: "Endpoints",
    class_name_to_endpoints: Dict[str, Set["Endpoint"]],
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
    if parent and not parent.has_path_parameters:
        response.list_property = None
