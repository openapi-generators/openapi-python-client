{% macro construct(property, source) %}
{# Receiving files not supported (yet) #}
{{ property.python_name }} = {{ source }}
{% endmacro %}

{% macro transform(property, source, destination) %}
{% if property.required %}
{{ destination }} = {{ source }}.to_tuple()
{% else %}
{{ destination }} = {{ source }}.to_tuple() if {{ source }} else None
{% endif %}
{% endmacro %}
