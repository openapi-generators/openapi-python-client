from enum import IntEnum

class {{ enum.reference.class_name }}(IntEnum):
    {% for key, value in enum.values.items() %}
    {{ key }} = {{ value }}
    {% endfor %}
