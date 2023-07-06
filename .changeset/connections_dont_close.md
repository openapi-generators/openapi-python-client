---
default: major
---

#### Connections from clients no longer automatically close (PR [#775](https://github.com/openapi-generators/openapi-python-client/pull/775))

`Client` and `AuthenticatedClient` now reuse an internal [`httpx.Client`](https://www.python-httpx.org/advanced/#client-instances) (or `AsyncClient`)—keeping connections open between requests. This will improve performance overall, but may cause resource leaking if clients are not closed properly. The new clients are intended to be used via context managers—though for compatibility they don't _have_ to be used with context managers. If not using a context manager, connections will probably leak. Note that once a client is closed (by leaving the context manager), it can no longer be used—and attempting to do so will raise an exception.

APIs should now be called like:

```python
with client as client:
    my_api.sync(client)
    another_api.sync(client)
# client is closed here and can no longer be used
```

Generated READMEs reflect the new syntax, but READMEs for existing generated clients should be updated manually. See [this diff](https://github.com/openapi-generators/openapi-python-client/pull/775/files#diff-62b50316369f84439d58f4981c37538f5b619d344393cb659080dadbda328547) for inspiration.
