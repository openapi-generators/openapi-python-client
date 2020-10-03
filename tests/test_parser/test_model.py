import openapi_python_client.schema as oai
from openapi_python_client.parser.errors import ParseError

MODULE_NAME = "openapi_python_client.parser.model"


def test_model_from_data(mocker):
    from openapi_python_client.parser.properties import Property

    in_data = oai.Schema.construct(
        title=mocker.MagicMock(),
        description=mocker.MagicMock(),
        required=["RequiredEnum"],
        properties={
            "RequiredEnum": mocker.MagicMock(),
            "OptionalDateTime": mocker.MagicMock(),
        },
    )
    required_property = mocker.MagicMock(autospec=Property)
    required_imports = mocker.MagicMock()
    required_property.get_imports.return_value = {required_imports}
    optional_property = mocker.MagicMock(autospec=Property)
    optional_imports = mocker.MagicMock()
    optional_property.get_imports.return_value = {optional_imports}
    property_from_data = mocker.patch(
        f"{MODULE_NAME}.property_from_data",
        side_effect=[required_property, optional_property],
    )
    from_ref = mocker.patch(f"{MODULE_NAME}.Reference.from_ref")

    from openapi_python_client.parser.model import Model, model_from_data

    result = model_from_data(data=in_data, name=mocker.MagicMock())

    from_ref.assert_called_once_with(in_data.title)
    property_from_data.assert_has_calls(
        [
            mocker.call(name="RequiredEnum", required=True, data=in_data.properties["RequiredEnum"]),
            mocker.call(name="OptionalDateTime", required=False, data=in_data.properties["OptionalDateTime"]),
        ]
    )
    required_property.get_imports.assert_called_once_with(prefix="..")
    optional_property.get_imports.assert_called_once_with(prefix="..")
    assert result == Model(
        reference=from_ref(),
        required_properties=[required_property],
        optional_properties=[optional_property],
        relative_imports={
            required_imports,
            optional_imports,
        },
        description=in_data.description,
    )


def test_model_from_data_property_parse_error(mocker):
    in_data = oai.Schema.construct(
        title=mocker.MagicMock(),
        description=mocker.MagicMock(),
        required=["RequiredEnum"],
        properties={
            "RequiredEnum": mocker.MagicMock(),
            "OptionalDateTime": mocker.MagicMock(),
        },
    )
    parse_error = ParseError(data=mocker.MagicMock())
    property_from_data = mocker.patch(
        f"{MODULE_NAME}.property_from_data",
        return_value=parse_error,
    )
    from_ref = mocker.patch(f"{MODULE_NAME}.Reference.from_ref")

    from openapi_python_client.parser.model import model_from_data

    result = model_from_data(data=in_data, name=mocker.MagicMock())

    from_ref.assert_called_once_with(in_data.title)
    property_from_data.assert_called_once_with(
        name="RequiredEnum", required=True, data=in_data.properties["RequiredEnum"]
    )

    assert result == parse_error
