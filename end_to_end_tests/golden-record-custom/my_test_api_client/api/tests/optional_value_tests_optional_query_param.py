from typing import Optional

import httpx

Client = httpx.Client

from typing import List, Optional, Union

from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Unset


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, HTTPValidationError]]:
    if response.status_code == 200:
        return None
    if response.status_code == 422:
        return HTTPValidationError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> httpx.Response[Union[None, HTTPValidationError]]:
    return httpx.Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def httpx_request(
    *,
    client: Client,
    query_param: Union[Unset, List[str]] = UNSET,
) -> httpx.Response[Union[None, HTTPValidationError]]:

    json_query_param: Union[Unset, List[Any]] = UNSET
    if not isinstance(query_param, Unset):
        json_query_param = query_param

    params: Dict[str, Any] = {}
    if query_param is not UNSET:
        params["query_param"] = json_query_param

    response = client.request(
        "get",
        "/tests/optional_query_param/",
        params=params,
    )

    return _build_response(response=response)
