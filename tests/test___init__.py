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

    from openapi_python_client import MetaType, _get_project_for_url_or_path

    project = _get_project_for_url_or_path(url=url, path=path, meta=MetaType.POETRY)

    _get_document.assert_called_once_with(url=url, path=path)
    from_dict.assert_called_once_with(data_dict)
    _Project.assert_called_once_with(openapi=openapi, custom_template_path=None, meta=MetaType.POETRY)
    assert project == _Project.return_value


def test__get_project_for_url_or_path_generator_error(mocker):
    data_dict = mocker.MagicMock()
    _get_document = mocker.patch("openapi_python_client._get_document", return_value=data_dict)
    error = GeneratorError()
    from_dict = mocker.patch("openapi_python_client.parser.GeneratorData.from_dict", return_value=error)
    _Project = mocker.patch("openapi_python_client.Project")
    url = mocker.MagicMock()
    path = mocker.MagicMock()

    from openapi_python_client import MetaType, _get_project_for_url_or_path

    project = _get_project_for_url_or_path(url=url, path=path, meta=MetaType.POETRY)

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

    from openapi_python_client import MetaType, _get_project_for_url_or_path

    project = _get_project_for_url_or_path(url=url, path=path, meta=MetaType.POETRY)

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

    from openapi_python_client import MetaType, create_new_client

    result = create_new_client(url=url, path=path, meta=MetaType.POETRY)

    _get_project_for_url_or_path.assert_called_once_with(
        url=url, path=path, custom_template_path=None, meta=MetaType.POETRY
    )
    project.build.assert_called_once()
    assert result == project.build.return_value


def test_create_new_client_project_error(mocker):
    error = GeneratorError()
    _get_project_for_url_or_path = mocker.patch(
        "openapi_python_client._get_project_for_url_or_path", return_value=error
    )
    url = mocker.MagicMock()
    path = mocker.MagicMock()

    from openapi_python_client import MetaType, create_new_client

    result = create_new_client(url=url, path=path, meta=MetaType.POETRY)

    _get_project_for_url_or_path.assert_called_once_with(
        url=url, path=path, custom_template_path=None, meta=MetaType.POETRY
    )
    assert result == [error]


def test_update_existing_client(mocker):
    project = mocker.MagicMock()
    _get_project_for_url_or_path = mocker.patch(
        "openapi_python_client._get_project_for_url_or_path", return_value=project
    )
    url = mocker.MagicMock()
    path = mocker.MagicMock()

    from openapi_python_client import MetaType, update_existing_client

    result = update_existing_client(url=url, path=path, meta=MetaType.POETRY)

    _get_project_for_url_or_path.assert_called_once_with(
        url=url, path=path, custom_template_path=None, meta=MetaType.POETRY
    )
    project.update.assert_called_once()
    assert result == project.update.return_value


