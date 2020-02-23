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

    def test__build_models(self, mocker):
        from openapi_python_client import _Project, OpenAPI

        openapi = mocker.MagicMock(autospec=OpenAPI, title="My Test API")
        schema_1 = mocker.MagicMock()
        schema_2 = mocker.MagicMock()
        openapi.schemas = {"1": schema_1, "2": schema_2}
        enum_1 = mocker.MagicMock()
        enum_2 = mocker.MagicMock()
        openapi.enums = {"1": enum_1, "2": enum_2}
        project = _Project(openapi=openapi)
        project.package_dir = mocker.MagicMock()
        models_init = mocker.MagicMock()
        models_dir = mocker.MagicMock()
        schema_1_module_path = mocker.MagicMock()
        schema_2_module_path = mocker.MagicMock()
        enum_1_module_path = mocker.MagicMock()
        enum_2_module_path = mocker.MagicMock()
        module_paths = {
            "__init__.py": models_init,
            f"{schema_1.reference.module_name}.py": schema_1_module_path,
            f"{schema_2.reference.module_name}.py": schema_2_module_path,
            f"{enum_1.name}.py": enum_1_module_path,
            f"{enum_2.name}.py": enum_2_module_path,
        }
        models_dir.__truediv__.side_effect = lambda x: module_paths[x]
        project.package_dir.__truediv__.return_value = models_dir
        model_render_1 = mocker.MagicMock()
        model_render_2 = mocker.MagicMock()
        model_template = mocker.MagicMock()
        model_template.render.side_effect = [model_render_1, model_render_2]
        enum_render_1 = mocker.MagicMock()
        enum_render_2 = mocker.MagicMock()
        enum_template = mocker.MagicMock()
        enum_renders = {
            enum_1: enum_render_1,
            enum_2: enum_render_2,
        }
        enum_template.render.side_effect = lambda enum: enum_renders[enum]
        models_init_template = mocker.MagicMock()
        templates = {
            "model.pyi": model_template,
            "enum.pyi": enum_template,
            "models_init.pyi": models_init_template,
        }
        project.env = mocker.MagicMock()
        project.env.get_template.side_effect = lambda x: templates[x]
        imports = [
            "import_schema_1",
            "import_schema_2",
            "import_enum_1",
            "import_enum_2",
        ]
        import_string_from_reference = mocker.patch(
            "openapi_python_client.import_string_from_reference", side_effect=imports
        )

        project._build_models()

        project.package_dir.__truediv__.assert_called_once_with("models")
        models_dir.mkdir.assert_called_once()
        models_dir.__truediv__.assert_has_calls([mocker.call(key) for key in module_paths])
        project.env.get_template.assert_has_calls([mocker.call(key) for key in templates])
        model_template.render.assert_has_calls([mocker.call(schema=schema_1), mocker.call(schema=schema_2)])
        schema_1_module_path.write_text.assert_called_once_with(model_render_1)
        schema_2_module_path.write_text.assert_called_once_with(model_render_2)
        import_string_from_reference.assert_has_calls(
            [
                mocker.call(schema_1.reference),
                mocker.call(schema_2.reference),
                mocker.call(enum_1.reference),
                mocker.call(enum_2.reference),
            ]
        )
        models_init_template.render.assert_called_once_with(imports=imports)
        enum_1_module_path.write_text.assert_called_once_with(enum_render_1)
        enum_2_module_path.write_text.assert_called_once_with(enum_render_2)

    def test__build_api(self, mocker):
        import pathlib
        from openapi_python_client import _Project, OpenAPI

        openapi = mocker.MagicMock(autospec=OpenAPI, title="My Test API")
        tag_1 = mocker.MagicMock(autospec=str)
        tag_2 = mocker.MagicMock(autospec=str)
        collection_1 = mocker.MagicMock()
        collection_2 = mocker.MagicMock()
        openapi.endpoint_collections_by_tag = {tag_1: collection_1, tag_2: collection_2}
        project = _Project(openapi=openapi)
        project.package_dir = mocker.MagicMock()
        client_path = mocker.MagicMock()
        api_init = mocker.MagicMock(autospec=pathlib.Path)
        collection_1_path = mocker.MagicMock(autospec=pathlib.Path)
        collection_2_path = mocker.MagicMock(autospec=pathlib.Path)
        api_paths = {
            "__init__.py": api_init,
            f"{tag_1}.py": collection_1_path,
            f"{tag_2}.py": collection_2_path,
        }
        api_dir = mocker.MagicMock(autospec=pathlib.Path)
        api_dir.__truediv__.side_effect = lambda x: api_paths[x]
        package_paths = {
            "client.py": client_path,
            "api": api_dir,
        }
        project.package_dir.__truediv__.side_effect = lambda x: package_paths[x]
        client_template = mocker.MagicMock()
        endpoint_template = mocker.MagicMock()
        templates = {
            "client.pyi": client_template,
            "endpoint_module.pyi": endpoint_template,
        }
        mocker.patch.object(project.env, "get_template", autospec=True, side_effect=lambda x: templates[x])
        endpoint_renders = {
            collection_1: mocker.MagicMock(),
            collection_2: mocker.MagicMock(),
        }
        endpoint_template.render.side_effect = lambda collection: endpoint_renders[collection]

        project._build_api()

        project.package_dir.__truediv__.assert_has_calls([mocker.call(key) for key in package_paths])
        project.env.get_template.assert_has_calls([mocker.call(key) for key in templates])
        client_template.render.assert_called_once()
        client_path.write_text.assert_called_once_with(client_template.render())
        api_dir.mkdir.assert_called_once()
        api_dir.__truediv__.assert_has_calls([mocker.call(key) for key in api_paths])
        api_init.write_text.assert_called_once_with('""" Contains all methods for accessing the API """')
        endpoint_template.render.assert_has_calls(
            [mocker.call(collection=collection_1), mocker.call(collection=collection_2),]
        )
        collection_1_path.write_text.assert_called_once_with(endpoint_renders[collection_1])
        collection_2_path.write_text.assert_called_once_with(endpoint_renders[collection_2])
