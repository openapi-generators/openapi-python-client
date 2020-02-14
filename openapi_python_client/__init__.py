""" Generate modern Python clients from OpenAPI """
import sys
from typing import Dict

import orjson
import requests

from .models import OpenAPI


def main():
    """ Generate the client library """
    url = sys.argv[1]
    json = _get_json(url)
    data_dict = _parse_json(json)
    openapi = OpenAPI.from_dict(data_dict)
    print(openapi)


def _get_json(url) -> bytes:
    response = requests.get(url)
    return response.content


def _parse_json(json: bytes) -> Dict:
    return orjson.loads(json)
