import pytest

from openapi_python_client import Config, ErrorLevel, Project
from openapi_python_client.config import ConfigFile

default_http_timeout = ConfigFile.model_json_schema()["properties"]["http_timeout"]["default"]


def make_project(config: Config) -> Project:
    from unittest.mock import MagicMock

    from openapi_python_client import Project

    return Project(openapi=MagicMock(title="My Test API"), config=config)


@pytest.fixture
def project_with_dir(config) -> Project:
    """Return a Project with the project dir pre-made (needed for cwd of commands). Unlinks after the test completes"""
    project = make_project(config)
    project.project_dir.mkdir()

    yield project

    project.project_dir.rmdir()


class TestProject:
    def test__run_post_hooks_reports_missing_commands(self, project_with_dir: Project) -> None:
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
