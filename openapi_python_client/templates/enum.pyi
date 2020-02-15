from enum import Enum

class {{ enum.class_name }}(Enum):
    {% for key, value in enum.values.items() %}
    {{ key }} = "{{ value }}"
    {% endfor %}
