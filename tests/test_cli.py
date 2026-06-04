import json

from typer.testing import CliRunner

from openapi_python_client.cli import app

runner = CliRunner()


def test_version() -> None:
    result = runner.invoke(app, ["--version", "generate"])

    assert result.exit_code == 0
    assert "openapi-python-client version: " in result.stdout


def test_bad_config() -> None:
    config_path = "config/path"
    path = "cool/path"

    result = runner.invoke(app, ["generate", f"--config={config_path}", f"--path={path}"])

    assert result.exit_code == 2
    assert "Unable to parse config" in result.output


class TestGenerate:
    def test_generate_no_params(self) -> None:
        result = runner.invoke(app, ["generate"])

        assert result.exit_code == 1, result.output

    def test_generate_url_and_path(self) -> None:
        result = runner.invoke(app, ["generate", "--path=blah", "--url=otherblah"])

        assert result.exit_code == 1
        assert result.output == "Provide either --url or --path, not both\n"

    def test_generate_encoding_errors(self) -> None:
        path = "cool/path"
        file_encoding = "error-file-encoding"
        result = runner.invoke(app, ["generate", f"--path={path}", f"--file-encoding={file_encoding}"])

        assert result.exit_code == 1
        assert result.output == f"Unknown encoding : {file_encoding}\n"


class TestTagFilterOptions:
    def _config_from_invoke(self, mocker, args):
        generate = mocker.patch("openapi_python_client.generate", return_value=[])
        result = runner.invoke(app, ["generate", "--path=openapi.json", *args])
        assert result.exit_code == 0, result.output
        return generate.call_args.kwargs["config"]

    def test_include_tags(self, mocker) -> None:
        config = self._config_from_invoke(mocker, ["--include-tags=billing,users"])
        assert config.include_tags == ["billing", "users"]
        assert config.exclude_tags == []

    def test_exclude_tags(self, mocker) -> None:
        config = self._config_from_invoke(mocker, ["--exclude-tags=admin"])
        assert config.exclude_tags == ["admin"]
        assert config.include_tags == []

    def test_include_tags_whitespace_trimmed(self, mocker) -> None:
        config = self._config_from_invoke(mocker, ["--include-tags=a, b"])
        assert config.include_tags == ["a", "b"]
        assert config.exclude_tags == []

    def test_empty_include_tags_yields_no_filter(self, mocker) -> None:
        config = self._config_from_invoke(mocker, ["--include-tags="])
        assert config.include_tags == []
        assert config.exclude_tags == []

    def test_both_flags_exits_with_error(self, mocker) -> None:
        generate = mocker.patch("openapi_python_client.generate", return_value=[])
        result = runner.invoke(
            app, ["generate", "--path=openapi.json", "--include-tags=billing", "--exclude-tags=admin"]
        )
        assert result.exit_code == 1
        assert result.output == "Provide either include_tags or exclude_tags, not both\n"
        generate.assert_not_called()

    def test_cli_overrides_config_file_value(self, mocker, tmp_path) -> None:
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps({"include_tags": ["from_config"]}))
        config = self._config_from_invoke(mocker, [f"--config={config_path}", "--include-tags=from_cli"])
        assert config.include_tags == ["from_cli"]

    def test_cli_include_with_opposite_config_exclude_errors(self, mocker, tmp_path) -> None:
        generate = mocker.patch("openapi_python_client.generate", return_value=[])
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps({"exclude_tags": ["admin"]}))
        result = runner.invoke(
            app, ["generate", "--path=openapi.json", f"--config={config_path}", "--include-tags=billing"]
        )
        assert result.exit_code == 1
        assert result.output == "Provide either include_tags or exclude_tags, not both\n"
        generate.assert_not_called()

    def test_cli_exclude_with_opposite_config_include_errors(self, mocker, tmp_path) -> None:
        generate = mocker.patch("openapi_python_client.generate", return_value=[])
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps({"include_tags": ["billing"]}))
        result = runner.invoke(
            app, ["generate", "--path=openapi.json", f"--config={config_path}", "--exclude-tags=admin"]
        )
        assert result.exit_code == 1
        assert result.output == "Provide either include_tags or exclude_tags, not both\n"
        generate.assert_not_called()

    def test_config_with_both_tags_and_no_cli_flags_errors(self, mocker, tmp_path) -> None:
        generate = mocker.patch("openapi_python_client.generate", return_value=[])
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps({"include_tags": ["billing"], "exclude_tags": ["admin"]}))
        result = runner.invoke(app, ["generate", "--path=openapi.json", f"--config={config_path}"])
        assert result.exit_code == 1
        assert result.output == "Provide either include_tags or exclude_tags, not both\n"
        generate.assert_not_called()
