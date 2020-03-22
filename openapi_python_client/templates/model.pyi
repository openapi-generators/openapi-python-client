from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, cast

{% for relative in schema.relative_imports %}
{{ relative }}
{% endfor %}


@dataclass
class {{ schema.reference.class_name }}:
    """ {{ schema.description }} """
    {% for property in schema.required_properties + schema.optional_properties %}
    {{ property.to_string() }}
    {% endfor %}

    def to_dict(self) -> Dict:
        return {
            {% for property in schema.required_properties %}
            "{{ property.name }}": self.{{ property.transform() }},
            {% endfor %}
            {% for property in schema.optional_properties %}
            "{{ property.name }}": self.{{ property.transform() }} if self.{{ property.name }} is not None else None,
            {% endfor %}
        }

    @staticmethod
    def from_dict(d: Dict) -> {{ schema.reference.class_name }}:
        {% for property in schema.required_properties + schema.optional_properties %}

        {% if property.constructor_template %}
        {% include property.constructor_template %}
        {% else %}
        {{ property.name }} = {{ property.constructor_from_dict("d") }}
        {% endif %}

        {% endfor %}
        return {{ schema.reference.class_name }}(
            {% for property in schema.required_properties + schema.optional_properties %}
            {{ property.name }}={{ property.name }},
            {% endfor %}
        )
