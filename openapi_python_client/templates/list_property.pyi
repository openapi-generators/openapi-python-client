{% macro template(property, source) %}
{% set inner_property = property.inner_property %}
{% if inner_property.constructor_template %}
{% set inner_source = inner_property.python_name + "_data" %}
{{ property.python_name }} = []
{% if property.required %}
for {{ inner_source }} in ({{ source }}):
{% else %}
for {{ inner_source }} in ({{ source }} or []):
{% endif %}
    {% from inner_property.constructor_template import template %}
    {{ template(inner_property, inner_source) | indent(4) }}
    {{ property.python_name }}.append({{ inner_property.python_name }})
{% else %}
{{ property.python_name }} = {{ source }}
{% endif %}
{% endmacro %}
