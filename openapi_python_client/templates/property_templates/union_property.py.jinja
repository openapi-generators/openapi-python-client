{% macro construct(property, source, initial_value=None) %}
def _parse_{{ property.python_name }}(data: Any) -> {{ property.get_type_string() }}:
    data = None if isinstance(data, Unset) else data
    {{ property.python_name }}: {{ property.get_type_string() }}
    {% for inner_property in property.inner_properties_with_template() %}
    {% if not loop.last or property.has_properties_without_templates %}
    try:
    {% from "property_templates/" + inner_property.template import construct %}
        {{ construct(inner_property, "data", initial_value="UNSET") | indent(8) }}
        return {{ property.python_name }}
    except: # noqa: E722
        pass
    {% else  %}{# Don't do try/except for the last one #}
    {% from "property_templates/" + inner_property.template import construct %}
    {{ construct(inner_property, "data", initial_value="UNSET") | indent(4) }}
    return {{ property.python_name }}
    {% endif %}
    {% endfor %}
    {% if property.has_properties_without_templates %}
    {# Doesn't really matter what we cast it to as this type will be erased, so cast to one of the options #}
    return cast({{ property.get_type_string() }}, data)
    {% endif %}

{{ property.python_name }} = _parse_{{ property.python_name }}({{ source }})
{% endmacro %}

{% macro transform(property, source, destination, declare_type=True) %}
{% if not property.required %}
{{ destination }}{% if declare_type %}: {{ property.get_type_string() }}{% endif %}

if isinstance({{ source }}, Unset):
    {{ destination }} = UNSET
{% endif %}
{% if property.nullable %}
    {% if property.required %}
if {{ source }} is None:
    {% else %}{# There's an if UNSET statement before this #}
elif {{ source }} is None:
    {% endif %}
    {{ destination }}{% if declare_type %}: {{ property.get_type_string() }}{% endif %} = None
{% endif %}
{% for inner_property in property.inner_properties_with_template() %}
    {% if loop.first and property.required and not property.nullable %}{# No if UNSET or if None statement before this #}
if isinstance({{ source }}, {{ inner_property.get_instance_type_string() }}):
    {% elif not loop.last or property.has_properties_without_templates %}
elif isinstance({{ source }}, {{ inner_property.get_instance_type_string() }}):
    {% else %}
else:
    {% endif %}
    {% from "property_templates/" + inner_property.template import transform %}
    {{ transform(inner_property, source, destination, declare_type=False) | indent(4) }}
{% endfor %}
{% if property.has_properties_without_templates and (property.inner_properties_with_template() | any or not property.required)%}
else:
    {{ destination }} = {{ source }}
{% elif property.has_properties_without_templates %}
{{ destination }} = {{ source }}
{% endif %}

{% endmacro %}
