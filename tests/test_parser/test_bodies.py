from copy import deepcopy

import pytest

from openapi_python_client import schema as oai
from openapi_python_client.parser.bodies import body_from_data, mark_multipart_file_properties
from openapi_python_client.parser.errors import ParseError
from openapi_python_client.parser.properties import Schemas

OCTET_STREAM = {"type": "string", "contentMediaType": "application/octet-stream"}


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

    errs, _ = body_from_data(
        data=operation, schemas=Schemas(), config=config, endpoint_name="this will not succeed", request_bodies={}
    )

    assert len(errs) == len(operation.request_body.content)
    assert all(isinstance(err, ParseError) for err in errs)


def _document(body_schema, content_type="multipart/form-data", components=None):
    document = {
        "openapi": "3.1.0",
        "paths": {"/upload": {"post": {"requestBody": {"content": {content_type: {"schema": body_schema}}}}}},
    }
    if components is not None:
        document["components"] = {"schemas": components}
    return document


class TestMarkMultipartFileProperties:
    """`contentMediaType: application/octet-stream` is 3.1's spelling of `format: binary`.

    It only carries that meaning inside a multipart body: on a JSON body the identical
    property schema describes a value that really is transported as a string.
    """

    def test_marks_inline_multipart_property(self):
        document = _document({"type": "object", "properties": {"file": dict(OCTET_STREAM)}})

        mark_multipart_file_properties(document)

        prop = document["paths"]["/upload"]["post"]["requestBody"]["content"]["multipart/form-data"]["schema"]
        assert prop["properties"]["file"]["format"] == "binary"
        # The 3.1 keyword is the spec-correct description and stays put.
        assert prop["properties"]["file"]["contentMediaType"] == "application/octet-stream"

    def test_marks_referenced_multipart_body(self):
        document = _document(
            {"$ref": "#/components/schemas/UploadBody"},
            components={"UploadBody": {"type": "object", "properties": {"file": dict(OCTET_STREAM)}}},
        )

        mark_multipart_file_properties(document)

        assert document["components"]["schemas"]["UploadBody"]["properties"]["file"]["format"] == "binary"

    def test_marks_array_items_and_union_members(self):
        document = _document(
            {
                "type": "object",
                "properties": {
                    "files": {"type": "array", "items": dict(OCTET_STREAM)},
                    "optional": {"anyOf": [dict(OCTET_STREAM), {"type": "null"}]},
                },
            }
        )

        mark_multipart_file_properties(document)

        properties = document["paths"]["/upload"]["post"]["requestBody"]["content"]["multipart/form-data"]["schema"][
            "properties"
        ]
        assert properties["files"]["items"]["format"] == "binary"
        assert properties["optional"]["anyOf"][0]["format"] == "binary"

    def test_marks_inline_all_of_members(self):
        document = _document(
            {
                "allOf": [
                    {"type": "object", "properties": {"file": dict(OCTET_STREAM)}},
                    {"$ref": "#/components/schemas/Shared"},
                ]
            },
            components={"Shared": {"type": "object", "properties": {"blob": dict(OCTET_STREAM)}}},
        )

        mark_multipart_file_properties(document)

        schema = document["paths"]["/upload"]["post"]["requestBody"]["content"]["multipart/form-data"]["schema"]
        assert schema["allOf"][0]["properties"]["file"]["format"] == "binary"
        # A $ref inside allOf reaches a component other schemas may share, so it is left alone.
        assert "format" not in document["components"]["schemas"]["Shared"]["properties"]["blob"]

    @pytest.mark.parametrize(
        "content_type",
        ["application/json", "application/x-www-form-urlencoded", "application/octet-stream"],
    )
    def test_leaves_non_multipart_bodies_alone(self, content_type):
        document = _document({"type": "object", "properties": {"blob": dict(OCTET_STREAM)}}, content_type)
        expected = deepcopy(document)

        mark_multipart_file_properties(document)

        assert document == expected

    def test_leaves_schema_shared_with_another_media_type_alone(self):
        """Annotating it would change how the component is generated everywhere."""
        document = _document(
            {"$ref": "#/components/schemas/Shared"},
            components={"Shared": {"type": "object", "properties": {"blob": dict(OCTET_STREAM)}}},
        )
        document["paths"]["/store"] = {
            "post": {
                "requestBody": {"content": {"application/json": {"schema": {"$ref": "#/components/schemas/Shared"}}}}
            }
        }
        expected = deepcopy(document)

        mark_multipart_file_properties(document)

        assert document == expected

    def test_leaves_non_binary_properties_alone(self):
        document = _document(
            {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "html": {"type": "string", "contentMediaType": "text/html"},
                    "count": {"type": "integer"},
                },
            }
        )
        expected = deepcopy(document)

        mark_multipart_file_properties(document)

        assert document == expected

    def test_keeps_an_explicit_format(self):
        document = _document(
            {"type": "object", "properties": {"file": {**OCTET_STREAM, "format": "uuid"}}},
        )

        mark_multipart_file_properties(document)

        schema = document["paths"]["/upload"]["post"]["requestBody"]["content"]["multipart/form-data"]["schema"]
        assert schema["properties"]["file"]["format"] == "uuid"

    def test_handles_nullable_type_list(self):
        document = _document({"type": "object", "properties": {"file": {**OCTET_STREAM, "type": ["string", "null"]}}})

        mark_multipart_file_properties(document)

        schema = document["paths"]["/upload"]["post"]["requestBody"]["content"]["multipart/form-data"]["schema"]
        assert schema["properties"]["file"]["format"] == "binary"

    def test_marks_body_declared_in_components(self):
        document = {
            "openapi": "3.1.0",
            "paths": {},
            "components": {
                "requestBodies": {
                    "Upload": {
                        "content": {
                            "multipart/form-data": {
                                "schema": {"type": "object", "properties": {"file": dict(OCTET_STREAM)}}
                            }
                        }
                    }
                }
            },
        }

        mark_multipart_file_properties(document)

        schema = document["components"]["requestBodies"]["Upload"]["content"]["multipart/form-data"]["schema"]
        assert schema["properties"]["file"]["format"] == "binary"

    def test_handles_a_content_type_with_parameters(self):
        document = _document(
            {"type": "object", "properties": {"file": dict(OCTET_STREAM)}},
            content_type="multipart/form-data; charset=utf-8",
        )

        mark_multipart_file_properties(document)

        schema = document["paths"]["/upload"]["post"]["requestBody"]["content"]["multipart/form-data; charset=utf-8"][
            "schema"
        ]
        assert schema["properties"]["file"]["format"] == "binary"

    @pytest.mark.parametrize(
        "document",
        [
            {},
            {"paths": None},
            {"paths": {}, "components": None},
            {
                "paths": {"/x": {"post": {"requestBody": {"content": {"multipart/form-data": {}}}}}},
                "components": {"schemas": {}},
            },
            # A schema property that happens to be named "content" is not a content map.
            {"paths": {}, "components": {"schemas": {"M": {"properties": {"content": {"type": "string"}}}}}},
            {
                "paths": {
                    "/x": {
                        "post": {
                            "requestBody": {
                                "content": {"multipart/form-data": {"schema": {"$ref": "#/components/schemas/Missing"}}}
                            }
                        }
                    }
                },
                "components": {"schemas": {}},
            },
            {
                "paths": {
                    "/x": {
                        "post": {
                            "requestBody": {
                                "content": {"multipart/form-data": {"schema": {"$ref": "external.yaml#/Body"}}}
                            }
                        }
                    }
                }
            },
        ],
    )
    def test_tolerates_incomplete_documents(self, document):
        mark_multipart_file_properties(document)
