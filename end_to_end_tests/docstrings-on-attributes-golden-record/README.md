# my-test-api-client
A client library for accessing My Test API

## Usage
First, create a client:

```python
from my_test_api_client import Client

client = Client(base_url="https://api.example.com")
```

If the endpoints you're going to hit require authentication, use `AuthenticatedClient` instead:

```python
from my_test_api_client import AuthenticatedClient

client = AuthenticatedClient(base_url="https://api.example.com", token="SuperSecretToken")
```

Now call your endpoint and use your models. Endpoints are async:

```python
from my_test_api_client.models import MyDataModel
from my_test_api_client.api.my_tag import get_my_data_model

async with client as client:
    my_data: MyDataModel = await get_my_data_model.request(client=client)
```

An endpoint whose response is `application/jsonl` exposes `stream` instead, an async generator over the
parsed items:

```python
from my_test_api_client.api.my_tag import get_my_data_stream

async with client as client:
    async for item in get_my_data_stream.stream(client=client):
        print(item)
```

By default, when you're calling an HTTPS API it will attempt to verify that SSL is working correctly. Using certificate verification is highly recommended most of the time, but sometimes you may need to authenticate to a server (especially an internal server) using a custom certificate bundle.

```python
client = AuthenticatedClient(
    base_url="https://internal_api.example.com", 
    token="SuperSecretToken",
    verify_ssl="/path/to/certificate_bundle.pem",
)
```

You can also disable certificate validation altogether, but beware that **this is a security risk**.

```python
client = AuthenticatedClient(
    base_url="https://internal_api.example.com", 
    token="SuperSecretToken", 
    verify_ssl=False
)
```

Things to know:
1. Every path/method combo becomes a Python module. A regular endpoint exposes:
    1. `request`: Async request that returns the parsed response body.
    1. `_request_detailed`: Same request, but returns a `Response` wrapper with the status code, headers and
       raw content alongside `parsed`. Prefixed with `_` because the parsed body is what you normally want.

   An `application/jsonl` endpoint exposes `stream` instead, an async generator over the parsed items.

1. An undocumented status code raises `errors.UnexpectedStatus` when `Client.raise_on_unexpected_status` is
   set (the default); otherwise `request` returns `None` for it. `stream` raises either way, since an async
   generator has no value to hand back and would otherwise look like an empty stream.

1. All path/query params, and bodies become method arguments.
1. If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above)
1. Any endpoint which did not have a tag will be in `my_test_api_client.api.default`

## Advanced customizations

There are more settings on the generated `Client` class which let you control more runtime behavior, check out the docstring on that class for more info. You can also customize the underlying `httpx.AsyncClient`, which is the one endpoints issue requests through:

```python
from my_test_api_client import Client

def log_request(request):
    print(f"Request event hook: {request.method} {request.url} - Waiting for response")

def log_response(response):
    request = response.request
    print(f"Response event hook: {request.method} {request.url} - Status {response.status_code}")

client = Client(
    base_url="https://api.example.com",
    httpx_args={"event_hooks": {"request": [log_request], "response": [log_response]}},
)

# Or get the underlying httpx client to modify directly with client.get_async_httpx_client()
```

You can even set the httpx client directly, but beware that this will override any existing settings (e.g., base_url):

```python
import httpx
from my_test_api_client import Client

client = Client(
    base_url="https://api.example.com",
)
# Note that base_url needs to be re-set, as would any shared cookies, headers, etc.
client.set_async_httpx_client(httpx.AsyncClient(base_url="https://api.example.com", proxies="http://localhost:8030"))
```

## Building / publishing this package
This project uses [uv](https://github.com/astral-sh/uv) to manage dependencies and packaging. Here are the basics:
1. Update the metadata in `pyproject.toml` (e.g. authors, version).
2. If you're using a private repository: https://docs.astral.sh/uv/guides/integration/alternative-indexes/
3. Build a distribution with `uv build`, builds `sdist` and `wheel` by default.
1. Publish the client with `uv publish`, see documentation for publishing to private indexes.

If you want to install this client into another project without publishing it (e.g. for development) then:
1. If that project **is using uv**, you can simply do `uv add <path-to-this-client>` from that project
1. If that project is not using uv:
    1. Build a wheel with `uv build --wheel`.
    1. Install that wheel from the other project `pip install <path-to-wheel>`.
