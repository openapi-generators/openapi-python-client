{% macro construct(property, source) %}
{% if property.required %}
{{ property.python_name }} = isoparse({{ source }})
{% else %}
{{ property.python_name }} = None
if {{ source }} is not None:
    {{ property.python_name }} = isoparse(cast(str, {{ source }}))
{% endif %}
{% endmacro %}

{% macro transform(property, source, destination, declare_type=True) %}
{% if property.required %}
{% if property.nullable %}
{{ destination }} = {{ source }}.isoformat() if {{ source }} else None
{% else %}
{{ destination }} = {{ source }}.isoformat()
{% endif %}
{% else %}
{{ destination }}{% if declare_type %}: Union[Unset, str]{% endif %} = UNSET
if not isinstance({{ source }}, Unset):
{% if property.nullable %}
    {{ destination }} = {{ source }}.isoformat() if {{ source }} else None
{% else %}
    {{ destination }} = {{ source }}.isoformat()
{% endif %}
{% endif %}
{% endmacro %}
