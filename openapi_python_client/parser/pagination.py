import re

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from openapi_python_client.parser.endpoints import Endpoint, Parameter
    from openapi_python_client.parser.context import OpenapiContext

RE_OFFSET_PARAM = re.compile(r"(?i)(page|start|offset)")
RE_CURSOR_PARAM = re.compile(r"(?i)(cursor|after|since)")

OFFSET_PARAM_KEYWORDS = {"offset", "page", "start"}


@dataclass
class Pagination:
    @classmethod
    def from_endpoint(cls, endpoint: "Endpoint", context: "OpenapiContext") -> "Pagination":
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

        prompt_props_str = ""
        for prop in prompt_props:
            prompt_props_str += f"""
            * JSON PATH: {prop['json_path']}
            DESCRIPTION: {prop['description']}
            TYPES: {prop['types']}
            """

        prompt = f"""
        The following properties are included in a JSON response of the
        endpoint {endpoint.path}. This is a flattened representation of the
        properties, in reality the properties are nested in a JSON object
        according to their `json_path` where dot represents a nested object
        and `[*]` represents an array.

        Use the property names, their types and their location within the json
        object to determine which properties are used for pagination.

        If the endpoint does not use pagination then return None.

        Here is the description of the endpoint from the OpenAPI schema:

        {endpoint.description}

        Here are the response properties:

        {prompt_props_str}
        """

        ai_result = context.openai.prompt(
            [
                {
                    "role": "system",
                    "content": """You are an expert data engineer working on dlt pipeline generator from API documentations.
                You are tasked with identifying the properties used for pagination in an API response.
                Always respond with JSON and put the results under the key \"paginator\"!
                """,
                },
                {"role": "user", "content": prompt},
            ]
        )

        # import json

        # print(json.dumps(prompt_params, indent=2))
        # print(json.dumps(prompt_props, indent=2))

        # if offset_param:
        #     print("OFFSET PARAM", offset_param.name, offset_param.description)
        # if cursor_param:
        #     if cursor_param.name == "cursor":
        #         breakpoint()
        #     print("CURSOR PARAM", cursor_param.name, cursor_param.description)
