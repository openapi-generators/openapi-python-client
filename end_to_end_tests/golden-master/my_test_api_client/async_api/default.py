from dataclasses import asdict
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ..client import AuthenticatedClient, Client
from ..errors import ApiResponseError


async def ping_ping_get(*, client: Client,) -> bool:

    """ A quick check to see if the system is running  """
    url = "{}/ping".format(client.base_url)

    async with httpx.AsyncClient() as _client:
        response = await _client.get(url=url, headers=client.get_headers(),)

    if response.status_code == 200:
        return bool(response.text)
    else:
        raise ApiResponseError(response=response)
