from typing import Any, Dict

import httpx

from ...client import Client
from ...types import UNSET, Response


def _get_kwargs(
    param_path: str,
    *,
    client: Client,
    param_query: str = "overridden_in_GET",
) -> Dict[str, Any]:
    url = "{}/common_parameters_overriding/{param}".format(client.base_url, param=param_path)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["param"] = param_query

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    param_path: str,
    *,
    client: Client,
    param_query: str = "overridden_in_GET",
) -> Response[Any]:
    """Test that if you have an overriding property from `PathItem` in `Operation`, it produces valid code

    Args:
        param_path (str):
        param_query (str): A parameter with the same name as another. Default:
            'overridden_in_GET'. Example: an example string.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        param_path=param_path,
        client=client,
        param_query=param_query,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    param_path: str,
    *,
    client: Client,
    param_query: str = "overridden_in_GET",
) -> Response[Any]:
    """Test that if you have an overriding property from `PathItem` in `Operation`, it produces valid code

    Args:
        param_path (str):
        param_query (str): A parameter with the same name as another. Default:
            'overridden_in_GET'. Example: an example string.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        param_path=param_path,
        client=client,
        param_query=param_query,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
