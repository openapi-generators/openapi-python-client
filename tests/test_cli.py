import pytest
import typer


def test_callback():
    from openapi_python_client.cli import cli

    cli()


class TestGenerate:
    def test_generate_no_params(self, mocker):
        create_new_client = mocker.patch("openapi_python_client.create_new_client")
        from openapi_python_client.cli import generate

        with pytest.raises(typer.Exit) as exc_info:
            generate(url=None, path=None)
            assert exc_info.value.exit_code == 1
        create_new_client.assert_not_called()

    def test_generate_url_and_path(self, mocker):
        create_new_client = mocker.patch("openapi_python_client.create_new_client")
        from openapi_python_client.cli import generate

        with pytest.raises(typer.Exit) as exc_info:
            generate(url="blah", path="other_blah")
            assert exc_info.value.exit_code == 1
        create_new_client.assert_not_called()

    def test_generate_url(self, mocker):
        create_new_client = mocker.patch("openapi_python_client.create_new_client")
        url = mocker.MagicMock()
        from openapi_python_client.cli import generate

        generate(url=url, path=None)

        create_new_client.assert_called_once_with(url=url, path=None)

    def test_generate_path(self, mocker):
        create_new_client = mocker.patch("openapi_python_client.create_new_client")
        path = mocker.MagicMock()
        from openapi_python_client.cli import generate

        generate(url=None, path=path)

        create_new_client.assert_called_once_with(url=None, path=path)


class TestUpdate:
    def test_update_no_params(self, mocker):
        update_existing_client = mocker.patch("openapi_python_client.update_existing_client")
        from openapi_python_client.cli import update

        with pytest.raises(typer.Exit) as exc_info:
            update(url=None, path=None)
            assert exc_info.value.exit_code == 1
        update_existing_client.assert_not_called()

    def test_update_url_and_path(self, mocker):
        update_existing_client = mocker.patch("openapi_python_client.update_existing_client")
        from openapi_python_client.cli import update

        with pytest.raises(typer.Exit) as exc_info:
            update(url="blah", path="other_blah")
            assert exc_info.value.exit_code == 1
        update_existing_client.assert_not_called()

    def test_update_url(self, mocker):
        update_existing_client = mocker.patch("openapi_python_client.update_existing_client")
        url = mocker.MagicMock()
        from openapi_python_client.cli import update

        update(url=url, path=None)

        update_existing_client.assert_called_once_with(url=url, path=None)

    def test_update_path(self, mocker):
        update_existing_client = mocker.patch("openapi_python_client.update_existing_client")
        path = mocker.MagicMock()
        from openapi_python_client.cli import update

        update(url=None, path=path)

        update_existing_client.assert_called_once_with(url=None, path=path)
