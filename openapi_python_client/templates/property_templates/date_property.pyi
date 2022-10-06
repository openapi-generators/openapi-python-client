{% macro construct(property, source, initial_value="None", nested=False) %}
{% if property.required and not property.nullable %}
{{ property.python_name }} = isoparse({{ source }}).date()
{% else %}
{{ property.python_name }} = {{ initial_value }}
_{{ property.python_name }} = {{ source }}
if _{{ property.python_name }} is not None:
    {{ property.python_name }} = isoparse(cast(str, _{{ property.python_name }})).date()
{% endif %}
{% endmacro %}

{% macro check_type_for_construct(source) %}isinstance({{ source }}, str){% endmacro %}

{% macro transform(property, source, destination, declare_type=True, query_parameter=False) %}
{% if property.required %}
{{ destination }} = {{ source }}.isoformat() {% if property.nullable %}if {{ source }} else None {%endif%}
{% else %}
{{ destination }}{% if declare_type %}: {{ property.get_type_string(query_parameter=query_parameter, json=True) }}{% endif %} = UNSET
if not isinstance({{ source }}, Unset):
{% if property.nullable %}
    {{ destination }} = {{ source }}.isoformat() if {{ source }} else None
{% else %}
    {{ destination }} = {{ source }}.isoformat()
{% endif %}
{% endif %}
{% endmacro %}
