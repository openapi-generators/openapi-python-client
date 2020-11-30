from typing import Any, Dict

{% if model.additional_properties %}
from typing import List

{% endif %}

import attr

from ..types import UNSET, Unset

{% for relative in model.relative_imports %}
{{ relative }}
{% endfor %}


{% if model.additional_properties %}
{% set additional_property_type = 'Any' if model.additional_properties == True else model.additional_properties.get_type_string(no_optional=True) %}
{% endif %}

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
    _additional_properties: Dict[str, {{ additional_property_type }}] = attr.ib(init=False, factory=dict)
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
        field_dict.update(self._additional_properties)
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

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "{{ model.reference.class_name }}":
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
        {{model.reference.module_name}} = {{ model.reference.class_name }}(
{% for property in model.required_properties + model.optional_properties %}
            {{ property.python_name }}={{ property.python_name }},
{% endfor %}
        )

        {% if model.additional_properties %}
        {{model.reference.module_name}}._additional_properties = d
        {% endif %}
        return {{model.reference.module_name}}

    {% if model.additional_properties %}

    @property
    def additional_properties(self) -> Dict[str, {{ additional_property_type }}]:
        return self._additional_properties

    @property
    def additional_keys(self) -> List[str]:
        return list(self._additional_properties.keys())

    def __getitem__(self, key: str) -> {{ additional_property_type }}:
        return self._additional_properties[key]

    def __setitem__(self, key: str, value: {{ additional_property_type }}) -> None:
        self._additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self._additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self._additional_properties
    {% endif %}

