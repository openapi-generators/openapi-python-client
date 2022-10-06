{% macro construct(property, source, initial_value="None", nested=False) %}
{{ property.python_name }} = {{ initial_value }}
{% endmacro %}

{% macro check_type_for_construct(source) %}{{ source }} is None{% endmacro %}

{% macro transform(property, source, destination, declare_type=True) %}
{{ destination }} =  None
{% endmacro %}
