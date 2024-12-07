---
default: major
---

# `type` is now a reserved field name

Because `type` is used in type annotations now, it is no longer a valid field name. Fields which were previously named 
`type` will be renamed to `type_`.
