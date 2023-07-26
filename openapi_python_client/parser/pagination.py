import re

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from openapi_python_client.parser.endpoints import Endpoint, Parameter

RE_OFFSET_PARAM = re.compile(r"(?i)(page|start|offset)")
RE_CURSOR_PARAM = re.compile(r"(?i)(cursor|after|since)")

OFFSET_PARAM_KEYWORDS = {"offset", "page", "start"}


@dataclass
class Pagination:
    @classmethod
    def from_endpoint(cls, endpoint: "Endpoint") -> None:
        resp = endpoint.data_response
        if not resp or not resp.content_schema:
            raise ValueError(f"Endpoint {endpoint.path} does not have a content response")

        crawler = resp.content_schema.crawled_properties
        offset_param: Optional["Parameter"] = None
        cursor_param: Optional["Parameter"] = None
        for name, param in endpoint.parameters.items():
            if not offset_param and "integer" in param.schema.types and RE_OFFSET_PARAM.search(name):
                offset_param = param
            if not cursor_param and "string" in param.schema.types and RE_CURSOR_PARAM.search(name):
                cursor_param = param

        parameter_names = set(endpoint.parameters.keys())
        property_paths = [".".join(k) for k in crawler.all_properties.keys()]

        prompt_params = []
        for param in endpoint.parameters.values():
            prompt_params.append(
                dict(
                    name=param.name,
                    location=param.location,
                    description=param.description,
                    types=param.schema.types,
                )
            )

        prompt_props = []
        for path, prop in crawler.all_properties.items():
            prompt_props.append(
                dict(
                    json_path=".".join(path),
                    description=prop.description,
                    types=prop.types,
                )
            )

        import json

        print(json.dumps(prompt_params, indent=2))
        print(json.dumps(prompt_props, indent=2))

        # if offset_param:
        #     print("OFFSET PARAM", offset_param.name, offset_param.description)
        # if cursor_param:
        #     if cursor_param.name == "cursor":
        #         breakpoint()
        #     print("CURSOR PARAM", cursor_param.name, cursor_param.description)
