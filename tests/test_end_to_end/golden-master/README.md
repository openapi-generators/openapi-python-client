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

Now call your endpoint and use your models:

```python
from my_test_api_client.models import MyDataModel
from my_test_api_client.api.my_tag import get_my_data_model

my_data: MyDataModel = get_my_data_model(client=client)
```

Things to know:
1. Every path/method combo becomes a Python function with type annotations. 
1. All path/query params, and bodies become method arguments.
1. If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above)
1. Any endpoint which did not have a tag will be in `my_test_api_client.api.default`
1. If the API returns a response code that was not declared in the OpenAPI document, a 
    `my_test_api_client.api.errors.ApiResponseError` wil be raised 
    with the `response` attribute set to the `httpx.Response` that was received.