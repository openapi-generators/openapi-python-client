{% macro construct(property, source) %}
def _parse_{{ property.python_name }}(data: Dict[str, Any]) -> {{ property.get_type_string() }}:
    {{ property.python_name }}: {{ property.get_type_string() }}
    {% for inner_property in property.inner_properties %}
    {% if inner_property.template and not loop.last %}
    try:
    {% from "property_templates/" + inner_property.template import construct %}
        {{ construct(inner_property, source) | indent(8) }}
        return {{ property.python_name }}
    except: # noqa: E722
        pass
    {% elif inner_property.template and loop.last %}{# Don't do try/except for the last one #}
    {% from "property_templates/" + inner_property.template import construct %}
    {{ construct(inner_property, source) | indent(4) }}
    return {{ property.python_name }}
    {% else %}
    return {{ source }}
    {% endif %}
    {% endfor %}

{{ property.python_name }} = _parse_{{ property.python_name }}({{ source }})
{% endmacro %}

{% macro transform(property, source, destination) %}
{% if not property.required %}
{{ destination }}: {{ property.get_type_string() }}
if isinstance({{ source }}, Unset):
    {{ destination }} = UNSET
{% endif %}
{% if property.nullable %}
{% if property.required %}
if {{ source }} is None:
{% else %}{# There's an if UNSET statement before this #}
elif {{ source }} is None:
{% endif %}
    {{ destination }}: {{ property.get_type_string() }} = None
{% endif %}
{% for inner_property in property.inner_properties %}
    {% if loop.first and property.required and not property.nullable %}{# No if UNSET or if None statement before this #}
if isinstance({{ source }}, {{ inner_property.get_type_string(no_optional=True) }}):
    {% elif not loop.last %}
elif isinstance({{ source }}, {{ inner_property.get_type_string(no_optional=True) }}):
    {% else %}
else:
    {% endif %}
{% if inner_property.template %}
{% from "property_templates/" + inner_property.template import transform %}
    {{ transform(inner_property, source, destination) | indent(8) }}
{% else %}
    {{ destination }} = {{ source }}
{% endif %}
{% endfor %}
{% endmacro %}
