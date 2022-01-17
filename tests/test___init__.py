import pathlib

import httpcore
import jinja2
import pytest
from pytest_mock import MockFixture

from openapi_python_client import Config, ErrorLevel, GeneratorError, Project


def test__get_project_for_url_or_path(mocker):
    data_dict = mocker.MagicMock()
    _get_document = mocker.patch("openapi_python_client._get_document", return_value=data_dict)
    openapi = mocker.MagicMock()
    from_dict = mocker.patch("openapi_python_client.parser.GeneratorData.from_dict", return_value=openapi)
    _Project = mocker.patch("openapi_python_client.Project")
    url = mocker.MagicMock()
    path = mocker.MagicMock()
    config = mocker.MagicMock()

    from openapi_python_client import MetaType, _get_project_for_url_or_path

    project = _get_project_for_url_or_path(url=url, path=path, meta=MetaType.POETRY, config=config)

    _get_document.assert_called_once_with(url=url, path=path)
    from_dict.assert_called_once_with(data_dict, config=config)
    _Project.assert_called_once_with(
        openapi=openapi, custom_template_path=None, meta=MetaType.POETRY, file_encoding="utf-8", config=config
    )
    assert project == _Project.return_value


def test__get_project_for_url_or_path_generator_error(mocker):
    data_dict = mocker.MagicMock()
    _get_document = mocker.patch("openapi_python_client._get_document", return_value=data_dict)
    error = GeneratorError()
    from_dict = mocker.patch("openapi_python_client.parser.GeneratorData.from_dict", return_value=error)
    _Project = mocker.patch("openapi_python_client.Project")
    url = mocker.MagicMock()
    path = mocker.MagicMock()
    config = mocker.MagicMock()

    from openapi_python_client import MetaType, _get_project_for_url_or_path

    project = _get_project_for_url_or_path(url=url, path=path, meta=MetaType.POETRY, config=config)

    _get_document.assert_called_once_with(url=url, path=path)
    from_dict.assert_called_once_with(data_dict, config=config)
    _Project.assert_not_called()
    assert project == error


