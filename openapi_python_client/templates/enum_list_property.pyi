        {{ property.python_name }} = []
        for {{ property.python_name }}_item in d.get("{{ property.name }}", []):
            {{ property.python_name }}.append({{ property.reference.class_name }}({{ property.python_name }}_item))
