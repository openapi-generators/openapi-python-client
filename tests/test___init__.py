import pytest


def test_main(mocker):
    data_dict = mocker.MagicMock()
    _get_json = mocker.patch("openapi_python_client._get_json", return_value=data_dict)
    openapi = mocker.MagicMock()
    from_dict = mocker.patch("openapi_python_client.openapi_parser.OpenAPI.from_dict", return_value=openapi)
    _Project = mocker.patch("openapi_python_client._Project")
    url = mocker.MagicMock()
    path = mocker.MagicMock()

    from openapi_python_client import main

    main(url=url, path=path)

    _get_json.assert_called_once_with(url=url, path=path)
    from_dict.assert_called_once_with(data_dict)
    _Project.assert_called_once_with(openapi=openapi)
    _Project().build.assert_called_once()


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


class TestProject:
    def test___init__(self, mocker):
        openapi = mocker.MagicMock(title="My Test API")

        from openapi_python_client import _Project

        project = _Project(openapi=openapi)

        assert project.openapi == openapi
        assert project.project_name == "my-test-api-client"
        assert project.package_name == "my_test_api_client"

    def test_build(self, mocker):
        from openapi_python_client import _Project

        project = _Project(openapi=mocker.MagicMock(title="My Test API"))
        project.project_dir = mocker.MagicMock()
        project.package_dir = mocker.MagicMock()
        project._build_metadata = mocker.MagicMock()
        project._build_models = mocker.MagicMock()
        project._build_api = mocker.MagicMock()

        project.build()

        project.project_dir.mkdir.assert_called_once()
        project.package_dir.mkdir.assert_called_once()
        project._build_metadata.assert_called_once()
        project._build_models.assert_called_once()
        project._build_api.assert_called_once()

    def test__build_metadata(self, mocker):
        from openapi_python_client import _Project

        project = _Project(openapi=mocker.MagicMock(title="My Test API"))
        project.project_dir = mocker.MagicMock()
        pyproject_path = mocker.MagicMock()
        readme_path = mocker.MagicMock()
        project.project_dir.__truediv__.side_effect = [pyproject_path, readme_path]
        project.package_dir = mocker.MagicMock()
        package_init_template = mocker.MagicMock()
        pyproject_template = mocker.MagicMock()
        readme_template = mocker.MagicMock()
        project.env = mocker.MagicMock()
        project.env.get_template.side_effect = [package_init_template, pyproject_template, readme_template]

        project._build_metadata()

        project.env.get_template.assert_has_calls(
            [mocker.call("package_init.pyi"), mocker.call("pyproject.toml"), mocker.call("README.md"),]
        )
        description = f"A client library for accessing {project.openapi.title}"
        package_init = project.package_dir / "__init__.py"
        package_init_template.render.assert_called_once_with(description=description)
        package_init.write_text.assert_called_once_with(package_init_template.render())
        pyproject_template.render.assert_called_once_with(
            project_name=project.project_name, package_name=project.package_name, description=description
        )
        pyproject_path.write_text.assert_called_once_with(pyproject_template.render())
        readme_template.render.assert_called_once_with(description=description)
        readme_path.write_text.assert_called_once_with(readme_template.render())

    def test__build_models(self):
        assert False

    def test__build_api(self):
        assert False
