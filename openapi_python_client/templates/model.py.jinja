from typing import Any, Dict, Type, TypeVar

{% if model.additional_properties %}
from typing import List

{% endif %}

import attr

from ..types import UNSET, Unset

{% for relative in model.relative_imports %}
{{ relative }}
{% endfor %}


{% if model.additional_properties %}
{% set additional_property_type = 'Any' if model.additional_properties == True else model.additional_properties.get_type_string() %}
{% endif %}

T = TypeVar("T", bound="{{ model.reference.class_name }}")

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
    {% if model.additional_properties %}
    additional_properties: Dict[str, {{ additional_property_type }}] = attr.ib(init=False, factory=dict)
    {% endif %}


    def to_dict(self) -> Dict[str, Any]:
        {% for property in model.required_properties + model.optional_properties %}
        {% if property.template %}
        {% from "property_templates/" + property.template import transform %}
        {{ transform(property, "self." + property.python_name, property.python_name) | indent(8) }}
        {% else %}
        {{ property.python_name }} =  self.{{ property.python_name }}
        {% endif %}
        {% endfor %}

        field_dict: Dict[str, Any] = {}
        {% if model.additional_properties %}
        {% if model.additional_properties.template %}
        {% from "property_templates/" + model.additional_properties.template import transform %}
        for prop_name, prop in self.additional_properties.items():
            {{ transform(model.additional_properties, "prop", "field_dict[prop_name]") | indent(12) }}
        {% else %}
        field_dict.update(self.additional_properties)
        {% endif %}
        {% endif %}
        field_dict.update({
            {% for property in model.required_properties + model.optional_properties %}
            {% if property.required %}
            "{{ property.name }}": {{ property.python_name }},
            {% endif %}
            {% endfor %}
        })
        {% for property in model.optional_properties %}
        {% if not property.required %}
        if {{ property.python_name }} is not UNSET:
            field_dict["{{ property.name }}"] = {{ property.python_name }}
        {% endif %}
        {% endfor %}

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
{% for property in model.required_properties + model.optional_properties %}
    {% if property.required %}
        {% set property_source = 'd.pop("' + property.name + '")' %}
    {% else %}
        {% set property_source = 'd.pop("' + property.name + '", UNSET)' %}
    {% endif %}
    {% if property.template %}
        {% from "property_templates/" + property.template import construct %}
        {{ construct(property, property_source) | indent(8) }}
    {% else %}
        {{ property.python_name }} = {{ property_source }}
    {% endif %}

{% endfor %}
        {{model.reference.module_name}} = cls(
{% for property in model.required_properties + model.optional_properties %}
            {{ property.python_name }}={{ property.python_name }},
{% endfor %}
        )

{% if model.additional_properties %}
    {% if model.additional_properties.template %}
        {% from "property_templates/" + model.additional_properties.template import construct %}
        additional_properties = {}
        for prop_name, prop_dict in d.items():
            {{ construct(model.additional_properties, "prop_dict") | indent(12) }}
            additional_properties[prop_name] = {{ model.additional_properties.python_name }}

        {{model.reference.module_name}}.additional_properties = additional_properties
    {% else %}
        {{model.reference.module_name}}.additional_properties = d
    {% endif %}
{% endif %}
        return {{model.reference.module_name}}

    {% if model.additional_properties %}
    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> {{ additional_property_type }}:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: {{ additional_property_type }}) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
    {% endif %}
