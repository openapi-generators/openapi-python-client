{% macro construct(property, source) %}
{# Receiving files not supported (yet) #}
{{ property.python_name }} = {{ source }}
{% endmacro %}

{% macro transform(property, source, destination) %}
{% if property.required %}
{% if property.nullable %}
{{ destination }} = {{ source }}.to_tuple() if {{ source }} else None
{% else %}
{{ destination }} = {{ source }}.to_tuple()
{% endif %}
{% else %}
if {{ source }} is UNSET:
    {{ destination }} = UNSET
{% if property.nullable %}
else:
    {{ destination }} = {{ source }}.to_tuple() if {{ source }} else None
{% else %}
else:
    {{ destination }} = {{ source }}.to_tuple()
{% endif %}
{% endif %}
{% endmacro %}
