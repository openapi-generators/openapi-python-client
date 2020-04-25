{% if property.required %}
        {{ property.python_name }} = {{ property.reference.class_name }}.from_dict(d["{{ property.name }}"])
{% else %}
        {{ property.python_name }} = None
        if ({{ property.python_name }}_data := d.get("{{ property.name }}")) is not None:
            {{ property.python_name }} = {{ property.reference.class_name }}.from_dict(cast(Dict[str, Any], {{ property.python_name }}_data))
{% endif %}
