{% macro construct(property, source, initial_value=None) %}
{% if property.required %}
{{ property.python_name }} = {{ property.reference.class_name }}.from_dict({{ source }})
{% else %}
{% if initial_value != None %}
{{ property.python_name }} = {{ initial_value }}
{% elif property.nullable %}
{{ property.python_name }} = None
{% else %}
{{ property.python_name }} = UNSET
{% endif %}
_{{ property.python_name }} = {{source}}
if _{{ property.python_name }} is not None and not isinstance({{ property.python_name }},  Unset):
    {{ property.python_name }} = {{ property.reference.class_name }}.from_dict(cast(Dict[str, Any], _{{ property.python_name }}))
{% endif %}
{% endmacro %}

{% macro transform(property, source, destination, declare_type=True) %}
{% if property.required %}
{% if property.nullable %}
{{ destination }} = {{ source }}.to_dict() if {{ source }} else None
{% else %}
{{ destination }} = {{ source }}.to_dict()
{% endif %}
{% else %}
{{ destination }}{% if declare_type %}: Union[{% if property.nullable %}None, {% endif %}Unset, Dict[str, Any]]{% endif %} = UNSET
if not isinstance({{ source }}, Unset):
{% if property.nullable %}
    {{ destination }} = {{ source }}.to_dict() if {{ source }} else None
{% else %}
    {{ destination }} = {{ source }}.to_dict()
{% endif %}
{% endif %}
{% endmacro %}
