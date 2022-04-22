{% macro header_params(endpoint) %}
{% if endpoint.header_parameters %}
    {% for parameter in endpoint.header_parameters %}
        {% if parameter.required %}
headers["{{ parameter.python_name | kebabcase}}"] = {{ parameter.python_name }}
        {% else %}
if {{ parameter.python_name }} is not UNSET:
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
{{ transform(property, property.python_name, destination, query_parameter=True) }}
        {% endif %}
    {% endfor %}
params: Dict[str, Any] = {
    {% for property in endpoint.query_parameters %}
        {% if property.required and not property.nullable %}
            {% if property.template %}
    "{{ property.name }}": {{ "json_" + property.python_name }},
            {% else %}
    "{{ property.name }}": {{ property.python_name }},
            {% endif %}
        {% endif %}
    {% endfor %}
}
    {% for property in endpoint.query_parameters %}
        {% if not property.required or property.nullable %}
            {% set property_name = "json_" + property.python_name if property.template else property.python_name %}
if {% if not property.required %}not isinstance({{ property_name }}, Unset) and {% endif %}{{ property_name }} is not None:
            {% if property.json_is_dict %}
    params.update({{ property_name }})
            {% else %}
    params["{{ property.name }}"] = {{ property_name }}
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

{% macro yaml_body(endpoint) %}
{% if endpoint.yaml_body %}
    {% set property = endpoint.yaml_body %}
    {% set destination = "yaml_" + property.python_name %}
    {% if property.template %}
        {% from "property_templates/" + property.template import transform %}
{{ transform(property, property.python_name, destination) }}
    {% endif %}
{% endif %}
{% endmacro %}

{% macro return_type(endpoint) %}
{% if endpoint.responses | length == 0 %}
None
{%- elif endpoint.responses | length == 1 %}
{{ endpoint.responses[0].prop.get_type_string() }}
{%- else %}
Union[
    {% for response in endpoint.responses %}
    {{ response.prop.get_type_string() }}{{ "," if not loop.last }}
    {% endfor %}
]
{%- endif %}
{% endmacro %}

{# The all the kwargs passed into an endpoint (and variants thereof)) #}
{% macro arguments(endpoint) %}
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
{# Yaml body if any #}
{% if endpoint.yaml_body %}
yaml_body: {{ endpoint.yaml_body.get_type_string() }},
{% endif %}
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
{{ parameter.to_string(query_parameter=True) }},
{% endfor %}
{% for parameter in endpoint.header_parameters %}
{{ parameter.to_string() }},
{% endfor %}
{% endmacro %}

{# Just lists all kwargs to endpoints as name=name for passing to other functions #}
{% macro kwargs(endpoint) %}
client=client,
{% for parameter in endpoint.path_parameters %}
{{ parameter.python_name }}={{ parameter.python_name }},
{% endfor %}
{% if endpoint.yaml_body %}
yaml_body=yaml_body,
{% endif %}
{% if endpoint.form_body_reference %}
form_data=form_data,
{% endif %}
{% if endpoint.multipart_body_reference %}
multipart_data=multipart_data,
{% endif %}
{% if endpoint.json_body %}
json_body=json_body,
{% endif %}
{% for parameter in endpoint.query_parameters %}
{{ parameter.python_name }}={{ parameter.python_name }},
{% endfor %}
{% for parameter in endpoint.header_parameters %}
{{ parameter.python_name }}={{ parameter.python_name }},
{% endfor %}
{% endmacro %}
