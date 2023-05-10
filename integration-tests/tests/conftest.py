import pytest

from integration_tests.client import Client


@pytest.fixture(scope="session")
def client() -> Client:
    return Client(base_url="http://localhost:3000")
