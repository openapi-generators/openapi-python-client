from dataclasses import asdict

import requests

from ..client import AuthenticatedClient, Client
{% for relative in collection.relative_imports %}
{{ relative }}
{% endfor %}
{% for endpoint in collection.endpoints %}


def {{ endpoint.name }}(
    *,
    {% if endpoint.requires_security %}
    client: AuthenticatedClient,
    {% else %}
    client: Client,
    {% endif %}
    {% if endpoint.form_body_reference %}
    form_data: {{ endpoint.form_body_reference.class_name }},
    {% endif %}
):
    """ {{ endpoint.description }} """
    url = client.base_url + "{{ endpoint.path }}"

    {% if endpoint.method == "get" %}
    return requests.get(url=url, headers=client.get_headers())
    {% elif endpoint.method == "post" %}
    return requests.post(
        url=url,
        headers=client.get_headers(),
        {% if endpoint.form_body_reference %}
        data=asdict(form_data),
        {% endif %}
    )
    {% elif endpoint.method == "patch" %}
    return requests.patch(
        url=url,
        headers=client.get_headers()
        {% if endpoint.form_body_reference %}
        data=asdict(form_data),
        {% endif %}
    )
    {% elif endpoint.method == "put" %}
    return requests.put(
        url=url,
        headers=client.get_headers()
        {% if endpoint.form_body_reference %}
        data=asdict(form_data),
        {% endif %}
    )
    {% endif %}
{% endfor %}
