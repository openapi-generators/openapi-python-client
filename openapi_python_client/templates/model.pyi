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
        return {
            {% for property in schema.required_properties %}
            "{{ property.name }}": self.{{ property.transform() }},
            {% endfor %}
            {% for property in schema.optional_properties %}
            "{{ property.name }}": self.{{ property.transform() }} if self.{{ property.python_name }} is not None else None,
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
    {% if property.constructor_template %}
        {% from property.constructor_template import template %}
        {{ template(property, property_source) | indent(8) }}
    {% else %}
        {{ property.python_name }} = {{ property_source }}
    {% endif %}

{% endfor %}
        return {{ schema.reference.class_name }}(
{% for property in schema.required_properties + schema.optional_properties %}
            {{ property.python_name }}={{ property.python_name }},
{% endfor %}
        )
