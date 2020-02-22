import pytest


def test_main(mocker):
    data_dict = mocker.MagicMock()
    _get_json = mocker.patch("openapi_python_client._get_json", return_value=data_dict)
    openapi = mocker.MagicMock()
    from_dict = mocker.patch("openapi_python_client.openapi_parser.OpenAPI.from_dict", return_value=openapi)
    _build_project = mocker.patch("openapi_python_client._build_project")
    url = mocker.MagicMock()
    path = mocker.MagicMock()

    from openapi_python_client import main

    main(url=url, path=path)

    _get_json.assert_called_once_with(url=url, path=path)
    from_dict.assert_called_once_with(data_dict)
    _build_project.assert_called_once_with(openapi=openapi)


class TestGetJson:
    def test__get_json_no_url_or_path(self, mocker):
        get = mocker.patch("requests.get")
        Path = mocker.patch("openapi_python_client.Path")
        loads = mocker.patch("json.loads")

        from openapi_python_client import _get_json

        with pytest.raises(ValueError):
            _get_json(url=None, path=None)

        get.assert_not_called()
        Path.assert_not_called()
        loads.assert_not_called()

    def test__get_json_url_and_path(self, mocker):
        get = mocker.patch("requests.get")
        Path = mocker.patch("openapi_python_client.Path")
        loads = mocker.patch("json.loads")

        from openapi_python_client import _get_json

        with pytest.raises(ValueError):
            _get_json(url=mocker.MagicMock(), path=mocker.MagicMock())

        get.assert_not_called()
        Path.assert_not_called()
        loads.assert_not_called()

    def test__get_json_url_no_path(self, mocker):
        get = mocker.patch("requests.get")
        Path = mocker.patch("openapi_python_client.Path")
        loads = mocker.patch("json.loads")

        from openapi_python_client import _get_json

        url = mocker.MagicMock()
        _get_json(url=url, path=None)

        get.assert_called_once_with(url)
        Path.assert_not_called()
        loads.assert_called_once_with(get().content)

    def test__get_json_path_no_url(self, mocker):
        get = mocker.patch("requests.get")
        Path = mocker.patch("openapi_python_client.Path")
        loads = mocker.patch("json.loads")

        from openapi_python_client import _get_json

        path = mocker.MagicMock()
        _get_json(url=None, path=path)

        get.assert_not_called()
        Path.assert_called_once_with(path)
        loads.assert_called_once_with(Path().read_bytes())
