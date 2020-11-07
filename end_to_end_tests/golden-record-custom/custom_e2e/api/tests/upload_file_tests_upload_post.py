from typing import Optional

import httpx

Client = httpx.Client

from typing import Union

from ...models.body_upload_file_tests_upload_post import BodyUploadFileTestsUploadPost
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Unset


def _parse_response(*, response: httpx.Response) -> Optional[Union[
    None,
    HTTPValidationError
]]:
    if response.status_code == 200:
        return None
    if response.status_code == 422:
        return HTTPValidationError.from_dict(cast(Dict[str, Any], response.json()))
    return None



def _build_response(*, response: httpx.Response) -> httpx.Response[Union[
    None,
    HTTPValidationError
]]:
    return httpx.Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def httpx_request(*,
    client: Client,
    multipart_data: BodyUploadFileTestsUploadPost,
    keep_alive: Union[Unset, bool] = UNSET,
) -> httpx.Response[Union[
    None,
    HTTPValidationError
]]:
    if keep_alive is not UNSET:
        headers["keep-alive"] = keep_alive

    
    

    response = client.request(
        "post",
        "/tests/upload",
        "files": multipart_data.to_dict(),
    )

    return _build_response(response=response)