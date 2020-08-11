from dataclasses import asdict
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ..client import AuthenticatedClient, Client
from ..errors import ApiResponseError


def ping_ping_get(*, client: Client,) -> bool:

    """ A quick check to see if the system is running  """
    url = "{}/ping".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    response = httpx.get(url=url, headers=headers,)

    if response.status_code == 200:
        return bool(response.text)
    else:
        raise ApiResponseError(response=response)