def test_update_existing_client_project_error(mocker):
    error = GeneratorError()
    _get_project_for_url_or_path = mocker.patch(
        "openapi_python_client._get_project_for_url_or_path", return_value=error
    )
    url = mocker.MagicMock()
    path = mocker.MagicMock()

    from openapi_python_client import MetaType, update_existing_client

    result = update_existing_client(url=url, path=path, meta=MetaType.POETRY)

    _get_project_for_url_or_path.assert_called_once_with(
        url=url, path=path, custom_template_path=None, meta=MetaType.POETRY
    )
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

        from openapi_python_client import MetaType, Project

        project = Project(openapi=openapi, meta=MetaType.POETRY)

        assert project.openapi == openapi
        assert project.project_name == "my-test-api-client"
        assert project.package_name == "my_test_api_client"
        assert project.package_description == "A client library for accessing My Test API"
        assert project.meta == MetaType.POETRY
        assert project.project_dir == pathlib.Path.cwd() / project.project_name
        assert project.package_dir == pathlib.Path.cwd() / project.project_name / project.package_name

    def test___init___no_meta(self, mocker):
        openapi = mocker.MagicMock(title="My Test API")

        from openapi_python_client import MetaType, Project

        project = Project(openapi=openapi, meta=MetaType.NONE)

        assert project.openapi == openapi
        assert project.project_name == "my-test-api-client"
        assert project.package_name == "my_test_api_client"
        assert project.package_description == "A client library for accessing My Test API"
        assert project.meta == MetaType.NONE
        assert project.project_dir == pathlib.Path.cwd()
        assert project.package_dir == pathlib.Path.cwd() / project.package_name

    def test_project_and_package_name_overrides(self, mocker):
        openapi = mocker.MagicMock(title="My Test API")

        from openapi_python_client import MetaType, Project

        Project.project_name_override = "my-special-project-name"
        project = Project(openapi=openapi, meta=MetaType.POETRY)

        assert project.project_name == "my-special-project-name"
        assert project.package_name == "my_special_project_name"

        Project.package_name_override = "my_special_package_name"
        project = Project(openapi=openapi, meta=MetaType.POETRY)

        assert project.project_name == "my-special-project-name"
        assert project.package_name == "my_special_package_name"

    def test_build(self, mocker):
        from openapi_python_client import MetaType, Project

        project = Project(openapi=mocker.MagicMock(title="My Test API"), meta=MetaType.POETRY)
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

    def test_build_no_meta(self, mocker):
        from openapi_python_client import MetaType, Project

        project = Project(openapi=mocker.MagicMock(title="My Test API"), meta=MetaType.NONE)
        project.project_dir = mocker.MagicMock()
        project.package_dir = mocker.MagicMock()
        project._build_metadata = mocker.MagicMock()
        project._build_models = mocker.MagicMock()
        project._build_api = mocker.MagicMock()
        project._create_package = mocker.MagicMock()
        project._reformat = mocker.MagicMock()
        project._get_errors = mocker.MagicMock()

        project.build()

        project.project_dir.mkdir.assert_not_called()

    def test_build_file_exists(self, mocker):
        from openapi_python_client import MetaType, Project

        project = Project(openapi=mocker.MagicMock(title="My Test API"), meta=MetaType.POETRY)
        project.project_dir = mocker.MagicMock()
        project.project_dir.mkdir.side_effect = FileExistsError
        result = project.build()

        project.project_dir.mkdir.assert_called_once()

        assert result == [GeneratorError(detail="Directory already exists. Delete it or use the update command.")]

    def test_update(self, mocker):
        from openapi_python_client import MetaType, Project, shutil

        rmtree = mocker.patch.object(shutil, "rmtree")
        project = Project(openapi=mocker.MagicMock(title="My Test API"), meta=MetaType.POETRY)
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
        from openapi_python_client import MetaType, Project

        project = Project(openapi=mocker.MagicMock(title="My Test API"), meta=MetaType.POETRY)
        project.package_dir = mocker.MagicMock()
        project.package_dir.is_dir.return_value = False
        project._build_models = mocker.MagicMock()

        with pytest.raises(FileNotFoundError):
            project.update()

        project.package_dir.is_dir.assert_called_once()
        project._build_models.assert_not_called()

    def test__build_metadata_poetry(self, mocker):
        from openapi_python_client import MetaType, Project

        project = Project(openapi=mocker.MagicMock(title="My Test API"), meta=MetaType.POETRY)
        project._build_pyproject_toml = mocker.MagicMock()
        project.project_dir = mocker.MagicMock()
        readme_path = mocker.MagicMock(autospec=pathlib.Path)
        git_ignore_path = mocker.MagicMock(autospec=pathlib.Path)
        paths = {
            "README.md": readme_path,
            ".gitignore": git_ignore_path,
        }
        project.project_dir.__truediv__.side_effect = lambda x: paths[x]

        readme_template = mocker.MagicMock(autospec=jinja2.Template)
        git_ignore_template = mocker.MagicMock(autospec=jinja2.Template)
        project.env = mocker.MagicMock(autospec=jinja2.Environment)
        templates = {
            "README.md.jinja": readme_template,
            ".gitignore.jinja": git_ignore_template,
        }
        project.env.get_template.side_effect = lambda x: templates[x]

        project._build_metadata()

        project.env.get_template.assert_has_calls([mocker.call("README.md.jinja"), mocker.call(".gitignore.jinja")])
        readme_template.render.assert_called_once_with(
            description=project.package_description,
            project_name=project.project_name,
            package_name=project.package_name,
        )
        readme_path.write_text.assert_called_once_with(readme_template.render())
        git_ignore_template.render.assert_called_once()
        git_ignore_path.write_text.assert_called_once_with(git_ignore_template.render())
        project._build_pyproject_toml.assert_called_once_with(use_poetry=True)

    def test__build_metadata_setup(self, mocker):
        from openapi_python_client import MetaType, Project

        project = Project(openapi=mocker.MagicMock(title="My Test API"), meta=MetaType.SETUP)
        project._build_pyproject_toml = mocker.MagicMock()
        project._build_setup_py = mocker.MagicMock()
        project.project_dir = mocker.MagicMock()
        readme_path = mocker.MagicMock(autospec=pathlib.Path)
        git_ignore_path = mocker.MagicMock(autospec=pathlib.Path)
        paths = {
            "README.md": readme_path,
            ".gitignore": git_ignore_path,
        }
        project.project_dir.__truediv__.side_effect = lambda x: paths[x]

        readme_template = mocker.MagicMock(autospec=jinja2.Template)
        git_ignore_template = mocker.MagicMock(autospec=jinja2.Template)
        project.env = mocker.MagicMock(autospec=jinja2.Environment)
        templates = {
            "README.md.jinja": readme_template,
            ".gitignore.jinja": git_ignore_template,
        }
        project.env.get_template.side_effect = lambda x: templates[x]

        project._build_metadata()

        project.env.get_template.assert_has_calls([mocker.call("README.md.jinja"), mocker.call(".gitignore.jinja")])
        readme_template.render.assert_called_once_with(
            description=project.package_description,
            project_name=project.project_name,
            package_name=project.package_name,
        )
        readme_path.write_text.assert_called_once_with(readme_template.render())
        git_ignore_template.render.assert_called_once()
        git_ignore_path.write_text.assert_called_once_with(git_ignore_template.render())
        project._build_pyproject_toml.assert_called_once_with(use_poetry=False)
        project._build_setup_py.assert_called_once()

    def test__build_metadata_none(self, mocker):
        from openapi_python_client import MetaType, Project

        project = Project(openapi=mocker.MagicMock(title="My Test API"), meta=MetaType.NONE)
        project._build_pyproject_toml = mocker.MagicMock()

        project._build_metadata()

        project._build_pyproject_toml.assert_not_called()

    @pytest.mark.parametrize("use_poetry", [(True,), (False,)])
    def test__build_pyproject_toml(self, mocker, use_poetry):
        from openapi_python_client import MetaType, Project

        project = Project(openapi=mocker.MagicMock(title="My Test API"), meta=MetaType.POETRY)
        project.project_dir = mocker.MagicMock()
        pyproject_path = mocker.MagicMock(autospec=pathlib.Path)
        paths = {
            "pyproject.toml": pyproject_path,
        }
        project.project_dir.__truediv__.side_effect = lambda x: paths[x]

        pyproject_template = mocker.MagicMock(autospec=jinja2.Template)
        project.env = mocker.MagicMock(autospec=jinja2.Environment)
        template_path = "pyproject.toml.jinja" if use_poetry else "pyproject_no_poetry.toml.jinja"
        templates = {
            template_path: pyproject_template,
        }
        project.env.get_template.side_effect = lambda x: templates[x]

        project._build_pyproject_toml(use_poetry=use_poetry)

        project.env.get_template.assert_called_once_with(template_path)

        pyproject_template.render.assert_called_once_with(
            project_name=project.project_name,
            package_name=project.package_name,
            version=project.version,
            description=project.package_description,
        )
        pyproject_path.write_text.assert_called_once_with(pyproject_template.render())

    def test__build_setup_py(self, mocker):
        from openapi_python_client import MetaType, Project

        project = Project(openapi=mocker.MagicMock(title="My Test API"), meta=MetaType.SETUP)
        project.project_dir = mocker.MagicMock()
        setup_path = mocker.MagicMock(autospec=pathlib.Path)
        paths = {
            "setup.py": setup_path,
        }
        project.project_dir.__truediv__.side_effect = lambda x: paths[x]

        setup_template = mocker.MagicMock(autospec=jinja2.Template)
        project.env = mocker.MagicMock(autospec=jinja2.Environment)
        templates = {
            "setup.py.jinja": setup_template,
        }
        project.env.get_template.side_effect = lambda x: templates[x]

        project._build_setup_py()

        project.env.get_template.assert_called_once_with("setup.py.jinja")

        setup_template.render.assert_called_once_with(
            project_name=project.project_name,
            package_name=project.package_name,
            version=project.version,
            description=project.package_description,
        )
        setup_path.write_text.assert_called_once_with(setup_template.render())


