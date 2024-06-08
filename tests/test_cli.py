from typer.testing import CliRunner

runner = CliRunner()


def test_version():
    from openapi_python_client.cli import app

    result = runner.invoke(app, ["--version", "generate"])

    assert result.exit_code == 0
    assert "openapi-python-client version: " in result.stdout


def test_bad_config():
    from openapi_python_client.cli import app

    config_path = "config/path"
    path = "cool/path"

    result = runner.invoke(app, ["generate", f"--config={config_path}", f"--path={path}"])

    assert result.exit_code == 2  # noqa: PLR2004
    assert "Unable to parse config" in result.stdout


class TestGenerate:
    def test_generate_no_params(self):
        from openapi_python_client.cli import app

        result = runner.invoke(app, ["generate"])

        assert result.exit_code == 1, result.output

    def test_generate_url_and_path(self):
        from openapi_python_client.cli import app

        result = runner.invoke(app, ["generate", "--path=blah", "--url=otherblah"])

        assert result.exit_code == 1
        assert result.output == "Provide either --url or --path, not both\n"

    def test_generate_encoding_errors(self):
        path = "cool/path"
        file_encoding = "error-file-encoding"
        from openapi_python_client.cli import app

        result = runner.invoke(app, ["generate", f"--path={path}", f"--file-encoding={file_encoding}"])

        assert result.exit_code == 1
        assert result.output == f"Unknown encoding : {file_encoding}\n"
