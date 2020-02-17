{% if property.required %}
        {{ property.name }} = {{ property.reference.class_name }}.from_dict(d["{{ property.name }}"])
{% else %}
        {{ property.name }} = None
        if ({{ property.name }}_data := d.get("{{ property.name }}")) is not None:
            {{ property.name }} = {{ property.reference.class_name }}.from_dict({{ property.name }}_data)
{% endif %}
