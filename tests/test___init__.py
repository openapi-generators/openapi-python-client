import pathlib

import httpcore
import jinja2
import pytest
import yaml

from openapi_python_client import GeneratorError


def test__get_project_for_url_or_path(mocker):
    data_dict = mocker.MagicMock()
    _get_document = mocker.patch("openapi_python_client._get_document", return_value=data_dict)
    openapi = mocker.MagicMock()
    from_dict = mocker.patch("openapi_python_client.parser.GeneratorData.from_dict", return_value=openapi)
    _Project = mocker.patch("openapi_python_client.Project")
    url = mocker.MagicMock()
    path = mocker.MagicMock()

    from openapi_python_client import _get_project_for_url_or_path

    project = _get_project_for_url_or_path(url=url, path=path)

    _get_document.assert_called_once_with(url=url, path=path)
    from_dict.assert_called_once_with(data_dict)
    _Project.assert_called_once_with(openapi=openapi)
    assert project == _Project()


def test__get_project_for_url_or_path_generator_error(mocker):
    data_dict = mocker.MagicMock()
    _get_document = mocker.patch("openapi_python_client._get_document", return_value=data_dict)
    error = GeneratorError()
    from_dict = mocker.patch("openapi_python_client.parser.GeneratorData.from_dict", return_value=error)
    _Project = mocker.patch("openapi_python_client.Project")
    url = mocker.MagicMock()
    path = mocker.MagicMock()

    from openapi_python_client import _get_project_for_url_or_path

    project = _get_project_for_url_or_path(url=url, path=path)

    _get_document.assert_called_once_with(url=url, path=path)
    from_dict.assert_called_once_with(data_dict)
    _Project.assert_not_called()
    assert project == error


def test__get_project_for_url_or_path_document_error(mocker):
    error = GeneratorError()
    _get_document = mocker.patch("openapi_python_client._get_document", return_value=error)

    from_dict = mocker.patch("openapi_python_client.parser.GeneratorData.from_dict")
    url = mocker.MagicMock()
    path = mocker.MagicMock()

    from openapi_python_client import _get_project_for_url_or_path

    project = _get_project_for_url_or_path(url=url, path=path)

    _get_document.assert_called_once_with(url=url, path=path)
    from_dict.assert_not_called()
    assert project == error


def test_create_new_client(mocker):
    project = mocker.MagicMock()
    _get_project_for_url_or_path = mocker.patch(
        "openapi_python_client._get_project_for_url_or_path", return_value=project
    )
    url = mocker.MagicMock()
    path = mocker.MagicMock()

    from openapi_python_client import create_new_client

    result = create_new_client(url=url, path=path)

    _get_project_for_url_or_path.assert_called_once_with(url=url, path=path)
    project.build.assert_called_once()
    assert result == project.build.return_value


def test_create_new_client_project_error(mocker):
    error = GeneratorError()
    _get_project_for_url_or_path = mocker.patch(
        "openapi_python_client._get_project_for_url_or_path", return_value=error
    )
    url = mocker.MagicMock()
    path = mocker.MagicMock()

    from openapi_python_client import create_new_client

    result = create_new_client(url=url, path=path)

    _get_project_for_url_or_path.assert_called_once_with(url=url, path=path)
    assert result == [error]


def test_update_existing_client(mocker):
    project = mocker.MagicMock()
    _get_project_for_url_or_path = mocker.patch(
        "openapi_python_client._get_project_for_url_or_path", return_value=project
    )
    url = mocker.MagicMock()
    path = mocker.MagicMock()

    from openapi_python_client import update_existing_client

    result = update_existing_client(url=url, path=path)

    _get_project_for_url_or_path.assert_called_once_with(url=url, path=path)
    project.update.assert_called_once()
    assert result == project.update.return_value


def test_update_existing_client_project_error(mocker):
    error = GeneratorError()
    _get_project_for_url_or_path = mocker.patch(
        "openapi_python_client._get_project_for_url_or_path", return_value=error
    )
    url = mocker.MagicMock()
    path = mocker.MagicMock()

    from openapi_python_client import update_existing_client

    result = update_existing_client(url=url, path=path)

    _get_project_for_url_or_path.assert_called_once_with(url=url, path=path)
    assert result == [error]


