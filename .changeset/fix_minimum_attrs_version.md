---
default: patch
---

# Fix minimum `attrs` version

The minimum `attrs` dependency version was incorrectly set to 21.3.0. This has been corrected to 22.2.0, the minimum 
supported version since `openapi-python-client` 0.19.1.

Closes #1084, thanks @astralblue!
