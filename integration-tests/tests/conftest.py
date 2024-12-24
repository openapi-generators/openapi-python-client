import pytest

from integration_tests.client import Client


@pytest.fixture
def client() -> Client:
    return Client("http://localhost:3000")
