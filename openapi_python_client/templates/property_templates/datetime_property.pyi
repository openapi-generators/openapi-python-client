{% macro construct(property, source, initial_value="None", nested=False) %}
{% if property.required %}
{% if property.nullable %}
{{ property.python_name }} = {{ source }}
{{ property.python_name }} = isoparse({{ property.python_name }}) if {{ property.python_name }} else None
{% else %}
{{ property.python_name }} = isoparse({{ source }})
{% endif %}
{% else %}
{{ property.python_name }} = {{ initial_value }}
_{{ property.python_name }} = {{ source }}
if _{{ property.python_name }} is not None:
    {{ property.python_name }} = isoparse(cast(str, _{{ property.python_name }}))
{% endif %}
{% endmacro %}

{% macro check_type_for_construct(source) %}isinstance({{ source }}, str){% endmacro %}

{% macro transform(property, source, destination, declare_type=True, query_parameter=False) %}
{% if property.required %}
{% if property.nullable %}
{{ destination }} = {{ source }}.isoformat() if {{ source }} else None
{% else %}
{{ destination }} = {{ source }}.isoformat()
{% endif %}
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
