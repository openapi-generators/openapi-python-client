from datetime import date
from typing import cast, Union

from dateutil.parser import isoparse

some_source = date(2020, 10, 12)


some_destination = some_source.isoformat() 




a_prop = isoparse(some_destination).date()

