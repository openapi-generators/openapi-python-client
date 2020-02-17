from dataclasses import asdict
from typing import Optional

import requests

from ..client import AuthenticatedClient, Client
{% for relative in collection.relative_imports %}
{{ relative }}
{% endfor %}
{% for endpoint in collection.endpoints %}


def {{ endpoint.name }}(
    *,
    {# Proper client based on whether or not the endpoint requires authentication #}
    {% if endpoint.requires_security %}
    client: AuthenticatedClient,
    {% else %}
    client: Client,
    {% endif %}
    {# Form data if any #}
    {% if endpoint.form_body_reference %}
    form_data: {{ endpoint.form_body_reference.class_name }},
    {% endif %}
    {# query parameters #}
    {% if endpoint.query_parameters %}
    {% for parameter in endpoint.query_parameters %}
    {{ parameter.to_string() }},
    {% endfor %}
    {% endif %}
):
    """ {{ endpoint.description }} """
    url = client.base_url + "{{ endpoint.path }}"

    {% if endpoint.query_parameters %}
    params = {
        {% for parameter in endpoint.query_parameters %}
        "{{ parameter.name }}": {{ parameter.transform() }},
        {% endfor %}
    }
    {% endif %}

    return requests.{{ endpoint.method }}(
        url=url,
        headers=client.get_headers(),
        {% if endpoint.form_body_reference %}
        data=asdict(form_data),
        {% endif %}
        {% if endpoint.query_parameters %}
        params=params,
        {% endif %}
    )
{% endfor %}
