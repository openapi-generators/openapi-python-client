---
default: minor
---

# Support `application/octet-stream` request bodies

Endpoints that accept `application/octet-stream` request bodies are now supported using the same `File` type as octet-stream responses.

Thanks to @kgutwin for the implementation and @rtaycher for the discussion!

PR #899 closes #588
