---
default: patch
---

# Change default Ruff hook to `--fix-only`

This should enable `openapi-python-client` to keep auto-fixing lints (like removing unused imports) but _not_ fail to 
generate when unfixable lints are violated.

Since it's now unlikely for breaking changes to affect our usage (and by popular request), the upper bound of `ruff` 
has been lifted. Newer versions of `openapi-python-client` should no longer be required to support newer versions of `ruff`.
