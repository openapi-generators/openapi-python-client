        {{ property.python_name }} = []
        for {{ property.python_name }}_item in d.get("{{ property.python_name }}", []):
            {{ property.python_name }}.append({{ property.reference.class_name }}.from_dict({{ property.python_name }}_item))
