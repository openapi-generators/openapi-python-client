import pytest

from integration_tests.client import Client


@pytest.fixture(scope="session")
def client() -> Client:
    return Client("http://localhost:3000")
