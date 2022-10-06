{% macro construct(property, source, initial_value="[]", nested=False) %}
{% set inner_property = property.inner_property %}
{% if inner_property.template %}
{% set inner_source = inner_property.python_name + "_data" %}
{{ property.python_name }} = {{ initial_value }}
_{{ property.python_name }} = {{ source }}
{% if property.required %}
for {{ inner_source }} in (_{{ property.python_name }}):
{% else %}
for {{ inner_source }} in (_{{ property.python_name }} or []):
{% endif %}
    {% from "property_templates/" + inner_property.template import construct %}
    {{ construct(inner_property, inner_source) | indent(4) }}
    {{ property.python_name }}.append({{ inner_property.python_name }})
{% else %}
{{ property.python_name }} = cast({{ property.get_type_string(no_optional=True) }}, {{ source }})
{% endif %}
{% endmacro %}

{% macro check_type_for_construct(source) %}isinstance({{ source }}, list){% endmacro %}

{% macro _transform(property, source, destination) %}
{% set inner_property = property.inner_property %}
{% if inner_property.template %}
{% set inner_source = inner_property.python_name + "_data" %}
{{ destination }} = []
for {{ inner_source }} in {{ source }}:
    {% from "property_templates/" + inner_property.template import transform %}
    {{ transform(inner_property, inner_source, inner_property.python_name) | indent(4) }}
    {{ destination }}.append({{ inner_property.python_name }})
{% else %}
{{ destination }} = {{ source }}
{% endif %}
{% endmacro %}


{% macro transform(property, source, destination, declare_type=True, query_parameter=False) %}
{% set inner_property = property.inner_property %}
{% if property.required %}
{% if property.nullable %}
if {{ source }} is None:
    {{ destination }} = None
else:
    {{ _transform(property, source, destination) | indent(4) }}
{% else %}
{{ _transform(property, source, destination) }}
{% endif %}
{% else %}
{{ destination }}{% if declare_type %}: {{ property.get_type_string(query_parameter=query_parameter, json=True) }}{% endif %} = UNSET
if not isinstance({{ source }}, Unset):
{% if property.nullable %}
    if {{ source }} is None:
        {{ destination }} = None
    else:
        {{ _transform(property, source, destination) | indent(8)}}
{% else %}
    {{ _transform(property, source, destination) | indent(4)}}
{% endif %}
{% endif %}


{% endmacro %}
