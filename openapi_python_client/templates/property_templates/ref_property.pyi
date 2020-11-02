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
{{ destination }} = {{ source }}.to_dict(exclude_unset=True) if {{ source }} else None
{% else %}
{{ destination }} = {{ source }}.to_dict(exclude_unset=True)
{% endif %}
{% else %}
if {{ source }} is UNSET:
    {{ destination }} = UNSET
{% if property.nullable %}
else:
    {{ destination }} = {{ source }}.to_dict(exclude_unset=True) if {{ source }} else None
{% else %}
else:
    {{ destination }} = {{ source }}.to_dict(exclude_unset=True)
{% endif %}
{% endif %}
{% endmacro %}
