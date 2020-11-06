from typing import Any, Dict

import attr

from ..types import UNSET, Unset

{% for relative in model.relative_imports %}
{{ relative }}
{% endfor %}


@attr.s(auto_attribs=True)
class {{ model.reference.class_name }}:
    """ {{ model.description }} """
    {% for property in model.required_properties + model.optional_properties %}
    {% if property.default is none and property.required %}
    {{ property.to_string() }}
    {% endif %}
    {% endfor %}
    {% for property in model.required_properties + model.optional_properties %}
    {% if property.default is not none or not property.required %}
    {{ property.to_string() }}
    {% endif %}
    {% endfor %}

    def to_dict(self) -> Dict[str, Any]:
        {% for property in model.required_properties + model.optional_properties %}
        {% if property.template %}
        {% from "property_templates/" + property.template import transform %}
        {{ transform(property, "self." + property.python_name, property.python_name) | indent(8) }}
        {% else %}
        {{ property.python_name }} =  self.{{ property.python_name }}
        {% endif %}
        {% endfor %}


        field_dict = {
            {% for property in model.required_properties + model.optional_properties %}
            {% if property.required %}
            "{{ property.name }}": {{ property.python_name }},
            {% endif %}
            {% endfor %}
        }
        {% for property in model.optional_properties %}
        {% if not property.required %}
        if {{ property.python_name }} is not UNSET:
            field_dict["{{ property.name }}"] = {{ property.python_name }}
        {% endif %}
        {% endfor %}

        return field_dict

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
