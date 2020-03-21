from pathlib import PosixPath

import pytest
from typer.testing import CliRunner

runner = CliRunner()


def test_version(mocker):
    generate = mocker.patch("openapi_python_client.cli.generate")
    from openapi_python_client.cli import app

    result = runner.invoke(app, ["--version", "generate"])

    generate.assert_not_called()
    assert result.exit_code == 0
    assert "openapi-python-client version: " in result.stdout


@pytest.fixture
def _create_new_client(mocker):
    return mocker.patch("openapi_python_client.create_new_client")


class TestGenerate:
    def test_generate_no_params(self, _create_new_client):
        from openapi_python_client.cli import app

        result = runner.invoke(app, ["generate"])

        assert result.exit_code == 1
        _create_new_client.assert_not_called()

    def test_generate_url_and_path(self, _create_new_client):
        from openapi_python_client.cli import app

        result = runner.invoke(app, ["generate", "--path=blah", "--url=otherblah"])

        assert result.exit_code == 1
        _create_new_client.assert_not_called()

    def test_generate_url(self, _create_new_client):
        url = "cool.url"
        from openapi_python_client.cli import app

        result = runner.invoke(app, ["generate", f"--url={url}"])

        assert result.exit_code == 0
        _create_new_client.assert_called_once_with(url=url, path=None)

    def test_generate_path(self, _create_new_client):
        path = "cool/path"
        from openapi_python_client.cli import app

        result = runner.invoke(app, ["generate", f"--path={path}"])

        assert result.exit_code == 0
        _create_new_client.assert_called_once_with(url=None, path=PosixPath(path))


@pytest.fixture
def _update_existing_client(mocker):
    return mocker.patch("openapi_python_client.update_existing_client")


class TestUpdate:
    def test_update_no_params(self, _update_existing_client):
        from openapi_python_client.cli import app

        result = runner.invoke(app, ["update"])

        assert result.exit_code == 1
        _update_existing_client.assert_not_called()

    def test_update_url_and_path(self, _update_existing_client):
        from openapi_python_client.cli import app

        result = runner.invoke(app, ["update", "--path=blah", "--url=otherblah"])

        assert result.exit_code == 1
        _update_existing_client.assert_not_called()

    def test_update_url(self, _update_existing_client):
        url = "cool.url"
        from openapi_python_client.cli import app

        result = runner.invoke(app, ["update", f"--url={url}"])

        assert result.exit_code == 0
        _update_existing_client.assert_called_once_with(url=url, path=None)

    def test_update_path(self, _update_existing_client):
        path = "cool/path"
        from openapi_python_client.cli import app

        result = runner.invoke(app, ["update", f"--path={path}"])

        assert result.exit_code == 0
        _update_existing_client.assert_called_once_with(url=None, path=PosixPath(path))
