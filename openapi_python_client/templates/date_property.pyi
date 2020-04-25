{% if property.required %}
        {{ property.name }} = date.fromisoformat(d["{{ property.name }}"])
{% else %}
        {{ property.name }} = None
        if ({{ property.name }}_string := d.get("{{ property.name }}")) is not None:
            {{ property.name }} = date.fromisoformat(cast(str, {{ property.name }}_string))
{% endif %}