def test__get_project_for_url_or_path_document_error(mocker):
    error = GeneratorError()
    _get_document = mocker.patch("openapi_python_client._get_document", return_value=error)

    from_dict = mocker.patch("openapi_python_client.parser.GeneratorData.from_dict")
    url = mocker.MagicMock()
    path = mocker.MagicMock()

    from openapi_python_client import MetaType, _get_project_for_url_or_path

    project = _get_project_for_url_or_path(url=url, path=path, meta=MetaType.POETRY, config=Config())

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
    config = mocker.MagicMock()

    from openapi_python_client import MetaType, create_new_client

    result = create_new_client(url=url, path=path, meta=MetaType.POETRY, config=config)

    _get_project_for_url_or_path.assert_called_once_with(
        url=url, path=path, custom_template_path=None, meta=MetaType.POETRY, file_encoding="utf-8", config=config
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
    config = mocker.MagicMock()

    from openapi_python_client import MetaType, create_new_client

    result = create_new_client(url=url, path=path, meta=MetaType.POETRY, config=config)

    _get_project_for_url_or_path.assert_called_once_with(
        url=url, path=path, custom_template_path=None, meta=MetaType.POETRY, file_encoding="utf-8", config=config
    )
    assert result == [error]


def test_update_existing_client(mocker):
    project = mocker.MagicMock()
    _get_project_for_url_or_path = mocker.patch(
        "openapi_python_client._get_project_for_url_or_path", return_value=project
    )
    url = mocker.MagicMock()
    path = mocker.MagicMock()
    config = mocker.MagicMock()

    from openapi_python_client import MetaType, update_existing_client

    result = update_existing_client(url=url, path=path, meta=MetaType.POETRY, config=config)

    _get_project_for_url_or_path.assert_called_once_with(
        url=url, path=path, custom_template_path=None, meta=MetaType.POETRY, file_encoding="utf-8", config=config
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
    config = mocker.MagicMock()

    from openapi_python_client import MetaType, update_existing_client

    result = update_existing_client(url=url, path=path, meta=MetaType.POETRY, config=config)

    _get_project_for_url_or_path.assert_called_once_with(
        url=url, path=path, custom_template_path=None, meta=MetaType.POETRY, file_encoding="utf-8", config=config
    )
    assert result == [error]


class TestGetJson:
    def test__get_document_no_url_or_path(self, mocker):
        get = mocker.patch("httpx.get")
        _Path = mocker.patch("openapi_python_client.Path")
        loads = mocker.patch("yaml.safe_load")

        from openapi_python_client import _get_document

        result = _get_document(url=None, path=None)

        assert result == GeneratorError(header="No URL or Path provided")
        get.assert_not_called()
        _Path.assert_not_called()
        loads.assert_not_called()

    def test__get_document_url_and_path(self, mocker):
        get = mocker.patch("httpx.get")
        _Path = mocker.patch("openapi_python_client.Path")
        loads = mocker.patch("yaml.safe_load")

        from openapi_python_client import _get_document

        result = _get_document(url=mocker.MagicMock(), path=mocker.MagicMock())

        assert result == GeneratorError(header="Provide URL or Path, not both.")
        get.assert_not_called()
        _Path.assert_not_called()
        loads.assert_not_called()

    def test__get_document_bad_url(self, mocker):
        get = mocker.patch("httpx.get", side_effect=httpcore.NetworkError)
        _Path = mocker.patch("openapi_python_client.Path")
        loads = mocker.patch("yaml.safe_load")

        from openapi_python_client import _get_document

        url = mocker.MagicMock()
        result = _get_document(url=url, path=None)

        assert result == GeneratorError(header="Could not get OpenAPI document from provided URL")
        get.assert_called_once_with(url)
        _Path.assert_not_called()
        loads.assert_not_called()

    def test__get_document_url_no_path(self, mocker):
        get = mocker.patch("httpx.get")
        _Path = mocker.patch("openapi_python_client.Path")
        loads = mocker.patch("yaml.safe_load")

        from openapi_python_client import _get_document

        url = "test"
        _get_document(url=url, path=None)

        get.assert_called_once_with(url)
        _Path.assert_not_called()
        loads.assert_called_once_with(get().content)

    def test__get_document_path_no_url(self, tmp_path, mocker):
        get = mocker.patch("httpx.get")
        loads = mocker.patch("yaml.safe_load")
        path = tmp_path / "test.yaml"
        path.write_text("some test data")

        from openapi_python_client import _get_document

        _get_document(url=None, path=path)

        get.assert_not_called()
        loads.assert_called_once_with(b"some test data")

    def test__get_document_bad_yaml(self, mocker, tmp_path):
        get = mocker.patch("httpx.get")
        from openapi_python_client import _get_document

        path = tmp_path / "test.yaml"
        path.write_text("'")
        result = _get_document(url=None, path=path)

        get.assert_not_called()
        assert isinstance(result, GeneratorError)
        assert "Invalid YAML" in result.header

    def test__get_document_json(self, mocker):
        class FakeResponse:
            content = b'{\n\t"foo": "bar"}'
            headers = {"content-type": "application/json; encoding=utf8"}

        get = mocker.patch("httpx.get", return_value=FakeResponse())
        yaml_loads = mocker.patch("yaml.safe_load")
        json_result = mocker.MagicMock()
        json_loads = mocker.patch("json.loads", return_value=json_result)

        from openapi_python_client import _get_document

        url = mocker.MagicMock()
        result = _get_document(url=url, path=None)

        get.assert_called_once()
        json_loads.assert_called_once_with(FakeResponse.content.decode())
        yaml_loads.assert_not_called()
        assert result == json_result

    def test__get_document_bad_json(self, mocker):
        class FakeResponse:
            content = b'{"foo"}'
            headers = {"content-type": "application/json; encoding=utf8"}

        get = mocker.patch("httpx.get", return_value=FakeResponse())

        from openapi_python_client import _get_document

        url = mocker.MagicMock()
        result = _get_document(url=url, path=None)

        get.assert_called_once()
        assert result == GeneratorError(
            header="Invalid JSON from provided source: " "Expecting ':' delimiter: line 1 column 7 (char 6)"
        )


def make_project(**kwargs):
    from unittest.mock import MagicMock

    from openapi_python_client import MetaType, Project

    kwargs = {"openapi": MagicMock(title="My Test API"), "meta": MetaType.POETRY, "config": Config(), **kwargs}

    return Project(**kwargs)


@pytest.fixture
def project_with_dir() -> Project:
    """Return a Project with the project dir pre-made (needed for cwd of commands). Unlinks after the test completes"""
    project = make_project()
    project.project_dir.mkdir()

    yield project

    project.project_dir.rmdir()


class TestProject:
    def test___init__(self, mocker):
        openapi = mocker.MagicMock(title="My Test API")

        from openapi_python_client import MetaType, Project

        project = Project(openapi=openapi, meta=MetaType.POETRY, config=Config())

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

        project = Project(openapi=openapi, meta=MetaType.NONE, config=Config())

        assert project.openapi == openapi
        assert project.package_description == "A client library for accessing My Test API"
        assert project.meta == MetaType.NONE
        assert project.project_dir == pathlib.Path.cwd()
        assert project.package_dir == pathlib.Path.cwd() / project.package_name

    @pytest.mark.parametrize(
        "project_override, package_override, expected_project_name, expected_package_name",
        (
            (None, None, "my-test-api-client", "my_test_api_client"),
            ("custom-project", None, "custom-project", "custom_project"),
            ("custom-project", "custom_package", "custom-project", "custom_package"),
            (None, "custom_package", "my-test-api-client", "custom_package"),
        ),
    )
    def test_project_and_package_names(
        self, mocker, project_override, package_override, expected_project_name, expected_package_name
    ):
        openapi = mocker.MagicMock(title="My Test API")

        from openapi_python_client import MetaType, Project

        project = Project(
            openapi=openapi,
            meta=MetaType.POETRY,
            config=Config(project_name_override=project_override, package_name_override=package_override),
        )

        assert project.project_name == expected_project_name
        assert project.package_name == expected_package_name

    def test_build(self, mocker):
        project = make_project()
        project.project_dir = mocker.MagicMock()
        project.package_dir = mocker.MagicMock()
        project._build_metadata = mocker.MagicMock()
        project._build_models = mocker.MagicMock()
        project._build_api = mocker.MagicMock()
        project._create_package = mocker.MagicMock()
        project._run_post_hooks = mocker.MagicMock()
        project._get_errors = mocker.MagicMock()

        result = project.build()

        project.project_dir.mkdir.assert_called_once()
        project._create_package.assert_called_once()
        project._build_metadata.assert_called_once()
        project._build_models.assert_called_once()
        project._build_api.assert_called_once()
        project._run_post_hooks.assert_called_once()
        project._get_errors.assert_called_once()
        assert result == project._get_errors.return_value

    def test_build_no_meta(self, mocker):
        from openapi_python_client import MetaType

        project = make_project(meta=MetaType.NONE)
        project.project_dir = mocker.MagicMock()
        project.package_dir = mocker.MagicMock()
        project._build_metadata = mocker.MagicMock()
        project._build_models = mocker.MagicMock()
        project._build_api = mocker.MagicMock()
        project._create_package = mocker.MagicMock()
        project._run_post_hooks = mocker.MagicMock()
        project._get_errors = mocker.MagicMock()

        project.build()

        project.project_dir.mkdir.assert_not_called()

    def test_build_file_exists(self, mocker):
        project = make_project()
        project.project_dir = mocker.MagicMock()
        project.project_dir.mkdir.side_effect = FileExistsError
        result = project.build()

        project.project_dir.mkdir.assert_called_once()

        assert result == [GeneratorError(detail="Directory already exists. Delete it or use the update command.")]

    def test_update(self, mocker):
        from openapi_python_client import shutil

        rmtree = mocker.patch.object(shutil, "rmtree")
        project = make_project()
        project.package_dir = mocker.MagicMock()
        project._build_metadata = mocker.MagicMock()
        project._build_models = mocker.MagicMock()
        project._build_api = mocker.MagicMock()
        project._create_package = mocker.MagicMock()
        project._run_post_hooks = mocker.MagicMock()
        project._get_errors = mocker.MagicMock()

        result = project.update()

        rmtree.assert_called_once_with(project.package_dir)
        project._create_package.assert_called_once()
        project._build_models.assert_called_once()
        project._build_api.assert_called_once()
        project._run_post_hooks.assert_called_once()
        project._get_errors.assert_called_once()
        assert result == project._get_errors.return_value

    def test_update_missing_dir(self, mocker: MockFixture):
        project = make_project()
        mocker.patch.object(project, "package_dir")
        project.package_dir.is_dir.return_value = False
        mocker.patch.object(project, "_build_models")

        errs = project.update()

        assert len(errs) == 1
        project.package_dir.is_dir.assert_called_once()
        project._build_models.assert_not_called()

    def test__build_metadata_poetry(self, mocker):
        project = make_project()
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
        readme_template.render.assert_called_once_with()
        readme_path.write_text.assert_called_once_with(readme_template.render(), encoding="utf-8")
        git_ignore_template.render.assert_called_once()
        git_ignore_path.write_text.assert_called_once_with(git_ignore_template.render(), encoding="utf-8")
        project._build_pyproject_toml.assert_called_once_with(use_poetry=True)

    def test__build_metadata_setup(self, mocker):
        from openapi_python_client import MetaType

        project = make_project(meta=MetaType.SETUP)
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
        readme_template.render.assert_called_once_with()
        readme_path.write_text.assert_called_once_with(readme_template.render(), encoding="utf-8")
        git_ignore_template.render.assert_called_once()
        git_ignore_path.write_text.assert_called_once_with(git_ignore_template.render(), encoding="utf-8")
        project._build_pyproject_toml.assert_called_once_with(use_poetry=False)
        project._build_setup_py.assert_called_once()

    def test__build_metadata_none(self, mocker):
        from openapi_python_client import MetaType

        project = make_project(meta=MetaType.NONE)
        project._build_pyproject_toml = mocker.MagicMock()

        project._build_metadata()

        project._build_pyproject_toml.assert_not_called()

    @pytest.mark.parametrize("use_poetry", [(True,), (False,)])
    def test__build_pyproject_toml(self, mocker, use_poetry):
        project = make_project()
        project.project_dir = mocker.MagicMock()
        pyproject_path = mocker.MagicMock(autospec=pathlib.Path)
        paths = {
            "pyproject.toml": pyproject_path,
        }
        project.project_dir.__truediv__.side_effect = lambda x: paths[x]

        pyproject_template = mocker.MagicMock(autospec=jinja2.Template)
        project.env = mocker.MagicMock(autospec=jinja2.Environment)
        template_path = "pyproject.toml.jinja"
        templates = {
            template_path: pyproject_template,
        }
        project.env.get_template.side_effect = lambda x: templates[x]

        project._build_pyproject_toml(use_poetry=use_poetry)

        project.env.get_template.assert_called_once_with(template_path)

        pyproject_template.render.assert_called_once_with(use_poetry=use_poetry)
        pyproject_path.write_text.assert_called_once_with(pyproject_template.render(), encoding="utf-8")

    def test__build_setup_py(self, mocker):
        project = make_project()
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

        setup_template.render.assert_called_once_with()
        setup_path.write_text.assert_called_once_with(setup_template.render(), encoding="utf-8")

    def test__run_post_hooks_reports_missing_commands(self, project_with_dir):
        fake_command_name = "blahblahdoesntexist"
        project_with_dir.config.post_hooks = [fake_command_name]
        need_to_make_cwd = not project_with_dir.project_dir.exists()
        if need_to_make_cwd:
            project_with_dir.project_dir.mkdir()

        project_with_dir._run_post_hooks()

        assert len(project_with_dir.errors) == 1
        error = project_with_dir.errors[0]
        assert error.level == ErrorLevel.WARNING
        assert error.header == "Skipping Integration"
        assert fake_command_name in error.detail

    def test__run_post_hooks_reports_stdout_of_commands_that_error_with_no_stderr(self, project_with_dir):
        failing_command = "python -c \"print('a message'); exit(1)\""
        project_with_dir.config.post_hooks = [failing_command]
        project_with_dir._run_post_hooks()

        assert len(project_with_dir.errors) == 1
        error = project_with_dir.errors[0]
        assert error.level == ErrorLevel.ERROR
        assert error.header == "python failed"
        assert "a message" in error.detail

    def test__run_post_hooks_reports_stderr_of_commands_that_error(self, project_with_dir):
        failing_command = "python -c \"print('a message'); raise Exception('some exception')\""
        project_with_dir.config.post_hooks = [failing_command]
        project_with_dir._run_post_hooks()

        assert len(project_with_dir.errors) == 1
        error = project_with_dir.errors[0]
        assert error.level == ErrorLevel.ERROR
        assert error.header == "python failed"
        assert "some exception" in error.detail


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
    project = Project(openapi=openapi, meta=MetaType.POETRY, config=Config())

    assert project._get_errors() == [1, 2, 3]


def test_custom_templates(mocker):
    from openapi_python_client import GeneratorData, MetaType, Project

    openapi = mocker.MagicMock(
        autospec=GeneratorData,
        title="My Test API",
    )

    project = Project(openapi=openapi, meta=MetaType.POETRY, config=Config())
    assert isinstance(project.env.loader, jinja2.PackageLoader)

    project = Project(
        openapi=openapi,
        custom_template_path="../end_to_end_tests/test_custom_templates",
        meta=MetaType.POETRY,
        config=Config(),
    )
    assert isinstance(project.env.loader, jinja2.ChoiceLoader)
    assert len(project.env.loader.loaders) == 2
    assert isinstance(project.env.loader.loaders[0], jinja2.FileSystemLoader)
    assert isinstance(project.env.loader.loaders[1], jinja2.PackageLoader)
