---
default: note
---

# Many control characters now stripped from string literals

Out of an abundance of caution, most Unicode control characters are now stripped from string literals.
If your API uses control characters as part of const values, enums, or JSON body property names you may have issues 
with this new version.

Most APIs are not expected to be affected by this change.
