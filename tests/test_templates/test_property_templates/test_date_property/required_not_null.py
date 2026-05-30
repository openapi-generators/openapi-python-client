import datetime
from datetime import date

some_source = date(2020, 10, 12)
some_destination = some_source.isoformat()
a_prop = datetime.date.fromisoformat(some_destination)


