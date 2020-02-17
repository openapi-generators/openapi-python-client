from enum import Enum

class {{ enum.reference.class_name }}(Enum):
    {% for key, value in enum.values.items() %}
    {{ key }} = "{{ value }}"
    {% endfor %}
