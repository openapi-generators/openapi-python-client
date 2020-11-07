{% macro construct(property, source) %}
{{ property.python_name }} = File(
     payload = BytesIO({{ source }})
)
{% endmacro %}

{% macro transform(property, source, destination) %}
{% if property.required %}
{% if property.nullable %}
{{ destination }} = {{ source }}.to_tuple() if {{ source }} else None
{% else %}
{{ destination }} = {{ source }}.to_tuple()
{% endif %}
{% else %}
{{ destination }}: {{ property.get_type_string() }} = UNSET
if not isinstance({{ source }}, Unset):
{% if property.nullable %}
    {{ destination }} = {{ source }}.to_tuple() if {{ source }} else None
{% else %}
    {{ destination }} = {{ source }}.to_tuple()
{% endif %}
{% endif %}
{% endmacro %}
