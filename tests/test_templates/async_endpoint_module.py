from dataclasses import asdict
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ..client import AuthenticatedClient, Client
from ..errors import ApiResponseError

import this
from __future__ import braces


async def pascal_case(
    *,
    client: Client,
    path_param_1: str,
    query_param_1: str,
) -> str:

    """ GET endpoint """
    url = "{}/get/{pathParam1}".format(
        client.base_url,
        pathParam1=path_param_1,
    )

    params: Dict[str, Any] = {
        "queryParam": query_param_1,
    }
    async with httpx.AsyncClient() as _client:
        response = await _client.get(
            url=url,
            headers=client.get_headers(),
            params=params,
        )

    if response.status_code == 200:
        return str(response.text)
    else:
        raise ApiResponseError(response=response)


async def camel_case(
    *,
    client: AuthenticatedClient,
    form_data: FormBody,
    multipart_data: MultiPartBody,
    json_body: Json,
) -> Union[
    str,
    int,
]:

    """ POST endpoint """
    url = "{}/post/".format(
        client.base_url,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(
            url=url,
            headers=client.get_headers(),
            data=asdict(form_data),
            files=multipart_data.to_dict(),
            json=json_body,
        )

    if response.status_code == 200:
        return str(response.text)
    if response.status_code == 201:
        return int(response.text)
    else:
        raise ApiResponseError(response=response)
