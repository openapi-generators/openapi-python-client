---
default: major
---

# Allow case sensitive enum values

#725 by @expobrain

Added setting `case_sensitive_enums` to allow case sensitive enum values in the generated code.

This solve the issue in #587 .

Also, to avoid collisions, changes the prefix for values not starting with alphanumeric characters from `VALUE_` to `LITERAL_`.
