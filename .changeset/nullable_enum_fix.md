---
default: patch
---

# Fix class generation for nullable enums in OpenAPI 3.0

Fixed issue #1120, where enum types with `nullable: true` did not work correctly if `type` was also specified.
