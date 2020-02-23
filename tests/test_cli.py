from click.testing import CliRunner


def test_generate_no_params(mocker):
    main = mocker.patch("openapi_python_client.cli.main")
    from openapi_python_client.cli import generate

    runner = CliRunner()
    result = runner.invoke(generate)

    assert result.exit_code == 1
    assert result.output == "You must either provide --url or --path\n"
    main.assert_not_called()


def test_generate_url_and_path(mocker):
    main = mocker.patch("openapi_python_client.cli.main")
    from openapi_python_client.cli import generate

    runner = CliRunner()
    result = runner.invoke(generate, ["--url=blah", "--path=blahblah"])

    assert result.exit_code == 1
    assert result.output == "Provide either --url or --path, not both\n"
    main.assert_not_called()


def test_generate_url(mocker):
    main = mocker.patch("openapi_python_client.cli.main")
    url = mocker.MagicMock()
    from openapi_python_client.cli import generate

    runner = CliRunner()
    result = runner.invoke(generate, [f"--url={url}"])

    assert result.exit_code == 0
    main.assert_called_once_with(url=str(url), path=None)


def test_generate_path(mocker):
    main = mocker.patch("openapi_python_client.cli.main")
    path = mocker.MagicMock()
    from openapi_python_client.cli import generate

    runner = CliRunner()
    result = runner.invoke(generate, [f"--path={path}"])

    assert result.exit_code == 0
    main.assert_called_once_with(path=str(path), url=None)


def test_version():
    from importlib.metadata import version
    from openapi_python_client.cli import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])

    assert result.exit_code == 0
    assert result.output == f"OpenAPI Python Client, version {version('openapi-python-client')}\n"
