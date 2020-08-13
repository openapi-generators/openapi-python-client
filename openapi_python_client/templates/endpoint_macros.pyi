{% macro header_params(endpoint) %}
{% if endpoint.header_parameters %}
    {% for parameter in endpoint.header_parameters %}
        {% if parameter.required %}
headers["{{ parameter.python_name | kebabcase}}"] = {{ parameter.python_name }}
        {% else %}
if {{ parameter.python_name }} is not None:
    headers["{{ parameter.python_name | kebabcase}}"] = {{ parameter.python_name }}
        {% endif %}
    {% endfor %}
{% endif %}
{% endmacro %}

{% macro query_params(endpoint) %}
{% if endpoint.query_parameters %}
    {% for property in endpoint.query_parameters %}
        {% set destination = "json_" + property.python_name %}
        {% if property.template %}
            {% from "property_templates/" + property.template import transform %}
{{ transform(property, property.python_name, destination) }}
        {% endif %}
    {% endfor %}
params: Dict[str, Any] = {
    {% for property in endpoint.query_parameters %}
        {% if property.required %}
            {% if property.template %}
    "{{ property.name }}": {{ "json_" + property.python_name }},
            {% else %}
    "{{ property.name }}": {{ property.python_name }},
            {% endif %}
        {% endif %}
    {% endfor %}
}
    {% for property in endpoint.query_parameters %}
        {% if not property.required %}
if {{ property.python_name }} is not None:
            {% if property.template %}
    params["{{ property.name }}"] = {{ "json_" + property.python_name }}
            {% else %}
    params["{{ property.name }}"] = {{ property.python_name }}
            {% endif %}
        {% endif %}
    {% endfor %}
{% endif %}
{% endmacro %}

{% macro json_body(endpoint) %}
{% if endpoint.json_body %}
    {% set property = endpoint.json_body %}
    {% set destination = "json_" + property.python_name %}
    {% if property.template %}
        {% from "property_templates/" + property.template import transform %}
{{ transform(property, property.python_name, destination) }}
    {% endif %}
{% endif %}
{% endmacro %}

{% macro return_type(endpoint) %}
{% if endpoint.responses | length == 1 %}
) -> {{ endpoint.responses[0].return_string() }}:
{% else %}
) -> Union[
    {% for response in endpoint.responses %}
    {{ response.return_string() }},
    {% endfor %}
]:
{% endif %}
{% endmacro %}
