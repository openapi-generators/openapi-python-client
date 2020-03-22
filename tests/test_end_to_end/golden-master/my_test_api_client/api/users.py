from dataclasses import asdict
from typing import Dict, List, Optional, Union

import httpx

from ..client import AuthenticatedClient, Client
from ..errors import ApiResponseError
from ..models.h_t_t_p_validation_error import HTTPValidationError
from ..models.statuses import Statuses
from ..models.test_model import TestModel


def test_getting_lists_tests__get(
    *, client: Client, statuses: List[Statuses],
) -> Union[
    List[TestModel], HTTPValidationError,
]:
    """ Get users, filtered by statuses  """
    url = f"{client.base_url}/tests/"

    params = {
        "statuses": statuses,
    }

    response = httpx.get(url=url, headers=client.get_headers(), params=params,)

    if response.status_code == 200:
        return [TestModel.from_dict(item) for item in response.json()]
    if response.status_code == 422:
        return HTTPValidationError.from_dict(response.json())
    else:
        raise ApiResponseError(response=response)
