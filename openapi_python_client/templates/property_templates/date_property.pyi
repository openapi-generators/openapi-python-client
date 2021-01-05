{% macro construct(property, source, initial_value="None") %}
{% if property.required and not property.nullable %}
{{ property.python_name }} = isoparse({{ source }}).date()
{% else %}
{{ property.python_name }} = {{ initial_value }}
_{{ property.python_name }} = {{ source }}
if _{{ property.python_name }} is not None:
    {{ property.python_name }} = isoparse(cast(str, _{{ property.python_name }})).date()
{% endif %}
{% endmacro %}

{% macro transform(property, source, destination, declare_type=True) %}
{% if property.required %}
{{ destination }} = {{ source }}.isoformat() {% if property.nullable %}if {{ source }} else None {%endif%}
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
