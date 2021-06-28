def test_main(mocker):
    app = mocker.patch("openapi_python_client.cli.app")

    # noinspection PyUnresolvedReferences
    from openapi_python_client import __main__

    app.assert_called_once()
