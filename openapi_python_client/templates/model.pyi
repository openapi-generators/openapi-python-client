from typing import Any, Dict, Optional, Set

import attr

from ..types import UNSET

{% for relative in model.relative_imports %}
{{ relative }}
{% endfor %}


@attr.s(auto_attribs=True)
class {{ model.reference.class_name }}:
    """ {{ model.description }} """
    {% for property in model.required_properties + model.optional_properties %}
    {{ property.to_string() }}
    {% endfor %}

    def to_dict(
        self,
        include: Optional[Set[str]] = None,
        exclude: Optional[Set[str]] = None,
        exclude_unset: bool = False,
        exclude_none: bool = False,
    ) -> Dict[str, Any]:
        {% for property in model.required_properties + model.optional_properties %}
        {% if property.template %}
        {% from "property_templates/" + property.template import transform %}
        {{ transform(property, "self." + property.python_name, property.python_name) | indent(8) }}
        {% else %}
        {{ property.python_name }} =  self.{{ property.python_name }}
        {% endif %}
        {% endfor %}

        all_properties = {
            {% for property in model.required_properties + model.optional_properties %}
            "{{ property.name }}": {{ property.python_name }},
            {% endfor %}
        }

        trimmed_properties: Dict[str, Any] = {}
        for property_name, property_value in all_properties.items():
            if include is not None and property_name not in include:
                continue
            if exclude is not None and property_name in exclude:
                continue
            if exclude_unset and property_value is UNSET:
                continue
            if exclude_none and property_value is None:
                continue
            trimmed_properties[property_name] = property_value

        return trimmed_properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "{{ model.reference.class_name }}":
{% for property in model.required_properties + model.optional_properties %}
    {% if property.required %}
        {% set property_source = 'd["' + property.name + '"]' %}
    {% else %}
        {% set property_source = 'd.get("' + property.name + '", UNSET)' %}
    {% endif %}
    {% if property.template %}
        {% from "property_templates/" + property.template import construct %}
        {{ construct(property, property_source) | indent(8) }}
    {% else %}
        {{ property.python_name }} = {{ property_source }}
    {% endif %}

{% endfor %}
        return {{ model.reference.class_name }}(
{% for property in model.required_properties + model.optional_properties %}
            {{ property.python_name }}={{ property.python_name }},
{% endfor %}
        )
