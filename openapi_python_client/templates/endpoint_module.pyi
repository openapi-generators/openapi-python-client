from dataclasses import asdict
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response

{% for relative in endpoint.relative_imports %}
{{ relative }}
{% endfor %}

{% from "endpoint_macros.pyi" import header_params, query_params, json_body, return_type, arguments, client, kwargs, parse_response %}

def _get_kwargs(
    {{ arguments(endpoint) | indent(4) }}
) -> Dict[str, Any]:
    url = "{}{{ endpoint.path }}".format(
        client.base_url
        {%- for parameter in endpoint.path_parameters -%}
        ,{{parameter.name}}={{parameter.python_name}}
        {%- endfor -%}
    )

    headers: Dict[str, Any] = client.get_headers()

    {{ header_params(endpoint) | indent(4) }}

    {{ query_params(endpoint) | indent(4) }}

    {{ json_body(endpoint) | indent(4) }}

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        {% if endpoint.form_body_reference %}
        "data": asdict(form_data),
        {% endif %}
        {% if endpoint.multipart_body_reference %}
        "files": multipart_data.to_dict(),
        {% endif %}
        {% if endpoint.json_body %}
        "json": {{ "json_" + endpoint.json_body.python_name }},
        {% endif %}
        {% if endpoint.query_parameters %}
        "params": params,
        {% endif %}
    }


def _parse_response(*, response: httpx.Response) -> Optional[{{ return_type(endpoint) }}]:
    {% for response in endpoint.responses %}
    if response.status_code == {{ response.status_code }}:
        return {{ response.constructor() }}
    {% endfor %}
    return None


def _build_response(*, response: httpx.Response) -> Response[{{ return_type(endpoint) }}]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    {{ arguments(endpoint) | indent(4) }}
) -> Response[{{ return_type(endpoint) }}]:
    kwargs = _get_kwargs(
        {{ kwargs(endpoint) }}
    )

    response = httpx.{{ endpoint.method }}(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    {{ arguments(endpoint) | indent(4) }}
) -> Optional[{{ return_type(endpoint) }}]:
    """ {{ endpoint.description }} """

    return sync_detailed(
        {{ kwargs(endpoint) }}
    ).parsed


async def asyncio_detailed(
    {{ arguments(endpoint) | indent(4) }}
) -> Response[{{ return_type(endpoint) }}]:
    kwargs = _get_kwargs(
        {{ kwargs(endpoint) }}
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.{{ endpoint.method }}(
            **kwargs
        )

    return _build_response(response=response)


async def asyncio(
    {{ arguments(endpoint) | indent(4) }}
) -> Optional[{{ return_type(endpoint) }}]:
    """ {{ endpoint.description }} """

    return (await asyncio_detailed(
        {{ kwargs(endpoint) }}
    )).parsed
