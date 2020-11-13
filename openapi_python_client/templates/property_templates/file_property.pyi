{% macro construct(property, source, initial_value=None) %}
{{ property.python_name }} = File(
     payload = BytesIO({{ source }})
)
{% endmacro %}

{% macro transform(property, source, destination, declare_type=True) %}
{% if property.required %}
{% if property.nullable %}
{{ destination }} = {{ source }}.to_tuple() if {{ source }} else None
{% else %}
{{ destination }} = {{ source }}.to_tuple()
{% endif %}
{% else %}
{{ destination }}{% if declare_type %}: {{ property.get_type_string() }}{% endif %} = UNSET
if not isinstance({{ source }}, Unset):
{% if property.nullable %}
    {{ destination }} = {{ source }}.to_tuple() if {{ source }} else None
{% else %}
    {{ destination }} = {{ source }}.to_tuple()
{% endif %}
{% endif %}
{% endmacro %}