class TestGetJson:
    def test__get_document_no_url_or_path(self, mocker):
        get = mocker.patch("httpx.get")
        Path = mocker.patch("openapi_python_client.Path")
        loads = mocker.patch("yaml.safe_load")

        from openapi_python_client import _get_document

        result = _get_document(url=None, path=None)

        assert result == GeneratorError(header="No URL or Path provided")
        get.assert_not_called()
        Path.assert_not_called()
        loads.assert_not_called()

    def test__get_document_url_and_path(self, mocker):
        get = mocker.patch("httpx.get")
        Path = mocker.patch("openapi_python_client.Path")
        loads = mocker.patch("yaml.safe_load")

        from openapi_python_client import _get_document

        result = _get_document(url=mocker.MagicMock(), path=mocker.MagicMock())

        assert result == GeneratorError(header="Provide URL or Path, not both.")
        get.assert_not_called()
        Path.assert_not_called()
        loads.assert_not_called()

    def test__get_document_bad_url(self, mocker):
        get = mocker.patch("httpx.get", side_effect=httpcore.NetworkError)
        Path = mocker.patch("openapi_python_client.Path")
        loads = mocker.patch("yaml.safe_load")

        from openapi_python_client import _get_document

        url = mocker.MagicMock()
        result = _get_document(url=url, path=None)

        assert result == GeneratorError(header="Could not get OpenAPI document from provided URL")
        get.assert_called_once_with(url)
        Path.assert_not_called()
        loads.assert_not_called()

    def test__get_document_url_no_path(self, mocker):
        get = mocker.patch("httpx.get")
        Path = mocker.patch("openapi_python_client.Path")
        loads = mocker.patch("yaml.safe_load")

        from openapi_python_client import _get_document

        url = mocker.MagicMock()
        _get_document(url=url, path=None)

        get.assert_called_once_with(url)
        Path.assert_not_called()
        loads.assert_called_once_with(get().content)

    def test__get_document_path_no_url(self, mocker):
        get = mocker.patch("httpx.get")
        loads = mocker.patch("yaml.safe_load")

        from openapi_python_client import _get_document

        path = mocker.MagicMock()
        _get_document(url=None, path=path)

        get.assert_not_called()
        path.read_bytes.assert_called_once()
        loads.assert_called_once_with(path.read_bytes())

    def test__get_document_bad_yaml(self, mocker):
        get = mocker.patch("httpx.get")
        loads = mocker.patch("yaml.safe_load", side_effect=yaml.YAMLError)

        from openapi_python_client import _get_document

        path = mocker.MagicMock()
        result = _get_document(url=None, path=path)

        get.assert_not_called()
        path.read_bytes.assert_called_once()
        loads.assert_called_once_with(path.read_bytes())
        assert result == GeneratorError(header="Invalid YAML from provided source")


