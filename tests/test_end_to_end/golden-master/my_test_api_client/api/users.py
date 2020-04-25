from dataclasses import asdict
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ..client import AuthenticatedClient, Client
from ..errors import ApiResponseError
from ..models.a_model import AModel
from ..models.http_validation_error import HTTPValidationError
from ..models.statuses import Statuses


def get_user_list(
    *, client: Client, statuses: List[Statuses], some_date: date, some_datetime: datetime,
) -> Union[
    List[AModel], HTTPValidationError,
]:
    """ Get users, filtered by statuses  """
    url = "{}/tests/".format(client.base_url)

    params = {
        "statuses": statuses,
        "some_date": some_date.isoformat(),
        "some_datetime": some_datetime.isoformat(),
    }

    response = httpx.get(url=url, headers=client.get_headers(), params=params,)

    if response.status_code == 200:
        return [AModel.from_dict(item) for item in cast(List[Dict[str, Any]], response.json())]
    if response.status_code == 422:
        return HTTPValidationError.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)
