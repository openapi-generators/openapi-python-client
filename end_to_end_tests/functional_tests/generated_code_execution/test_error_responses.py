"""A documented non-2xx response is raised, not returned -- and it brings its body with it.

The generator used to open ``_parse_response`` with ``response.raise_for_status()``, so every 4xx/5xx became an
``httpx.HTTPStatusError`` before any of the client's own error handling ran: the documented error schema was parsed
nowhere, and ``Client.raise_on_unexpected_status`` was dead code on that path.

Now each documented status gets its own branch. A success is returned; anything else is raised as
``errors.UnexpectedStatus`` with the parsed body on ``.parsed``. ``default`` is the exception -- it is the catch-all
for statuses no pattern matched, so it stays on the return path.
"""

import inspect
import json

import pytest

from end_to_end_tests.functional_tests.helpers import (
    call,
    with_generated_client_fixture,
    with_generated_code_import,
    with_generated_code_imports,
)

ERROR_BODY = {"message": "nope", "code": 7}


@with_generated_client_fixture(
    """
components:
  schemas:
    Widget:
      type: object
      properties:
        name: {type: string}
      required: ["name"]
    ApiError:
      type: object
      properties:
        message: {type: string}
        code: {type: integer}
      required: ["message"]
paths:
  "/validated":
    get:
      operationId: getValidated
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema: {"$ref": "#/components/schemas/Widget"}
        "422":
          description: Validation Error
          content:
            application/json:
              schema: {"$ref": "#/components/schemas/ApiError"}
  "/ranges":
    get:
      operationId: getRanges
      responses:
        "2XX":
          description: Success
          content:
            application/json:
              schema: {"$ref": "#/components/schemas/Widget"}
        "4XX":
          description: Client Error
          content:
            application/json:
              schema: {"$ref": "#/components/schemas/ApiError"}
  "/bare-error":
    get:
      operationId: getBareError
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema: {"$ref": "#/components/schemas/Widget"}
        "404":
          description: Not Found
  "/defaulted":
    get:
      operationId: getDefaulted
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema: {"$ref": "#/components/schemas/Widget"}
        default:
          description: Anything else
          content:
            application/json:
              schema: {"$ref": "#/components/schemas/ApiError"}
  "/created":
    post:
      operationId: postCreated
      responses:
        "201":
          description: Created
          content:
            application/json:
              schema: {"$ref": "#/components/schemas/Widget"}
  "/no-content-error":
    delete:
      operationId: deleteThing
      responses:
        "204":
          description: No Content
        "409":
          description: Conflict
          content:
            application/json:
              schema: {"$ref": "#/components/schemas/ApiError"}
  "/union-error":
    get:
      operationId: getUnionError
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema: {"$ref": "#/components/schemas/Widget"}
        "400":
          description: Bad Request
          content:
            application/json:
              schema:
                oneOf:
                  - {"$ref": "#/components/schemas/ApiError"}
                  - {type: string}
"""
)
@with_generated_code_imports(
    ".client.Client",
    ".client.AuthenticatedClient",
    ".models.Widget",
    ".models.ApiError",
    ".errors.UnexpectedStatus",
)
@with_generated_code_import(".api.default.get_validated.request", alias="get_validated")
@with_generated_code_import(".api.default.get_validated._request_detailed", alias="get_validated_detailed")
@with_generated_code_import(".api.default.get_ranges.request", alias="get_ranges")
@with_generated_code_import(".api.default.get_bare_error.request", alias="get_bare_error")
@with_generated_code_import(".api.default.get_defaulted.request", alias="get_defaulted")
@with_generated_code_import(".api.default.post_created.request", alias="post_created")
@with_generated_code_import(".api.default.delete_thing.request", alias="delete_thing")
@with_generated_code_import(".api.default.get_union_error.request", alias="get_union_error")
class TestDocumentedErrorResponses:
    def test_success_is_still_parsed(self, Client, get_validated, Widget):
        result = call(Client, get_validated, json={"name": "x"})
        assert isinstance(result, Widget)
        assert result.name == "x"

    def test_non_200_success_is_returned_not_raised(self, Client, post_created, Widget):
        result = call(Client, post_created, status_code=201, json={"name": "x"})
        assert isinstance(result, Widget)

    def test_documented_error_raises_with_parsed_body(self, Client, get_validated, ApiError, UnexpectedStatus):
        with pytest.raises(UnexpectedStatus) as exc_info:
            call(Client, get_validated, status_code=422, json=ERROR_BODY)

        exc = exc_info.value
        assert exc.status_code == 422
        assert json.loads(exc.content) == ERROR_BODY
        assert isinstance(exc.parsed, ApiError)
        assert exc.parsed.message == "nope"
        assert exc.parsed.code == 7

    def test_error_range_parses_body(self, Client, get_ranges, ApiError, UnexpectedStatus):
        """A `4XX` pattern is matched by any 4xx, and its body is parsed the same way a specific code's is."""
        with pytest.raises(UnexpectedStatus) as exc_info:
            call(Client, get_ranges, status_code=418, json=ERROR_BODY)

        assert exc_info.value.status_code == 418
        assert isinstance(exc_info.value.parsed, ApiError)

    def test_error_range_local_is_named_for_the_pattern(self, generated_client):
        """Not `response_400`: the local has to come from the response's own name, or two patterns in the same
        function could collide."""
        module = generated_client.import_module(".api.default.get_ranges")
        assert "response_4xx" in inspect.getsource(module._parse_response)

    def test_error_without_a_body_raises_with_parsed_none(self, Client, get_bare_error, UnexpectedStatus):
        """A documented status with no `content` has no schema to parse, so there is nothing to attach."""
        with pytest.raises(UnexpectedStatus) as exc_info:
            call(Client, get_bare_error, status_code=404)

        assert exc_info.value.status_code == 404
        assert exc_info.value.parsed is None

    def test_undocumented_status_raises_with_parsed_none(self, Client, get_validated, UnexpectedStatus):
        with pytest.raises(UnexpectedStatus) as exc_info:
            call(Client, get_validated, status_code=500, json={"whatever": True})

        assert exc_info.value.status_code == 500
        assert exc_info.value.parsed is None

    def test_default_response_is_returned_not_raised(self, Client, get_defaulted, ApiError):
        """`default` is the catch-all for statuses no pattern matched -- it is a return value, not an error."""
        result = call(Client, get_defaulted, status_code=418, json=ERROR_BODY)
        assert isinstance(result, ApiError)
        assert result.message == "nope"

    def test_no_content_endpoint_returns_none(self, Client, delete_thing):
        assert call(Client, delete_thing, status_code=204) is None

    def test_no_content_endpoint_still_raises_its_documented_error(
        self, Client, delete_thing, ApiError, UnexpectedStatus
    ):
        """The endpoint has nothing to parse, so its return type is `None` -- the error branch must return a bare
        `None` there rather than `cast(None, None)`, which mypy rejects."""
        with pytest.raises(UnexpectedStatus) as exc_info:
            call(Client, delete_thing, status_code=409, json=ERROR_BODY)

        assert isinstance(exc_info.value.parsed, ApiError)

    def test_error_type_is_not_in_the_return_annotation(self, generated_client, Widget):
        """An error response can only be raised, so advertising it as a possible return value would be a lie."""
        module = generated_client.import_module(".api.default.get_validated")
        assert inspect.signature(module.request).return_annotation is Widget

    def test_default_type_is_in_the_return_annotation(self, generated_client, Widget, ApiError):
        module = generated_client.import_module(".api.default.get_defaulted")
        assert inspect.signature(module.request).return_annotation == ApiError | Widget

    def test_detailed_response_carries_the_error_status(self, Client, get_validated_detailed, UnexpectedStatus):
        with pytest.raises(UnexpectedStatus):
            call(Client, get_validated_detailed, status_code=422, json=ERROR_BODY)

    def test_union_error_body_is_parsed_onto_the_raised_error(
        self, Client, get_union_error, ApiError, UnexpectedStatus
    ):
        """A union error body is built before `UnexpectedStatus` is raised, so each member must reach `.parsed`."""
        with pytest.raises(UnexpectedStatus) as exc_info:
            call(Client, get_union_error, status_code=400, json=ERROR_BODY)
        assert isinstance(exc_info.value.parsed, ApiError)

        with pytest.raises(UnexpectedStatus) as exc_info:
            call(Client, get_union_error, status_code=400, json="plain text")
        assert exc_info.value.parsed == "plain text"

    def test_unmatchable_union_error_body_preserves_original_status(
        self, Client, get_union_error, UnexpectedStatus
    ):
        """The status is the error being reported, so a body matching no union member must not replace it.

        This is the one place the error path and the success path deliberately disagree: an unmatchable *success*
        body raises `TypeError`, because there the body is the whole point. Here the caller already has an error
        to handle, and losing its status code to a parse failure is strictly worse than losing `.parsed`.
        """
        with pytest.raises(UnexpectedStatus) as exc_info:
            call(Client, get_union_error, status_code=400, json=[1, 2])

        assert exc_info.value.status_code == 400
        assert exc_info.value.parsed is None

    def test_malformed_error_body_preserves_original_status(self, Client, get_validated, UnexpectedStatus):
        """A body that is not JSON at all reaches `response.json()`."""
        with pytest.raises(UnexpectedStatus) as exc_info:
            call(Client, get_validated, status_code=422, content=b"Hello :)")

        exc = exc_info.value
        assert exc.status_code == 422
        assert exc.content == b"Hello :)"
        assert exc.parsed is None

    def test_invalid_error_body_preserves_original_status(
        self, Client, get_validated, UnexpectedStatus
    ):
        """Well-formed JSON that the documented schema rejects: the document is simply wrong about the envelope.

        `ApiError.message` is required and a string, so a list fails validation.
        """
        with pytest.raises(UnexpectedStatus) as exc_info:
            call(Client, get_validated, status_code=422, json={"message": ["not", "a", "string"]})

        assert exc_info.value.status_code == 422
        assert exc_info.value.parsed is None

    def test_parse_error_does_not_override_exception_context(
        self, Client, get_validated, UnexpectedStatus
    ):
        with pytest.raises(UnexpectedStatus) as exc_info:
            call(Client, get_validated, status_code=422, content=b"{not json")

        exc = exc_info.value
        assert exc.__cause__ is None
        assert exc.__context__ is None
        assert b"not json" not in str(exc).encode()


