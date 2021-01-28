from datetime import date
from typing import cast, Union

from dateutil.parser import isoparse

some_source = date(2020, 10, 12)


some_destination = some_source.isoformat() if some_source else None 




a_prop = None
_a_prop = some_destination
if _a_prop is not None and not isinstance(_a_prop, Unset):
    a_prop = isoparse(cast(str, _a_prop)).date()

