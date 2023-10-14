def test_main(mocker):
    app = mocker.patch("openapi_python_client.cli.app")

    from openapi_python_client import __main__  # noqa: F401

    app.assert_called_once()
