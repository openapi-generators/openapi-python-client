from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

{% for relative in schema.relative_imports %}
{{ relative }}
{% endfor %}


@dataclass
class {{ schema.reference.class_name }}:
    """ {{ schema.description }} """
    {% for property in schema.required_properties + schema.optional_properties %}
    {{ property.to_string() }}
    {% endfor %}

    def to_dict(self) -> Dict[str, Any]:
        {% for property in schema.required_properties + schema.optional_properties %}
        {% if property.template %}
        {% from "property_templates/" + property.template import transform %}
        {{ transform(property, "self." + property.python_name, property.python_name) | indent(8) }}
        {% else %}
        {{ property.python_name }} =  self.{{ property.python_name }}
        {% endif %}
        {% endfor %}

        return {
            {% for property in schema.required_properties + schema.optional_properties %}
            "{{ property.name }}": {{ property.python_name }},
            {% endfor %}
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> {{ schema.reference.class_name }}:
{% for property in schema.required_properties + schema.optional_properties %}
    {% if property.required %}
        {% set property_source = 'd["' + property.name + '"]' %}
    {% else %}
        {% set property_source = 'd.get("' + property.name + '")' %}
    {% endif %}
    {% if property.template %}
        {% from "property_templates/" + property.template import construct %}
        {{ construct(property, property_source) | indent(8) }}
    {% else %}
        {{ property.python_name }} = {{ property_source }}
    {% endif %}

{% endfor %}
        return {{ schema.reference.class_name }}(
{% for property in schema.required_properties + schema.optional_properties %}
            {{ property.python_name }}={{ property.python_name }},
{% endfor %}
        )
