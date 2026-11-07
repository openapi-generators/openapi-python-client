---
default: patch
---

# Fixed generated endpoints breaking when a schema is named `Client`, `AuthenticatedClient`, `Response` or `HTTPStatus`

Generated endpoint modules imported the SDK's `Client`, `AuthenticatedClient` and `Response` classes and the standard library's `HTTPStatus` under their bare names, so a model with one of those names shadowed them. Depending on the name this produced wrong type annotations, a failed response build, or a `Response.status_code` that held a model instance instead of an `HTTPStatus`. Endpoint modules now bind these generator-owned symbols under private aliases, leaving the public model names unchanged.
