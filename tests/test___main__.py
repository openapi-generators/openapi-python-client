def test_main(mocker):
    cli = mocker.patch("openapi_python_client.cli.cli")

    # noinspection PyUnresolvedReferences
    from openapi_python_client import __main__

    cli.assert_called_once()
