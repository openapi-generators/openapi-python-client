from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.post_parameters_header_response_200 import PostParametersHeaderResponse200
from ...models.public_error import PublicError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    boolean_header: bool,
    string_header: str,
    number_header: float,
    integer_header: int,
) -> Dict[str, Any]:
    url = "{}/parameters/header".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    headers["Boolean-Header"] = "true" if boolean_header else "false"

    headers["String-Header"] = string_header

    headers["Number-Header"] = str(number_header)

    headers["Integer-Header"] = str(integer_header)

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[PostParametersHeaderResponse200, PublicError]]:
    if response.status_code == 200:
        response_200 = PostParametersHeaderResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = PublicError.from_dict(response.json())

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[PostParametersHeaderResponse200, PublicError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    boolean_header: bool,
    string_header: str,
    number_header: float,
    integer_header: int,
) -> Response[Union[PostParametersHeaderResponse200, PublicError]]:
    """
    Args:
        boolean_header (bool):
        string_header (str):
        number_header (float):
        integer_header (int):

    Returns:
        Response[Union[PostParametersHeaderResponse200, PublicError]]
    """

    kwargs = _get_kwargs(
        client=client,
        boolean_header=boolean_header,
        string_header=string_header,
        number_header=number_header,
        integer_header=integer_header,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    boolean_header: bool,
    string_header: str,
    number_header: float,
    integer_header: int,
) -> Optional[Union[PostParametersHeaderResponse200, PublicError]]:
    """
    Args:
        boolean_header (bool):
        string_header (str):
        number_header (float):
        integer_header (int):

    Returns:
        Response[Union[PostParametersHeaderResponse200, PublicError]]
    """

    return sync_detailed(
        client=client,
        boolean_header=boolean_header,
        string_header=string_header,
        number_header=number_header,
        integer_header=integer_header,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    boolean_header: bool,
    string_header: str,
    number_header: float,
    integer_header: int,
) -> Response[Union[PostParametersHeaderResponse200, PublicError]]:
    """
    Args:
        boolean_header (bool):
        string_header (str):
        number_header (float):
        integer_header (int):

    Returns:
        Response[Union[PostParametersHeaderResponse200, PublicError]]
    """

    kwargs = _get_kwargs(
        client=client,
        boolean_header=boolean_header,
        string_header=string_header,
        number_header=number_header,
        integer_header=integer_header,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    boolean_header: bool,
    string_header: str,
    number_header: float,
    integer_header: int,
) -> Optional[Union[PostParametersHeaderResponse200, PublicError]]:
    """
    Args:
        boolean_header (bool):
        string_header (str):
        number_header (float):
        integer_header (int):

    Returns:
        Response[Union[PostParametersHeaderResponse200, PublicError]]
    """

    return (
        await asyncio_detailed(
            client=client,
            boolean_header=boolean_header,
            string_header=string_header,
            number_header=number_header,
            integer_header=integer_header,
        )
    ).parsed
