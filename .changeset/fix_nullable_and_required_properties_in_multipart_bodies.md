---
default: patch
---

# Fix nullable and required properties in multipart bodies

Fixes #926.

> [!WARNING]
> This change is likely to break custom templates. Multipart body handling has been completely split from JSON bodies.
