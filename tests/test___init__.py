from pathlib import Path

import pytest

from openapi_python_client import Config, ErrorLevel, GeneratorData, MetaType, Project
from openapi_python_client.config import ConfigFile
from openapi_python_client.schema.untrusted_string import UntrustedString

default_http_timeout = ConfigFile.model_json_schema()["properties"]["http_timeout"]["default"]


def make_project(config: Config) -> Project:
    return Project(
        openapi=GeneratorData(
            title=UntrustedString("My API Client"),
            description=None,
            models=[],
            version="",
            errors=[],
            endpoint_collections_by_tag={},
            enums=[],
        ),
        config=config,
    )


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

        project_with_dir._run_post_hooks()

        assert len(project_with_dir.errors) == 1
        error = project_with_dir.errors[0]
        assert error.level == ErrorLevel.WARNING
        assert error.header == "Skipping Integration"
        assert fake_command_name in error.detail

    def test__run_post_hooks_reports_stdout_of_commands_that_error_with_no_stderr(self, project_with_dir):
        failing_command = "python3 -c \"print('a message'); exit(1)\""
        project_with_dir.config.post_hooks = [failing_command]
        project_with_dir._run_post_hooks()

        assert len(project_with_dir.errors) == 1
        error = project_with_dir.errors[0]
        assert error.level == ErrorLevel.ERROR
        assert error.header == "python3 failed"
        assert "a message" in error.detail

    def test__run_post_hooks_reports_stderr_of_commands_that_error(self, project_with_dir):
        failing_command = "python3 -c \"print('a message'); raise Exception('some exception')\""
        project_with_dir.config.post_hooks = [failing_command]
        project_with_dir._run_post_hooks()

        assert len(project_with_dir.errors) == 1
        error = project_with_dir.errors[0]
        assert error.level == ErrorLevel.ERROR
        assert error.header == "python3 failed"
        assert "some exception" in error.detail

    def test_build_creates_parent_directories(self, tmp_path):
        fresh_config = Config.from_sources(
            ConfigFile(),
            MetaType.POETRY,
            document_source=Path("openapi.yaml"),
            file_encoding="utf-8",
            overwrite=False,
            output_path=None,
        )
        project = make_project(fresh_config)
        project.project_dir = tmp_path / "nested" / "dir" / "my-api-client"
        project.package_dir = project.project_dir / project.package_name

        errors = project.build()

        assert errors == []
        assert project.project_dir.exists()
        assert project.project_dir.is_dir()
