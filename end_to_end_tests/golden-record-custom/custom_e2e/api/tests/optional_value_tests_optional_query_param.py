from typing import Optional

import httpx

from ...types import Response

Client = httpx.Client

from typing import Dict, List, Union

from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Unset


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = None

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def httpx_request(
    *,
    client: Client,
    query_param: Union[Unset, List[str]] = UNSET,
) -> Response[Union[None, HTTPValidationError]]:

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
