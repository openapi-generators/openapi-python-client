{% macro construct(property, source) %}
{% if property.required %}
{{ property.python_name }} = {{ source }}
{% else %}
{{ property.python_name }} = None
if {{ source }} is not None:
    {{ property.python_name }} = {{ source }}
{% endif %}
{% endmacro %}

{% macro transform(property, source, destination) %}
{% if property.nullable %}
{{ destination }} = {{ source }} if {{ source }} else None
{% else %}
{{ destination }} = {{ source }}
{% endif %}
{% endmacro %}
