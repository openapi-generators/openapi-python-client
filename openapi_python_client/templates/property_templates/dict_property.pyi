{% macro construct(property, source, initial_value="None") %}
{% if property.required %}
{{ property.python_name }} = {{ source }}
{% else %}
{{ property.python_name }} = {{ initial_value }}
if {{ source }} is not None:
    {{ property.python_name }} = {{ source }}
{% endif %}
{% endmacro %}

{% macro transform(property, source, destination, declare_type=True) %}
{% if property.nullable %}
{{ destination }} = {{ source }} if {{ source }} else None
{% else %}
{{ destination }} = {{ source }}
{% endif %}
{% endmacro %}
