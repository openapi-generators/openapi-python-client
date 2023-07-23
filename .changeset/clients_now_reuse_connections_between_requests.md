---
default: minor
---

#### Clients now reuse connections between requests

This happens every time you use the same `Client` or `AuthenticatedClient` instance for multiple requests, however it is best to use a context manager (e.g., `with client as client:`) to ensure the client is closed properly.
