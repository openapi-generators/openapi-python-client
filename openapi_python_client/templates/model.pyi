from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional, List

{% for relative in schema.relative_imports %}
{{ relative }}
{% endfor %}


@dataclass
class {{ schema.title }}:
    {% for property in schema.properties %}
    {{ property.to_string() }}
    {% endfor %}
