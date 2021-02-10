from datetime import date
from typing import cast, Union

from dateutil.parser import isoparse
some_source = date(2020, 10, 12)
some_destination = some_source.isoformat() if some_source else None
a_prop = None
_a_prop = some_destination
if _a_prop is not None:
    a_prop = isoparse(_a_prop).date()


