{% macro template(property, source) %}
{% if property.required %}
{{ property.python_name }} = {{ property.reference.class_name }}.from_dict({{ source }})
{% else %}
{{ property.python_name }} = None
if {{ source }} is not None:
    {{ property.python_name }} = {{ property.reference.class_name }}.from_dict(cast(Dict[str, Any], {{ source }}))
{% endif %}
{% endmacro %}
