import pytest


def test_load(mocker):
    from openapi_python_client.resolver.data_loader import DataLoader

    dl_load_json = mocker.patch("openapi_python_client.resolver.data_loader.DataLoader.load_json")
    dl_load_yaml = mocker.patch("openapi_python_client.resolver.data_loader.DataLoader.load_yaml")

    content = mocker.MagicMock()
    DataLoader.load("foobar.json", content)
    dl_load_json.assert_called_once_with(content)

    content = mocker.MagicMock()
    DataLoader.load("foobar.jSoN", content)
    dl_load_json.assert_called_with(content)

    content = mocker.MagicMock()
    DataLoader.load("foobar.yaml", content)
    dl_load_yaml.assert_called_once_with(content)

    content = mocker.MagicMock()
    DataLoader.load("foobar.yAmL", content)
    dl_load_yaml.assert_called_with(content)

    content = mocker.MagicMock()
    DataLoader.load("foobar.ymL", content)
    dl_load_yaml.assert_called_with(content)

    content = mocker.MagicMock()
    DataLoader.load("foobar", content)
    dl_load_yaml.assert_called_with(content)


def test_load_yaml(mocker):
    from openapi_python_client.resolver.data_loader import DataLoader

    yaml_safeload = mocker.patch("yaml.safe_load")

    content = mocker.MagicMock()
    DataLoader.load_yaml(content)
    yaml_safeload.assert_called_once_with(content)


def test_load_json(mocker):
    from openapi_python_client.resolver.data_loader import DataLoader

    content = mocker.MagicMock()
    with pytest.raises(NotImplementedError):
        DataLoader.load_json(content)
