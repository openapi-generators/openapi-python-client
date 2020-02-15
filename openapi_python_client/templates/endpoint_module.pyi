import requests

from ..client import Client

{% for endpoint in endpoints %}
def {{ endpoint.name }}(client: Client):
    """ {{ endpoint.description }} """
    url = client.base_url + "{{ endpoint.path }}"

    {% if endpoint.method == "get" %}
    return requests.get(url)
    {% endif %}


{% endfor %}


