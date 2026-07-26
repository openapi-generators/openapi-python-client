import pytest
from jinja2 import Environment, PackageLoader


@pytest.fixture(scope="session")
def env() -> Environment:
    from openapi_python_client import TEMPLATE_FILTERS

    env = Environment(loader=PackageLoader("openapi_python_client"), trim_blocks=True, lstrip_blocks=True)
    env.filters.update(TEMPLATE_FILTERS)
    return env
