{% macro construct(property, source) %}
{% if property.required %}
{{ property.python_name }} = {{ property.reference.class_name }}.from_dict({{ source }})
{% else %}
{{ property.python_name }} = None
if {{ source }} is not None:
    {{ property.python_name }} = {{ property.reference.class_name }}.from_dict(cast(Dict[str, Any], {{ source }}))
{% endif %}
{% endmacro %}

{% macro transform(property, source, destination) %}
{% if property.required %}
{{ destination }} = {{ source }}.to_dict()
{% else %}
{{ destination }} = {{ source }}.to_dict() if {{ source }} else None
{% endif %}
{% endmacro %}
