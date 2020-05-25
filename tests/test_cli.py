from pathlib import PosixPath
from unittest.mock import MagicMock

import pytest
from typer.testing import CliRunner

from openapi_python_client.openapi_parser.errors import ParseError

runner = CliRunner()


def test_version(mocker):
    generate = mocker.patch("openapi_python_client.cli.generate")
    from openapi_python_client.cli import app

    result = runner.invoke(app, ["--version", "generate"])

    generate.assert_not_called()
    assert result.exit_code == 0
    assert "openapi-python-client version: " in result.stdout


@pytest.fixture
def _create_new_client(mocker) -> MagicMock:
    return mocker.patch("openapi_python_client.create_new_client")


def test_config(mocker, _create_new_client):
    load_config = mocker.patch("openapi_python_client.load_config")
    from openapi_python_client.cli import app

    config_path = "config/path"
    path = "cool/path"

    result = runner.invoke(app, [f"--config={config_path}", "generate", f"--path={path}"], catch_exceptions=False)

    assert result.exit_code == 0
    load_config.assert_called_once_with(path=PosixPath(config_path))
    _create_new_client.assert_called_once_with(url=None, path=PosixPath(path))


def test_bad_config(mocker, _create_new_client):
    load_config = mocker.patch("openapi_python_client.load_config", side_effect=ValueError("Bad Config"))
    from openapi_python_client.cli import app

    config_path = "config/path"
    path = "cool/path"

    result = runner.invoke(app, [f"--config={config_path}", "generate", f"--path={path}"])

    assert result.exit_code == 2
    assert "Unable to parse config" in result.stdout
    load_config.assert_called_once_with(path=PosixPath(config_path))
    _create_new_client.assert_not_called()


class TestGenerate:
    def test_generate_no_params(self, _create_new_client):
        from openapi_python_client.cli import app

        result = runner.invoke(app, ["generate"])

        assert result.exit_code == 1, result.output
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

    def test_generate_handle_errors(self, _create_new_client):
        _create_new_client.side_effect = ParseError({"test": "data"}, "this is a message")
        path = "cool/path"
        from openapi_python_client.cli import app

        result = runner.invoke(app, ["generate", f"--path={path}"])

        assert result.exit_code == 1
        assert result.output == (
            "ERROR: Unable to parse this part of your OpenAPI document: \n"
            "{'test': 'data'}\n"
            "this is a message\n"
            "Please open an issue at https://github.com/triaxtec/openapi-python-client/issues/new/choose\n\n"
        )


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