@with_generated_client_fixture(
    """
paths:
  "/validated":
    get:
      operationId: getValidated
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                type: object
                properties:
                  name: {type: string}
                required: ["name"]
        "422":
          description: Validation Error
          content:
            application/json:
              schema:
                type: object
                properties:
                  message: {type: string}
                required: ["message"]
"""
)
@with_generated_code_imports(".client.Client", ".client.AuthenticatedClient")
@with_generated_code_import(".api.default.get_validated.request", alias="get_validated")
@with_generated_code_import(".api.default.get_validated._request_detailed", alias="get_validated_detailed")
class TestSuppressingErrors:
    """`raise_on_unexpected_status=False` opts out of raising entirely, documented or not."""

    def test_it_defaults_to_raising(self, Client, AuthenticatedClient):
        """The generator used to call `raise_for_status()` unconditionally, so every generated client raised on any
        4xx/5xx. Defaulting the flag off would have turned that into a silent `None`."""
        assert Client(base_url="https://example.com").raise_on_unexpected_status is True
        assert AuthenticatedClient(base_url="https://example.com", token="t").raise_on_unexpected_status is True

    def test_documented_error_returns_none(self, Client, get_validated):
        result = call(Client, get_validated, status_code=422, json={"message": "nope"}, raise_on_unexpected_status=False)
        assert result is None

    def test_undocumented_status_returns_none(self, Client, get_validated):
        result = call(Client, get_validated, status_code=500, raise_on_unexpected_status=False)
        assert result is None

    def test_detailed_response_reports_the_status_with_no_parsed_body(self, Client, get_validated_detailed):
        """`_request_detailed` is the way to see the status when raising is off."""
        from http import HTTPStatus

        response = call(
            Client,
            get_validated_detailed,
            status_code=422,
            json={"message": "nope"},
            raise_on_unexpected_status=False,
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.parsed is None
        assert json.loads(response.content) == {"message": "nope"}


@with_generated_client_fixture(
    """
paths:
  "/thing":
    get:
      operationId: getThing
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema: {type: string}
"""
)
@with_generated_code_import(".errors.UnexpectedStatus")
class TestUnexpectedStatus:
    def test_parsed_defaults_to_none(self, UnexpectedStatus):
        assert UnexpectedStatus(404, b"missing").parsed is None

    def test_parsed_is_kept(self, UnexpectedStatus):
        payload = object()
        assert UnexpectedStatus(404, b"missing", parsed=payload).parsed is payload

    def test_content_is_kept(self, UnexpectedStatus):
        """The message drops the body, so `content` is the only way back to it."""
        assert UnexpectedStatus(404, b"missing").content == b"missing"

    def test_message_is_the_status_alone(self, UnexpectedStatus):
        """The body can hold sensitive data and exception text reaches logs, so neither `content` nor `parsed`
        may appear in what the error prints."""
        assert str(UnexpectedStatus(404, b"missing", parsed="anything")) == "Unexpected status code: 404"
        assert "missing" not in repr(UnexpectedStatus(404, b"missing"))
