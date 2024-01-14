from openapi_python_client import schema as oai
from openapi_python_client.parser.bodies import body_from_data
from openapi_python_client.parser.errors import ParseError
from openapi_python_client.parser.properties import Schemas


def test_errors(config):
    operation = oai.Operation(
        requestBody=oai.RequestBody(
            content={
                "invalid content type": oai.MediaType(
                    media_type_schema=oai.Schema(
                        type=oai.DataType.STRING,
                    )
                ),
                "application/json": oai.MediaType(
                    media_type_schema=None  # Missing media type schema is an error
                ),
                "text/html": oai.MediaType(  # content type not supported by the generator
                    media_type_schema=oai.Schema(
                        type=oai.DataType.STRING,
                    )
                ),
                "application/sushi+json": oai.MediaType(
                    media_type_schema=oai.Schema(
                        type=oai.DataType.INTEGER,
                        default="make this an invalid property",
                    )
                ),
            }
        ),
        responses={},
    )

    errs, _ = body_from_data(data=operation, schemas=Schemas(), config=config, endpoint_name="this will not succeed")

    assert len(errs) == len(operation.request_body.content)
    assert all(isinstance(err, ParseError) for err in errs)