class TestProject:
    def test___init__(self, mocker):
        openapi = mocker.MagicMock(title="My Test API")

        from openapi_python_client import Project

        project = Project(openapi=openapi)

        assert project.openapi == openapi
        assert project.project_name == "my-test-api-client"
        assert project.package_name == "my_test_api_client"
        assert project.package_description == "A client library for accessing My Test API"

    def test_project_and_package_name_overrides(self, mocker):
        openapi = mocker.MagicMock(title="My Test API")

        from openapi_python_client import Project

        Project.project_name_override = "my-special-project-name"
        project = Project(openapi=openapi)

        assert project.project_name == "my-special-project-name"
        assert project.package_name == "my_special_project_name"

        Project.package_name_override = "my_special_package_name"
        project = Project(openapi=openapi)

        assert project.project_name == "my-special-project-name"
        assert project.package_name == "my_special_package_name"

    def test_build(self, mocker):
        from openapi_python_client import Project

        project = Project(openapi=mocker.MagicMock(title="My Test API"))
        project.project_dir = mocker.MagicMock()
        project.package_dir = mocker.MagicMock()
        project._build_metadata = mocker.MagicMock()
        project._build_models = mocker.MagicMock()
        project._build_api = mocker.MagicMock()
        project._create_package = mocker.MagicMock()
        project._reformat = mocker.MagicMock()
        project._get_errors = mocker.MagicMock()

        result = project.build()

        project.project_dir.mkdir.assert_called_once()
        project._create_package.assert_called_once()
        project._build_metadata.assert_called_once()
        project._build_models.assert_called_once()
        project._build_api.assert_called_once()
        project._reformat.assert_called_once()
        project._get_errors.assert_called_once()
        assert result == project._get_errors.return_value

    def test_build_file_exists(self, mocker):
        from openapi_python_client import Project

        project = Project(openapi=mocker.MagicMock(title="My Test API"))
        project.project_dir = mocker.MagicMock()
        project.project_dir.mkdir.side_effect = FileExistsError
        result = project.build()

        project.project_dir.mkdir.assert_called_once()

        assert result == [GeneratorError(detail="Directory already exists. Delete it or use the update command.")]

    def test_update(self, mocker):
        from openapi_python_client import Project, shutil

        rmtree = mocker.patch.object(shutil, "rmtree")
        project = Project(openapi=mocker.MagicMock(title="My Test API"))
        project.package_dir = mocker.MagicMock()
        project._build_metadata = mocker.MagicMock()
        project._build_models = mocker.MagicMock()
        project._build_api = mocker.MagicMock()
        project._create_package = mocker.MagicMock()
        project._reformat = mocker.MagicMock()
        project._get_errors = mocker.MagicMock()

        result = project.update()

        rmtree.assert_called_once_with(project.package_dir)
        project._create_package.assert_called_once()
        project._build_models.assert_called_once()
        project._build_api.assert_called_once()
        project._reformat.assert_called_once()
        project._get_errors.assert_called_once()
        assert result == project._get_errors.return_value

    def test_update_missing_dir(self, mocker):
        from openapi_python_client import Project

        project = Project(openapi=mocker.MagicMock(title="My Test API"))
        project.package_dir = mocker.MagicMock()
        project.package_dir.is_dir.return_value = False
        project._build_models = mocker.MagicMock()

        with pytest.raises(FileNotFoundError):
            project.update()

        project.package_dir.is_dir.assert_called_once()
        project._build_models.assert_not_called()

    def test__create_package(self, mocker):
        from openapi_python_client import Project

        project = Project(openapi=mocker.MagicMock(title="My Test API"))
        project.package_dir = mocker.MagicMock()
        package_init_template = mocker.MagicMock()
        project.env = mocker.MagicMock()
        project.env.get_template.return_value = package_init_template
        package_init_path = mocker.MagicMock(autospec=pathlib.Path)
        pytyped_path = mocker.MagicMock(autospec=pathlib.Path)
        paths = {
            "__init__.py": package_init_path,
            "py.typed": pytyped_path,
        }

        project.package_dir.__truediv__.side_effect = lambda x: paths[x]

        project._create_package()

        project.package_dir.mkdir.assert_called_once()
        project.env.get_template.assert_called_once_with("package_init.pyi")
        package_init_template.render.assert_called_once_with(description=project.package_description)
        package_init_path.write_text.assert_called_once_with(package_init_template.render())
        pytyped_path.write_text.assert_called_once_with("# Marker file for PEP 561")

    def test__build_metadata(self, mocker):
        from openapi_python_client import Project

        project = Project(openapi=mocker.MagicMock(title="My Test API"))
        project.project_dir = mocker.MagicMock()
        pyproject_path = mocker.MagicMock(autospec=pathlib.Path)
        readme_path = mocker.MagicMock(autospec=pathlib.Path)
        git_ignore_path = mocker.MagicMock(autospec=pathlib.Path)
        paths = {
            "pyproject.toml": pyproject_path,
            "README.md": readme_path,
            ".gitignore": git_ignore_path,
        }
        project.project_dir.__truediv__.side_effect = lambda x: paths[x]

        pyproject_template = mocker.MagicMock(autospec=jinja2.Template)
        readme_template = mocker.MagicMock(autospec=jinja2.Template)
        git_ignore_template = mocker.MagicMock(autospec=jinja2.Template)
        project.env = mocker.MagicMock(autospec=jinja2.Environment)
        templates = {
            "pyproject.toml": pyproject_template,
            "README.md": readme_template,
            ".gitignore": git_ignore_template,
        }
        project.env.get_template.side_effect = lambda x: templates[x]

        project._build_metadata()

        project.env.get_template.assert_has_calls(
            [mocker.call("pyproject.toml"), mocker.call("README.md"), mocker.call(".gitignore")]
        )

        pyproject_template.render.assert_called_once_with(
            project_name=project.project_name,
            package_name=project.package_name,
            version=project.version,
            description=project.package_description,
        )
        pyproject_path.write_text.assert_called_once_with(pyproject_template.render())
        readme_template.render.assert_called_once_with(
            description=project.package_description,
            project_name=project.project_name,
            package_name=project.package_name,
        )
        readme_path.write_text.assert_called_once_with(readme_template.render())
        git_ignore_template.render.assert_called_once()
        git_ignore_path.write_text.assert_called_once_with(git_ignore_template.render())

    def test__build_models(self, mocker):
        from openapi_python_client import GeneratorData, Project

        openapi = mocker.MagicMock(autospec=GeneratorData, title="My Test API")
        model_1 = mocker.MagicMock()
        model_2 = mocker.MagicMock()
        openapi.schemas.models = {"1": model_1, "2": model_2}
        enum_1 = mocker.MagicMock()
        enum_2 = mocker.MagicMock()
        openapi.enums = {"1": enum_1, "2": enum_2}
        project = Project(openapi=openapi)
        project.package_dir = mocker.MagicMock()
        models_init = mocker.MagicMock()
        types_py = mocker.MagicMock()
        models_dir = mocker.MagicMock()
        model_1_module_path = mocker.MagicMock()
        model_2_module_path = mocker.MagicMock()
        enum_1_module_path = mocker.MagicMock()
        enum_2_module_path = mocker.MagicMock()
        module_paths = {
            "__init__.py": models_init,
            "types.py": types_py,
            f"{model_1.reference.module_name}.py": model_1_module_path,
            f"{model_2.reference.module_name}.py": model_2_module_path,
            f"{enum_1.reference.module_name}.py": enum_1_module_path,
            f"{enum_2.reference.module_name}.py": enum_2_module_path,
        }

        def models_dir_get(x):
            return module_paths[x]

        models_dir.__truediv__.side_effect = models_dir_get
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
        types_template = mocker.MagicMock()
        templates = {
            "types.py": types_template,
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
        model_template.render.assert_has_calls([mocker.call(model=model_1), mocker.call(model=model_2)])
        model_1_module_path.write_text.assert_called_once_with(model_render_1)
        model_2_module_path.write_text.assert_called_once_with(model_render_2)
        import_string_from_reference.assert_has_calls(
            [
                mocker.call(model_1.reference),
                mocker.call(model_2.reference),
                mocker.call(enum_1.reference),
                mocker.call(enum_2.reference),
            ]
        )
        models_init_template.render.assert_called_once_with(imports=imports)
        types_template.render.assert_called_once()
        enum_1_module_path.write_text.assert_called_once_with(enum_render_1)
        enum_2_module_path.write_text.assert_called_once_with(enum_render_2)

    def test__build_api(self, mocker):
        import pathlib

        from jinja2 import Template

        from openapi_python_client import GeneratorData, Project

        openapi = mocker.MagicMock(autospec=GeneratorData, title="My Test API")
        tag_1 = mocker.MagicMock(autospec=str)
        tag_2 = mocker.MagicMock(autospec=str)
        collection_1 = mocker.MagicMock()
        collection_2 = mocker.MagicMock()
        openapi.endpoint_collections_by_tag = {tag_1: collection_1, tag_2: collection_2}
        project = Project(openapi=openapi)
        project.package_dir = mocker.MagicMock()
        api_errors = mocker.MagicMock(autospec=pathlib.Path)
        client_path = mocker.MagicMock()
        api_init = mocker.MagicMock(autospec=pathlib.Path)
        collection_1_path = mocker.MagicMock(autospec=pathlib.Path)
        collection_2_path = mocker.MagicMock(autospec=pathlib.Path)
        async_api_init = mocker.MagicMock(autospec=pathlib.Path)
        async_collection_1_path = mocker.MagicMock(autospec=pathlib.Path)
        async_collection_2_path = mocker.MagicMock(autospec=pathlib.Path)
        api_paths = {
            "__init__.py": api_init,
            f"{tag_1}.py": collection_1_path,
            f"{tag_2}.py": collection_2_path,
        }
        async_api_paths = {
            "__init__.py": async_api_init,
            f"{tag_1}.py": async_collection_1_path,
            f"{tag_2}.py": async_collection_2_path,
        }
        api_dir = mocker.MagicMock(autospec=pathlib.Path)
        api_dir.__truediv__.side_effect = lambda x: api_paths[x]
        async_api_dir = mocker.MagicMock(autospec=pathlib.Path)
        async_api_dir.__truediv__.side_effect = lambda x: async_api_paths[x]

        package_paths = {
            "client.py": client_path,
            "api": api_dir,
            "async_api": async_api_dir,
            "errors.py": api_errors,
        }
        project.package_dir.__truediv__.side_effect = lambda x: package_paths[x]
        client_template = mocker.MagicMock(autospec=Template)
        errors_template = mocker.MagicMock(autospec=Template)
        endpoint_template = mocker.MagicMock(autospec=Template)
        async_endpoint_template = mocker.MagicMock(autospec=Template)
        templates = {
            "client.pyi": client_template,
            "errors.pyi": errors_template,
            "endpoint_module.pyi": endpoint_template,
            "async_endpoint_module.pyi": async_endpoint_template,
        }
        mocker.patch.object(project.env, "get_template", autospec=True, side_effect=lambda x: templates[x])
        endpoint_renders = {
            collection_1: mocker.MagicMock(),
            collection_2: mocker.MagicMock(),
        }
        endpoint_template.render.side_effect = lambda collection: endpoint_renders[collection]
        async_endpoint_renders = {
            collection_1: mocker.MagicMock(),
            collection_2: mocker.MagicMock(),
        }
        async_endpoint_template.render.side_effect = lambda collection: async_endpoint_renders[collection]

        project._build_api()

        project.package_dir.__truediv__.assert_has_calls([mocker.call(key) for key in package_paths])
        project.env.get_template.assert_has_calls([mocker.call(key) for key in templates])
        client_template.render.assert_called_once()
        client_path.write_text.assert_called_once_with(client_template.render())
        errors_template.render.assert_called_once()
        api_errors.write_text.assert_called_once_with(errors_template.render())
        api_dir.mkdir.assert_called_once()
        api_dir.__truediv__.assert_has_calls([mocker.call(key) for key in api_paths])
        api_init.write_text.assert_called_once_with('""" Contains synchronous methods for accessing the API """')
        endpoint_template.render.assert_has_calls(
            [mocker.call(collection=collection_1), mocker.call(collection=collection_2)]
        )
        collection_1_path.write_text.assert_called_once_with(endpoint_renders[collection_1])
        collection_2_path.write_text.assert_called_once_with(endpoint_renders[collection_2])
        async_api_dir.mkdir.assert_called_once()
        async_api_dir.__truediv__.assert_has_calls([mocker.call(key) for key in async_api_paths])
        async_api_init.write_text.assert_called_once_with('""" Contains async methods for accessing the API """')
        async_endpoint_template.render.assert_has_calls(
            [mocker.call(collection=collection_1), mocker.call(collection=collection_2)]
        )
        async_collection_1_path.write_text.assert_called_once_with(async_endpoint_renders[collection_1])
        async_collection_2_path.write_text.assert_called_once_with(async_endpoint_renders[collection_2])


def test__reformat(mocker):
    import subprocess

    from openapi_python_client import GeneratorData, Project

    sub_run = mocker.patch("subprocess.run")
    openapi = mocker.MagicMock(autospec=GeneratorData, title="My Test API")
    project = Project(openapi=openapi)
    project.project_dir = mocker.MagicMock(autospec=pathlib.Path)

    project._reformat()

    sub_run.assert_has_calls(
        [
            mocker.call(
                "isort .", cwd=project.project_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            ),
            mocker.call("black .", cwd=project.project_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE),
        ]
    )


def test__get_errors(mocker):
    from openapi_python_client import GeneratorData, Project
    from openapi_python_client.parser.openapi import EndpointCollection, Schemas

    openapi = mocker.MagicMock(
        autospec=GeneratorData,
        title="My Test API",
        endpoint_collections_by_tag={
            "default": mocker.MagicMock(autospec=EndpointCollection, parse_errors=[1]),
            "other": mocker.MagicMock(autospec=EndpointCollection, parse_errors=[2]),
        },
        schemas=mocker.MagicMock(autospec=Schemas, errors=[3]),
    )
    project = Project(openapi=openapi)

    assert project._get_errors() == [1, 2, 3]
