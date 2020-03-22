# {{ project_name }}
{{ description }}

## Usage
First, create a client:

```python
from {{ package_name }} import Client

client = Client(base_url="https://api.example.com")
```

If the endpoints you're going to hit require authentication, use `AuthenticatedClient` instead:

```python
from {{ package_name }} import AuthenticatedClient

client = AuthenticatedClient(base_url="https://api.example.com", token="SuperSecretToken")
```

Now call your endpoint and use your models:

```python
from {{ package_name }}.models import MyDataModel
from {{ package_name }}.api.my_tag import get_my_data_model

my_data: MyDataModel = get_my_data_model(client=client)
```

Or do the same thing with an async version:

```python
from {{ package_name }}.models import MyDataModel
from {{ package_name }}.async_api.my_tag import get_my_data_model

my_data: MyDataModel = await get_my_data_model(client=client)
```

Things to know:
1. Every path/method combo becomes a Python function with type annotations. 
1. All path/query params, and bodies become method arguments.
1. If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above)
1. Any endpoint which did not have a tag will be in `{{ package_name }}.api.default`
1. If the API returns a response code that was not declared in the OpenAPI document, a 
    `{{ package_name }}.api.errors.ApiResponseError` wil be raised 
    with the `response` attribute set to the `httpx.Response` that was received.
    

## Building / publishing this Client
This project uses [Poetry](https://python-poetry.org/) to manage dependencies  and packaging.  Here are the basics:
1. Update the metadata in pyproject.toml (e.g. authors, version)
1. If you're using a private repository, configure it with Poetry
    1. `poetry config repositories.<your-repository-name> <url-to-your-repository>`
    1. `poetry config http-basic.<your-repository-name> <username> <password>`
1. Publish the client with `poetry publish --build -r <your-repository-name>` or, if for public PyPI, just `poetry publish --build`

If you want to install this client into another project without publishing it (e.g. for development) then:
1. If that project **is using Poetry**, you can simply do `poetry add <path-to-this-client>` from that project
1. If that project is not using Poetry:
    1. Build a wheel with `poetry build -f wheel`
    1. Install that wheel from the other project `pip install <path-to-wheel>`