def test__reformat(mocker):
    import subprocess

    from openapi_python_client import GeneratorData, MetaType, Project

    sub_run = mocker.patch("subprocess.run")
    openapi = mocker.MagicMock(autospec=GeneratorData, title="My Test API")
    project = Project(openapi=openapi, meta=MetaType.POETRY)
    project.project_dir = mocker.MagicMock(autospec=pathlib.Path)

    project._reformat()

    sub_run.assert_has_calls(
        [
            mocker.call(
                "autoflake -i -r --remove-all-unused-imports --remove-unused-variables --ignore-init-module-imports .",
                cwd=project.package_dir,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ),
            mocker.call(
                "isort .",
                cwd=project.project_dir,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ),
            mocker.call("black .", cwd=project.project_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE),
        ]
    )


def test__get_errors(mocker):
    from openapi_python_client import GeneratorData, MetaType, Project
    from openapi_python_client.parser.openapi import EndpointCollection

    openapi = mocker.MagicMock(
        autospec=GeneratorData,
        title="My Test API",
        endpoint_collections_by_tag={
            "default": mocker.MagicMock(autospec=EndpointCollection, parse_errors=[1]),
            "other": mocker.MagicMock(autospec=EndpointCollection, parse_errors=[2]),
        },
        errors=[3],
    )
    project = Project(openapi=openapi, meta=MetaType.POETRY)

    assert project._get_errors() == [1, 2, 3]


def test__custom_templates(mocker):
    from openapi_python_client import GeneratorData, MetaType, Project
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

    project = Project(openapi=openapi, meta=MetaType.POETRY)
    assert isinstance(project.env.loader, jinja2.PackageLoader)

    project = Project(
        openapi=openapi, custom_template_path="../end_to_end_tests/test_custom_templates", meta=MetaType.POETRY
    )
    assert isinstance(project.env.loader, jinja2.ChoiceLoader)
    assert len(project.env.loader.loaders) == 2
    assert isinstance(project.env.loader.loaders[0], jinja2.FileSystemLoader)
    assert isinstance(project.env.loader.loaders[1], jinja2.PackageLoader)
