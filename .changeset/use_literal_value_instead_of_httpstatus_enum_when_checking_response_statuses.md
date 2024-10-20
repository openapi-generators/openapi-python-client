---
default: patch
---

# Use literal value instead of `HTTPStatus` enum when checking response statuses

Python 3.13 renamed some of the `HTTPStatus` enum members, which means clients generated with Python 3.13 may not work 
with older versions of Python. This change stops using the `HTTPStatus` enum directly when checking response statuses.

Statuses will still be checked for validity at generation time, and transformed into `HTTPStatus` _after_ being checked 
at runtime.

This may cause some linters to complain.
