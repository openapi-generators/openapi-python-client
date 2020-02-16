from dataclasses import asdict

import requests

from ..client import Client
{% for relative in collection.relative_imports %}
{{ relative }}
{% endfor %}

{% for endpoint in collection.endpoints %}
def {{ endpoint.name }}(
    *,
    client: Client,
    {% if endpoint.form_body_reference %}
    form_data: {{ endpoint.form_body_reference.class_name }},
    {% endif %}
):
    """ {{ endpoint.description }} """
    url = client.base_url + "{{ endpoint.path }}"

    {% if endpoint.method == "get" %}
    return requests.get(url=url)
    {% elif endpoint.method == "post" %}
    return requests.post(
        url=url,
        {% if endpoint.form_body_reference %}
        data=asdict(form_data),
        {% endif %}
    )
    {% elif endpoint.method == "patch" %}
    return requests.patch(
        url=url,
        {% if endpoint.form_body_reference %}
        data=asdict(form_data),
        {% endif %}
    )
    {% elif endpoint.method == "put" %}
    return requests.put(
        url=url,
        {% if endpoint.form_body_reference %}
        data=asdict(form_data),
        {% endif %}
    )
    {% endif %}


{% endfor %}


