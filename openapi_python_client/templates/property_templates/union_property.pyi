{% macro construct(property, source) %}
def _parse_{{ property.python_name }}(data: Dict[str, Any]) -> {{ property.get_type_string() }}:
    {{ property.python_name }}: {{ property.get_type_string() }}
    {% for inner_property in property.inner_properties %}
    {% if inner_property.template and not loop.last %}
    try:
    {% from "property_templates/" + inner_property.template import construct %}
        {{ construct(inner_property, source) | indent(8) }}
        return {{ property.python_name }}
    except:
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
if {{ source }} is None:
    {{ destination }}: {{ property.get_type_string() }} = None
{% endif %}
{% for inner_property in property.inner_properties %}
    {% if loop.first and property.required %}{# No if None statement before this #}
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
