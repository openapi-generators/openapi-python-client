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
