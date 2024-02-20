---
default: patch
---

# Fix invalid type check for nested unions

Nested union types (unions of unions) were generating `isinstance()` checks that were not valid (at least for Python 3.9).

Thanks to @codebutler for PR #959 which fixes #958 and #967.
