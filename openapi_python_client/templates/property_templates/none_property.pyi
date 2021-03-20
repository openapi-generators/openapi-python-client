{% macro construct(property, source, initial_value="None") %}
{{ property.python_name }} = {{ initial_value }}
{% endmacro %}

{% macro check_type_for_construct(source) %}{{ source }} is None{% endmacro %}

{% macro transform(property, source, destination, declare_type=False) %}
{{ destination }} =  None
{% endmacro %}
