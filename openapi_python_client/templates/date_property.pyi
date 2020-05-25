{% macro template(property, source) %}
{% if property.required %}
{{ property.name }} = date.fromisoformat({{ source }})
{% else %}
{{ property.name }} = None
if {{ source }} is not None:
    {{ property.name }} = date.fromisoformat(cast(str, {{ source }}))
{% endif %}
{% endmacro %}
