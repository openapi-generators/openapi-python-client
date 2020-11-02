{% macro construct(property, source) %}
{% if property.required %}
{{ property.python_name }} = {{ property.reference.class_name }}({{ source }})
{% else %}
{{ property.python_name }} = None
if {{ source }} is not None:
    {{ property.python_name }} = {{ property.reference.class_name }}({{ source }})
{% endif %}
{% endmacro %}

{% macro transform(property, source, destination) %}
{% if property.required %}
{% if property.nullable %}
{{ destination }} = {{ source }}.value if {{ source }} else None
{% else %}
{{ destination }} = {{ source }}.value
{% endif %}
{% else %}
if {{ source }} is UNSET:
    {{ destination }} = UNSET
{% if property.nullable %}
else:
    {{ destination }} = {{ source }}.value if {{ source }} else None
{% else %}
else:
    {{ destination }} = {{ source }}.value
{% endif %}
{% endif %}
{% endmacro %}
