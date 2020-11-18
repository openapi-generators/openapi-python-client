{% macro construct(property, source, initial_value="None") %}
{{ property.python_name }} = {{ initial_value }}
{% endmacro %}

{% macro transform(property, source, destination, declare_type=True) %}
{{ destination }} =  None
{% endmacro %}
