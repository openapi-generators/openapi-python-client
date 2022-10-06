{% macro construct(property, source, initial_value="None", nested=False) %}
{% if property.required %}
{{ property.python_name }} = {{ property.reference.class_name }}({{ source }})
{% else %}
{{ property.python_name }} = {{ initial_value }}
_{{ property.python_name }} = {{ source }}
if _{{ property.python_name }} is not None and _{{ property.python_name }} is not UNSET:
    {{ property.python_name }} = {{ property.reference.class_name }}(_{{ property.python_name }})
{% endif %}
{% endmacro %}

{% macro check_type_for_construct(source) %}(isinstance({{ source }}, int) or isinstance({{ source }}, str)){% endmacro %}

{% macro transform(property, source, destination, declare_type=True, query_parameter=False) %}
{% if property.required %}
{% if property.nullable %}
{{ destination }} = {{ source }}.value if {{ source }} else None
{% else %}
{{ destination }} = {{ source }}.value
{% endif %}
{% else %}
{{ destination }}{% if declare_type %}: {{ property.get_type_string(query_parameter=query_parameter, json=True) }}{% endif %} = UNSET
if not isinstance({{ source }}, Unset):
{% if property.nullable %}
    {{ destination }} = {{ source }}.value if {{ source }} else None
{% else %}
    {{ destination }} = {{ source }}.value
{% endif %}
{% endif %}
{% endmacro %}
