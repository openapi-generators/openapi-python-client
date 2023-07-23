---
default: minor
---

#### Allow customizing the underlying `httpx` clients

There are many use-cases where customizing the underlying `httpx` client directly is necessary. Some examples are:

- [Event hooks](https://www.python-httpx.org/advanced/#event-hooks)
- [Proxies](https://www.python-httpx.org/advanced/#http-proxying)
- [Custom authentication](https://www.python-httpx.org/advanced/#customizing-authentication)
- [Retries](https://www.python-httpx.org/advanced/#usage_1)

The new `Client` and `AuthenticatedClient` classes come with several methods to customize underlying clients. You can pass arbitrary arguments to `httpx.Client` or `httpx.AsyncClient` when they are constructed:

```python
client = Client(base_url="https://api.example.com", httpx_args={"proxies": {"https://": "https://proxy.example.com"}})
```

**The underlying clients are constructed lazily, only when needed. `httpx_args` are stored internally in a dictionary until the first request is made.**

You can force immediate construction of an underlying client in order to edit it directly:

```python
import httpx
from my_api import Client

client = Client(base_url="https://api.example.com")
sync_client: httpx.Client = client.get_httpx_client()
sync_client.timeout = 10
async_client = client.get_async_httpx_client()
async_client.timeout = 15
```

You can also completely override the underlying clients:

```python
import httpx
from my_api import Client

client = Client(base_url="https://api.example.com")
# The params you put in here ^ are discarded when you call set_httpx_client or set_async_httpx_client
sync_client = httpx.Client(base_url="https://api.example.com", timeout=10)
client.set_httpx_client(sync_client)
async_client = httpx.AsyncClient(base_url="https://api.example.com", timeout=15)
client.set_async_httpx_client(async_client)
```
