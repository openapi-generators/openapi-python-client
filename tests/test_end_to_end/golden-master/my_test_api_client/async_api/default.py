from dataclasses import asdict
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ..client import AuthenticatedClient, Client
from ..errors import ApiResponseError
from ..models.abc_response import ABCResponse


async def ping_ping_get(
    *, client: Client,
) -> Union[
    ABCResponse,
]:
    """ A quick check to see if the system is running  """
    url = "{}/ping".format(client.base_url)

    async with httpx.AsyncClient() as _client:
        response = await _client.get(url=url, headers=client.get_headers(),)

    if response.status_code == 200:
        return ABCResponse.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)
