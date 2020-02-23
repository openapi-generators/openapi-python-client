MODULE_NAME = "openapi_python_client.openapi_parser.openapi"


class TestOpenAPI:
    def test_from_dict(self, mocker):
        Schema = mocker.patch(f"{MODULE_NAME}.Schema")
        schemas = mocker.MagicMock()
        Schema.dict.return_value = schemas
        EndpointCollection = mocker.patch(f"{MODULE_NAME}.EndpointCollection")
        endpoint_collections_by_tag = mocker.MagicMock()
        EndpointCollection.from_dict.return_value = endpoint_collections_by_tag
        in_dict = {
            "components": {"schemas": mocker.MagicMock()},
            "paths": mocker.MagicMock(),
            "info": {"title": mocker.MagicMock(), "description": mocker.MagicMock(), "version": mocker.MagicMock()},
        }
        enums = mocker.MagicMock()
        _check_enums = mocker.patch(f"{MODULE_NAME}.OpenAPI._check_enums", return_value=enums)

        from openapi_python_client.openapi_parser.openapi import OpenAPI

        openapi = OpenAPI.from_dict(in_dict)

        Schema.dict.assert_called_once_with(in_dict["components"]["schemas"])
        EndpointCollection.from_dict.assert_called_once_with(in_dict["paths"])
        _check_enums.assert_called_once_with(schemas.values(), endpoint_collections_by_tag.values())
        assert openapi == OpenAPI(
            title=in_dict["info"]["title"],
            description=in_dict["info"]["description"],
            version=in_dict["info"]["version"],
            endpoint_collections_by_tag=endpoint_collections_by_tag,
            schemas=schemas,
            enums=enums,
        )
