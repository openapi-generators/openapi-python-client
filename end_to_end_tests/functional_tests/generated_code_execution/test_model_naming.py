from end_to_end_tests.functional_tests.helpers import (
    with_generated_client_fixture,
    with_generated_code_imports,
)

# FastAPI emits one component schema per direction when a Pydantic model is used for both
# request and response bodies, e.g. "DemoEntity-Input" and "DemoEntity-Output". Both carry the
# same `title`, so naming models from the title alone collides.
DIRECTIONAL_SCHEMAS_SPEC = """
components:
  schemas:
    DemoEntity-Input:
      title: DemoEntity
      type: object
      required: ["foo"]
      properties:
        foo: {"type": "string"}
        bar: {"type": "string", "default": "plopp"}
    DemoEntity-Output:
      title: DemoEntity
      type: object
      required: ["foo", "bar"]
      properties:
        foo: {"type": "string"}
        bar: {"type": "string", "default": "plopp"}
paths:
  /demo:
    post:
      tags: ["demo"]
      requestBody:
        required: true
        content:
          application/json:
            schema: {"$ref": "#/components/schemas/DemoEntity-Input"}
      responses:
        "200":
          description: Successful Response
          content:
            application/json:
              schema: {"$ref": "#/components/schemas/DemoEntity-Output"}
"""


@with_generated_client_fixture(DIRECTIONAL_SCHEMAS_SPEC)
@with_generated_code_imports(
    ".models.DemoEntityInput",
    ".models.DemoEntityOutput",
)
class TestSameTitleDifferentReferenceNames:
    def test_generates_a_model_per_reference(self, generated_client, DemoEntityInput, DemoEntityOutput):
        assert "Warning(s) encountered while generating" not in (
            generated_client.generator_result.stdout + generated_client.generator_result.stderr
        )
        assert DemoEntityInput is not DemoEntityOutput

    def test_each_model_keeps_its_own_required_properties(self, DemoEntityInput, DemoEntityOutput):
        # `bar` is optional on the way in (it has a default the server fills), required on the way out.
        assert DemoEntityInput.from_dict({"foo": "x"}).bar == "plopp"
        assert DemoEntityOutput.from_dict({"foo": "x", "bar": "y"}).bar == "y"

    def test_endpoint_uses_the_directional_models(self, generated_client, DemoEntityInput, DemoEntityOutput):
        demo = generated_client.import_module(".api.demo.post_demo")
        assert demo.request.__annotations__["body"] is DemoEntityInput
        assert demo.request.__annotations__["return"] is DemoEntityOutput


@with_generated_client_fixture(
    """
components:
  schemas:
    Status-Input:
      title: Status
      type: string
      enum: ["a", "b"]
    Status-Output:
      title: Status
      type: string
      enum: ["a", "b", "c"]
    UnambiguousComponentName:
      title: RenamedByTitle
      type: object
      properties:
        x: {"type": "string"}
"""
)
@with_generated_code_imports(
    ".models.StatusInput",
    ".models.StatusOutput",
    ".models.RenamedByTitle",
)
class TestSameTitleOnEnums:
    def test_generates_an_enum_per_reference(self, StatusInput, StatusOutput):
        assert [member.value for member in StatusInput] == ["a", "b"]
        assert [member.value for member in StatusOutput] == ["a", "b", "c"]

    def test_unambiguous_title_still_takes_precedence(self, RenamedByTitle):
        assert RenamedByTitle.__name__ == "RenamedByTitle"
