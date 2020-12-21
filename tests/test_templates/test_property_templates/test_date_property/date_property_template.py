from datetime import date
from typing import cast, Union

from dateutil.parser import isoparse
{% from "property_templates/date_property.pyi" import transform, construct %}
some_source = date(2020, 10, 12)
{{ transform(property, "some_source", "some_destination") }}
{{ construct(property, "some_destination") }}
