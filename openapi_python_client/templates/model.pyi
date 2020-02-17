from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional, List

{% for relative in schema.relative_imports %}
{{ relative }}
{% endfor %}


@dataclass
class {{ schema.reference.class_name }}:
    {% for property in schema.required_properties %}
    {{ property.to_string() }}
    {% endfor %}
    {% for property in schema.optional_properties %}
    {{ property.to_string() }}
    {% endfor %}
