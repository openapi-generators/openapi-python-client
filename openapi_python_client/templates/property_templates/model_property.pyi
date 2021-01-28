{% macro construct(property, source, initial_value=None) %}
{% if property.required and not property.nullable %}
if not isinstance({{ source }}, dict):
    raise ValueError("Cannot construct model from value " + str({{ source }}))
{{ property.python_name }} = {{ property.reference.class_name }}.from_dict({{ source }})
{% else %}
{% if initial_value != None %}
{{ property.python_name }} = {{ initial_value }}
{% elif property.nullable %}
{{ property.python_name }} = None
{% else %}
{{ property.python_name }}: {{ property.get_type_string() }} = UNSET
{% endif %}
if {{ source }} is not None and not isinstance({{ source }},  Unset):
    if not isinstance({{ source }}, dict):
        raise ValueError("Cannot construct model from value " + str({{ source }}))
    {{ property.python_name }} = {{ property.reference.class_name }}.from_dict({{ source }})
{% endif %}
{% endmacro %}

{% macro transform(property, source, destination, declare_type=True, query_parameter=False) %}
{% if property.required %}
{% if property.nullable %}
{{ destination }} = {{ source }}.to_dict() if {{ source }} else None
{% else %}
{{ destination }} = {{ source }}.to_dict()
{% endif %}
{% else %}
{{ destination }}{% if declare_type %}: {{ property.get_type_string(query_parameter=query_parameter, json=True) }}{% endif %} = UNSET
if not isinstance({{ source }}, Unset):
{% if property.nullable or query_parameter %}
    {{ destination }} = {{ source }}.to_dict() if {{ source }} else None
{% else %}
    {{ destination }} = {{ source }}.to_dict()
{% endif %}
{% endif %}
{% endmacro %}
