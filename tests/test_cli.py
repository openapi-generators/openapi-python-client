from unittest.mock import MagicMock

import pytest
from typer.testing import CliRunner

from openapi_python_client.parser.errors import GeneratorError, ParseError

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
    return mocker.patch("openapi_python_client.create_new_client", return_value=[])


def test_bad_config(_create_new_client):
    from openapi_python_client.cli import app

    config_path = "config/path"
    path = "cool/path"

    result = runner.invoke(app, ["generate", f"--config={config_path}", f"--path={path}"])

    assert result.exit_code == 2  # noqa: PLR2004
    assert "Unable to parse config" in result.stdout


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

    def test_generate_encoding_errors(self, _create_new_client):
        path = "cool/path"
        file_encoding = "error-file-encoding"
        from openapi_python_client.cli import app

        result = runner.invoke(app, ["generate", f"--path={path}", f"--file-encoding={file_encoding}"])

        assert result.exit_code == 1
        assert result.output == f"Unknown encoding : {file_encoding}\n"

    def test_generate_handle_errors(self, _create_new_client):
        _create_new_client.return_value = [GeneratorError(detail="this is a message")]
        path = "cool/path"
        from openapi_python_client.cli import app

        result = runner.invoke(app, ["generate", f"--path={path}"])

        assert result.exit_code == 1
        assert result.output == (
            "Error(s) encountered while generating, client was not created\n\n"
            "Unable to generate the client\n\n"
            "this is a message\n\n\n"
            "If you believe this was a mistake or this tool is missing a feature you need, please open an issue at "
            "https://github.com/openapi-generators/openapi-python-client/issues/new/choose\n"
        )

    def test_generate_handle_multiple_warnings(self, _create_new_client):
        error_1 = ParseError(data={"test": "data"}, detail="this is a message")
        error_2 = ParseError(data={"other": "data"}, detail="this is another message", header="Custom Header")
        _create_new_client.return_value = [error_1, error_2]
        path = "cool/path"
        from openapi_python_client.cli import app

        result = runner.invoke(app, ["generate", f"--path={path}"])

        assert result.exit_code == 0
        assert result.output == (
            "Warning(s) encountered while generating. Client was generated, but some pieces may be missing\n\n"
            "Unable to parse this part of your OpenAPI document: \n\n"
            "this is a message\n\n"
            "{'test': 'data'}\n\n"
            "Custom Header\n\n"
            "this is another message\n\n"
            "{'other': 'data'}\n\n"
            "If you believe this was a mistake or this tool is missing a feature you need, please open an issue at "
            "https://github.com/openapi-generators/openapi-python-client/issues/new/choose\n"
        )

    def test_generate_fail_on_warning(self, _create_new_client):
        error_1 = ParseError(data={"test": "data"}, detail="this is a message")
        error_2 = ParseError(data={"other": "data"}, detail="this is another message", header="Custom Header")
        _create_new_client.return_value = [error_1, error_2]
        path = "cool/path"
        from openapi_python_client.cli import app

        result = runner.invoke(app, ["generate", f"--path={path}", "--fail-on-warning"])

        assert result.exit_code == 1
        assert result.output == (
            "Warning(s) encountered while generating. Client was generated, but some pieces may be missing\n\n"
            "Unable to parse this part of your OpenAPI document: \n\n"
            "this is a message\n\n"
            "{'test': 'data'}\n\n"
            "Custom Header\n\n"
            "this is another message\n\n"
            "{'other': 'data'}\n\n"
            "If you believe this was a mistake or this tool is missing a feature you need, please open an issue at "
            "https://github.com/openapi-generators/openapi-python-client/issues/new/choose\n"
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

    def test_update_encoding_errors(self, _update_existing_client):
        path = "cool/path"
        file_encoding = "error-file-encoding"
        from openapi_python_client.cli import app

        result = runner.invoke(app, ["update", f"--path={path}", f"--file-encoding={file_encoding}"])

        assert result.exit_code == 1
        assert result.output == f"Unknown encoding : {file_encoding}\n"
