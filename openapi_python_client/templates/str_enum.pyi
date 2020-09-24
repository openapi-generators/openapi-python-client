from enum import Enum

class {{ enum.reference.class_name }}(str, Enum):
    {% for key, value in enum.values.items() %}
    {{ key }} = "{{ value }}"
    {% endfor %}
