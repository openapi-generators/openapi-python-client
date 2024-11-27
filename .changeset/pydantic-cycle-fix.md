---
default: patch
---

# Fix for rare Pydantic error

Fixed a subtle issue with forward type references in Pydantic classes that could, in very rare cases, cause the parser to fail with the error "`Parameter` is not fully defined".
