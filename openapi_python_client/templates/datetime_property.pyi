{% if property.required %}
        {{ property.python_name }} = datetime.fromisoformat(d["{{ property.name }}"])
{% else %}
        {{ property.python_name }} = None
        if ({{ property.python_name }}_string := d.get("{{ property.name }}")) is not None:
            {{ property.python_name }} = datetime.fromisoformat(cast(str, {{ property.python_name }}_string))
{% endif %}
