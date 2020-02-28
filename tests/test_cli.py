import pytest
import typer


def test_generate_no_params(mocker):
    main = mocker.patch("openapi_python_client.cli.main")
    from openapi_python_client.cli import generate

    with pytest.raises(typer.Exit) as exc_info:
        generate()
        assert exc_info.value.exit_code == 1
    main.assert_not_called()


def test_generate_url_and_path(mocker):
    main = mocker.patch("openapi_python_client.cli.main")
    from openapi_python_client.cli import generate

    with pytest.raises(typer.Exit) as exc_info:
        generate(url="blah", path="other_blah")
        assert exc_info.value.exit_code == 1
    main.assert_not_called()


def test_generate_url(mocker):
    main = mocker.patch("openapi_python_client.cli.main")
    url = mocker.MagicMock()
    from openapi_python_client.cli import generate

    generate(url=url, path=None)

    main.assert_called_once_with(url=url, path=None)


def test_generate_path(mocker):
    main = mocker.patch("openapi_python_client.cli.main")
    path = mocker.MagicMock()
    from openapi_python_client.cli import generate

    generate(url=None, path=path)

    main.assert_called_once_with(url=None, path=path)
