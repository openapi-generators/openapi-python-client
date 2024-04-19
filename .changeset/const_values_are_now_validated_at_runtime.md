---
default: major
---

# `const` values in responses are now validated at runtime

Prior to this version, `const` values returned from servers were assumed to always be correct. Now, if a server returns 
an unexpected value, the client will raise a `ValueError`. This should enable better usage with `oneOf`.

PR #1024. Thanks @peter-greenatlas!
