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
{% if property.nullable %}
{{ destination }} = {{ source }}.to_dict() if {{ source }} else None
{% else %}
{{ destination }} = {{ source }}.to_dict()
{% endif %}
{% else %}
{{ destination }}: {{ property.get_type_string() }} = UNSET
if not isinstance({{ source }}, Unset):
{% if property.nullable %}
    {{ destination }} = {{ source }}.to_dict() if {{ source }} else None
{% else %}
    {{ destination }} = {{ source }}.to_dict()
{% endif %}
{% endif %}
{% endmacro %}
