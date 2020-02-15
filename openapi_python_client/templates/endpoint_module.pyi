import requests

from ..client import Client


{% for endpoint in endpoints %}
def {{ endpoint.name }}(client: Client):
    """ {{ endpoint.description }} """
    url = client.base_url + "{{ endpoint.path }}"

    {% if endpoint.method == "get" %}
    return requests.get(url=url)
    {% elif endpoint.method == "post" %}
    return requests.post(url=url)
    {% elif endpoint.method == "patch" %}
    return requests.patch(url=url)
    {% elif endpoint.method == "put" %}
    return requests.put(url=url)
    {% endif %}


{% endfor %}


