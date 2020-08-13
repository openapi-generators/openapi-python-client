from dataclasses import asdict
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ..client import AuthenticatedClient, Client
from ..errors import ApiResponseError

{% for relative in collection.relative_imports %}
{{ relative }}
{% endfor %}
{% for endpoint in collection.endpoints %}

{% from "endpoint_macros.pyi" import header_params, query_params, json_body, return_type %}

async def {{ endpoint.name | snakecase }}(
    *,
    {# Proper client based on whether or not the endpoint requires authentication #}
    {% if endpoint.requires_security %}
    client: AuthenticatedClient,
    {% else %}
    client: Client,
    {% endif %}
    {# path parameters #}
    {% for parameter in endpoint.path_parameters %}
    {{ parameter.to_string() }},
    {% endfor %}
    {# Form data if any #}
    {% if endpoint.form_body_reference %}
    form_data: {{ endpoint.form_body_reference.class_name }},
    {% endif %}
    {# Multipart data if any #}
    {% if endpoint.multipart_body_reference %}
    multipart_data: {{ endpoint.multipart_body_reference.class_name }},
    {% endif %}
    {# JSON body if any #}
    {% if endpoint.json_body %}
    json_body: {{ endpoint.json_body.get_type_string() }},
    {% endif %}
    {# query parameters #}
    {% for parameter in endpoint.query_parameters %}
    {{ parameter.to_string() }},
    {% endfor %}
    {% for parameter in endpoint.header_parameters %}
    {{ parameter.to_string() }},
    {% endfor %}
{{ return_type(endpoint) }}
    """ {{ endpoint.description }} """
    url = "{}{{ endpoint.path }}".format(
        client.base_url,
        {% for parameter in endpoint.path_parameters %}
        {{parameter.name}}={{parameter.python_name}},
        {% endfor %}
    )

    headers: Dict[str, Any] = client.get_headers()
    {{ header_params(endpoint) | indent(4) }}

    {{ query_params(endpoint) | indent(4) }}
    {{ json_body(endpoint) | indent(4) }}

    async with httpx.AsyncClient() as _client:
        response = await _client.{{ endpoint.method }}(
            url=url,
            headers=headers,
            {% if endpoint.form_body_reference %}
            data=asdict(form_data),
            {% endif %}
            {% if endpoint.multipart_body_reference %}
            files=multipart_data.to_dict(),
            {% endif %}
            {% if endpoint.json_body %}
            json={{ "json_" + endpoint.json_body.python_name }},
            {% endif %}
            {% if endpoint.query_parameters %}
            params=params,
            {% endif %}
        )

    {% for response in endpoint.responses %}
    if response.status_code == {{ response.status_code }}:
        return {{ response.constructor() }}
    {% endfor %}
    else:
        raise ApiResponseError(response=response)
{% endfor %}
