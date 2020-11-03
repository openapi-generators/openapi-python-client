import pathlib

from openapi_python_client.config import Config


def test_load_from_path(mocker):
    safe_load = mocker.patch("yaml.safe_load", return_value={})
    fake_path = mocker.MagicMock(autospec=pathlib.Path)
    load_config = mocker.patch("openapi_python_client.config.Config.load_config")

    Config.load_from_path(fake_path)
    safe_load.assert_called()
    load_config.assert_called()


class TestLoadConfig:
    def test_class_overrides(self):
        from openapi_python_client.parser import reference

        override1 = {"class_name": "ExampleClass", "module_name": "example_module"}
        override2 = {"class_name": "DifferentClass", "module_name": "different_module"}
        config = Config(class_overrides={"Class1": override1, "Class2": override2})
        config.load_config()

        assert reference.class_overrides["Class1"] == reference.Reference(**override1)
        assert reference.class_overrides["Class2"] == reference.Reference(**override2)

    def test_project_and_package_name_and_package_version_overrides(self):
        config = Config(
            project_name_override="project-name",
            package_name_override="package_name",
            package_version_override="package_version",
        )
        config.load_config()

        from openapi_python_client import Project

        assert Project.project_name_override == "project-name"
        assert Project.package_name_override == "package_name"
        assert Project.package_version_override == "package_version"

    def test_field_prefix(self):
        Config(field_prefix="blah").load_config()

        from openapi_python_client import utils

        assert utils.FIELD_PREFIX == "blah"

        utils.FIELD_PREFIX = "field_"
