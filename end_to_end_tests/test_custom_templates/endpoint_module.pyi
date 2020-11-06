from typing import Optional

import httpx

Client = httpx.Client

{% for relative in endpoint.relative_imports %}
{{ relative }}
{% endfor %}

{% from "endpoint_macros.pyi" import header_params, query_params, json_body, return_type, arguments, client, kwargs, parse_response %}

{% set return_string = return_type(endpoint) %}
{% set parsed_responses = (endpoint.responses | length > 0) and return_string != "None" %}


{% if parsed_responses %}
def _parse_response(*, response: httpx.Response) -> Optional[{{ return_string }}]:
    {% for response in endpoint.responses %}
    if response.status_code == {{ response.status_code }}:
        return {{ response.constructor() }}
    {% endfor %}
    return None
{% endif %}



def _build_response(*, response: httpx.Response) -> httpx.Response[{{ return_string }}]:
    return httpx.Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        {% if parsed_responses %}
        parsed=_parse_response(response=response),
        {% else %}
        parsed=None,
        {% endif %}
    )


def httpx_request({{ arguments(endpoint) | indent(4) }}) -> httpx.Response[{{ return_string }}]:
    {{ header_params(endpoint) | indent(4) }}
    {{ query_params(endpoint) | indent(4) }}
    {{ json_body(endpoint) | indent(4) }}

    response = client.request(
        "{{ endpoint.method }}",
        "{{ endpoint.path }}",
        {% if endpoint.json_body %}
        json={{ "json_" + endpoint.json_body.python_name }},
        {% endif %}
        {% if endpoint.query_parameters %}
        params=params,
        {% endif %}
        {% if endpoint.form_body_reference %}
        "data": asdict(form_data),
        {% endif %}
        {% if endpoint.multipart_body_reference %}
        "files": multipart_data.to_dict(),
        {% endif %}
    )

    return _build_response(response=response)