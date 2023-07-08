from typing import List, Set

import questionary

# from .parser.endpoint_collection import Endpoints, Endpoint
from parser.endpoints import Endpoint, EndpointCollection


def questionary_endpoint_selection(endpoints: EndpointCollection) -> Set[str]:
    """Endpoint selection with questionary. Returns a Set of endpoint names"""
    choices: List[questionary.Choice] = []
    prev_table_name = ""
    for endpoint in endpoints.all_endpoints_to_render:
        if prev_table_name != endpoint.table_name:
            choices.append(questionary.Separator(f"\n{endpoint.table_name} endpoints:\n"))
        prev_table_name = endpoint.table_name
        # for tag, collection in endpoints.endpoints_by_tag.items():
        #     if not collection.endpoints_to_render:
        #         continue
        #     choices.append(questionary.Separator(f"\n{tag} endpoints:\n"))
        # for endpoint in collection.endpoints_to_render:
        # text = [("bold", str(endpoint.python_name))]  # , ("italic fg:ansigray", f" {endpoint.path}")]
        text = [
            ("bold", str(endpoint.python_name)),
            ("italic", f" {endpoint.path}"),
        ]
        choices.append(questionary.Choice(text, endpoint))
    selected_endpoints: List[Endpoint] = questionary.checkbox(
        "Which resources would you like to generate?", choices
    ).ask()

    selected_names = set()
    for ep in selected_endpoints:
        selected_names.add(ep.name)
        if ep.transformer and ep.parent:
            # TODO: Generalize traversing ancestry chain
            selected_names.add(ep.parent.name)
    return selected_names
