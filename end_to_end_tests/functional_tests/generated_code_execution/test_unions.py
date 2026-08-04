import pytest

from end_to_end_tests.functional_tests.helpers import (
    assert_model_decode_encode,
    assert_model_property_type_hint,
    call,
    with_generated_client_fixture,
    with_generated_code_import,
    with_generated_code_imports,
)


@with_generated_client_fixture(
"""
components:
  schemas:
    StringOrInt:
      type: ["string", "integer"]
    MyModel:
      type: object
      properties:
        stringOrIntProp:
          type: ["string", "integer"]
"""
)
@with_generated_code_imports(
    ".models.MyModel",
)
class TestSimpleTypeList:
    def test_decode_encode(self, MyModel):
        assert_model_decode_encode(MyModel, {"stringOrIntProp": "a"}, MyModel(string_or_int_prop="a"))
        assert_model_decode_encode(MyModel, {"stringOrIntProp": 1}, MyModel(string_or_int_prop=1))

    def test_type_hints(self, MyModel):
        assert_model_property_type_hint(MyModel, "string_or_int_prop", "int | str | Unset")


@with_generated_client_fixture(
"""
components:
  schemas:
    ThingA:
      type: object
      properties:
        propA: { type: "string" }
      required: ["propA"]
    ThingB:
      type: object
      properties:
        propB: { type: "string" }
      required: ["propB"]
    ThingAOrB:
      oneOf:
        - $ref: "#/components/schemas/ThingA"
        - $ref: "#/components/schemas/ThingB"
    ModelWithUnion:
      type: object
      properties:
        thing: {"$ref": "#/components/schemas/ThingAOrB"}
        thingOrString:
          oneOf:
            - $ref: "#/components/schemas/ThingA"
            - type: string
    ModelWithRequiredUnion:
      type: object
      properties:
        thing: {"$ref": "#/components/schemas/ThingAOrB"}
      required: ["thing"]
    ModelWithNestedUnion:
      type: object
      properties:
        thingOrValue:
          oneOf:
            - "$ref": "#/components/schemas/ThingAOrB"
            - oneOf:
              - type: string
              - type: number
    ModelWithUnionOfOne:
      type: object
      properties:
        thing:
          oneOf:
            - $ref: "#/components/schemas/ThingA"
        requiredThing:
          oneOf:
            - $ref: "#/components/schemas/ThingA"
      required: ["requiredThing"]
""")
@with_generated_code_imports(
    ".models.ThingA",
    ".models.ThingB",
    ".models.ModelWithUnion",
    ".models.ModelWithRequiredUnion",
    ".models.ModelWithNestedUnion",
    ".models.ModelWithUnionOfOne",
)
class TestOneOf:
    def test_disambiguate_objects_via_required_properties(self, ThingA, ThingB, ModelWithUnion):
        assert_model_decode_encode(
            ModelWithUnion,
            {"thing": {"propA": "x"}},
            ModelWithUnion(thing=ThingA(prop_a="x")),
        )
        assert_model_decode_encode(
            ModelWithUnion,
            {"thing": {"propB": "x"}},
            ModelWithUnion(thing=ThingB(prop_b="x")),
        )

    def test_disambiguate_object_and_non_object(self, ThingA, ModelWithUnion):
        assert_model_decode_encode(
            ModelWithUnion,
            {"thingOrString": {"propA": "x"}},
            ModelWithUnion(thing_or_string=ThingA(prop_a="x")),
        )
        assert_model_decode_encode(
            ModelWithUnion,
            {"thingOrString": "x"},
            ModelWithUnion(thing_or_string="x"),
        )
    
    def test_disambiguate_nested_union(self, ThingA, ThingB, ModelWithNestedUnion):
        assert_model_decode_encode(
            ModelWithNestedUnion,
            {"thingOrValue": {"propA": "x"}},
            ModelWithNestedUnion(thing_or_value=ThingA(prop_a="x")),
        )
        assert_model_decode_encode(
            ModelWithNestedUnion,
            {"thingOrValue": 3},
            ModelWithNestedUnion(thing_or_value=3),
        )

    def test_type_hints(self, ModelWithUnion, ModelWithRequiredUnion, ModelWithUnionOfOne, ThingA):
        assert_model_property_type_hint(
            ModelWithUnion,
            "thing",
            "ThingA | ThingB | Unset",
        )
        assert_model_property_type_hint(
            ModelWithRequiredUnion,
            "thing",
            "ThingA | ThingB",
        )
        assert_model_property_type_hint(
            ModelWithUnionOfOne, "thing", "ThingA | Unset"
        )
        assert_model_property_type_hint(
            ModelWithUnionOfOne, "required_thing", "ThingA"
        )


@with_generated_client_fixture(
"""
components:
  schemas:
    Thing:
      type: object
      properties:
        propA: { type: string }
      required: ["propA"]
paths:
  "/plain":
    get:
      operationId: getPlain
      responses:
        "200":
          description: Success
          content: { application/json: { schema: { type: string } } }
  "/scalars":
    get:
      operationId: getScalars
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                anyOf: [{ type: string }, { type: integer }]
  "/number-or-string":
    get:
      operationId: getNumberOrString
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                anyOf: [{ type: number }, { type: string }]
  "/int-or-bool":
    get:
      operationId: getIntOrBool
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                anyOf: [{ type: integer }, { type: boolean }]
  "/model-or-string":
    get:
      operationId: getModelOrString
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                oneOf:
                  - $ref: "#/components/schemas/Thing"
                  - { type: string }
  "/model-or-null":
    get:
      operationId: getModelOrNull
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                oneOf:
                  - $ref: "#/components/schemas/Thing"
                  - { type: "null" }
  "/object-or-string":
    get:
      operationId: getObjectOrString
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                anyOf:
                  - { type: object, additionalProperties: { type: string } }
                  - { type: string }
  "/array-or-string":
    get:
      operationId: getArrayOrString
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                anyOf:
                  - { type: array, items: { type: string } }
                  - { type: string }
  "/any-or-string":
    get:
      operationId: getAnyOrString
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                anyOf: [{}, { type: string }]
  "/branded-or-model":
    get:
      operationId: getBrandedOrModel
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                oneOf:
                  - $ref: "#/components/schemas/Thing"
                  - { type: string, format: "brand::protected::ProtectedString" }
""")
@with_generated_code_imports(".client.Client", ".models.Thing")
@with_generated_code_import(".api.default.get_plain.request", alias="get_plain")
@with_generated_code_import(".api.default.get_scalars.request", alias="get_scalars")
@with_generated_code_import(".api.default.get_number_or_string.request", alias="get_number_or_string")
@with_generated_code_import(".api.default.get_int_or_bool.request", alias="get_int_or_bool")
@with_generated_code_import(".api.default.get_model_or_string.request", alias="get_model_or_string")
@with_generated_code_import(".api.default.get_model_or_null.request", alias="get_model_or_null")
@with_generated_code_import(".api.default.get_object_or_string.request", alias="get_object_or_string")
@with_generated_code_import(".api.default.get_array_or_string.request", alias="get_array_or_string")
@with_generated_code_import(".api.default.get_any_or_string.request", alias="get_any_or_string")
@with_generated_code_import(".api.default.get_branded_or_model.request", alias="get_branded_or_model")
class TestUnionResponseBodies:
    """A response body that matches none of its union's members is rejected, not cast.

    Models are Pydantic, so the union macros are reached only from `construct_response` -- these are
    response bodies, never user-supplied values. The old code ended every union that had a raw-value
    member in an unconditional `cast()`, so a body matching nothing at all came back to the caller
    under a type it did not have. It now raises `TypeError`.

    The guard tests the *JSON* type rather than the Python one, which is what these cases pin down:
    JSON draws no int/float distinction, `bool` is not an `int` on the wire, and a branded string
    arrives as a plain `str`.
    """

    NO_MATCH = "did not match any declared union type"

    def test_scalar_union_accepts_its_members(self, Client, get_scalars):
        assert call(Client, get_scalars, json="a") == "a"
        assert call(Client, get_scalars, json=7) == 7

    @pytest.mark.parametrize("body", [1.5, {}, [], True])
    def test_scalar_union_rejects_everything_else(self, Client, get_scalars, body):
        with pytest.raises(TypeError, match=self.NO_MATCH):
            call(Client, get_scalars, json=body)

    def test_number_member_accepts_a_json_integer(self, Client, get_number_or_string):
        """`json.loads("1")` is an `int`, so a `number` member has to accept one."""
        assert call(Client, get_number_or_string, json=1) == 1
        assert call(Client, get_number_or_string, json=1.5) == 1.5
        assert call(Client, get_number_or_string, json="a") == "a"

    @pytest.mark.parametrize("body", [{}, [], True])
    def test_number_member_rejects_non_numbers(self, Client, get_number_or_string, body):
        with pytest.raises(TypeError, match=self.NO_MATCH):
            call(Client, get_number_or_string, json=body)

    def test_bool_satisfies_a_boolean_member_not_an_integer_one(self, Client, get_scalars, get_int_or_bool):
        """`isinstance(True, int)` is True, but JSON `true` is not a number -- the guard follows JSON."""
        assert call(Client, get_int_or_bool, json=True) is True
        assert call(Client, get_int_or_bool, json=7) == 7
        with pytest.raises(TypeError, match=self.NO_MATCH):
            call(Client, get_scalars, json=True)

    def test_model_or_raw_value(self, Client, Thing, get_model_or_string):
        assert call(Client, get_model_or_string, json={"propA": "x"}) == Thing(prop_a="x")
        assert call(Client, get_model_or_string, json="x") == "x"

    def test_model_or_raw_value_rejects_a_body_matching_neither(self, Client, get_model_or_string):
        with pytest.raises(TypeError, match=self.NO_MATCH):
            call(Client, get_model_or_string, json=[1])

    def test_nullable_model_accepts_null_and_the_model(self, Client, Thing, get_model_or_null):
        assert call(Client, get_model_or_null, content=b"null") is None
        assert call(Client, get_model_or_null, json={"propA": "x"}) == Thing(prop_a="x")

    def test_nullable_model_rejects_an_object_that_fails_validation(self, Client, get_model_or_null):
        """The hole this closes: `{"nope": 1}` used to come back as a raw dict typed as `Thing`."""
        with pytest.raises(TypeError, match=self.NO_MATCH):
            call(Client, get_model_or_null, json={"nope": 1})

    def test_object_or_raw_value(self, Client, get_object_or_string):
        assert call(Client, get_object_or_string, json={"k": "v"}) == {"k": "v"}
        assert call(Client, get_object_or_string, json="x") == "x"
        with pytest.raises(TypeError, match=self.NO_MATCH):
            call(Client, get_object_or_string, json=1)

    def test_array_or_raw_value(self, Client, get_array_or_string):
        assert call(Client, get_array_or_string, json=["a", "b"]) == ["a", "b"]
        assert call(Client, get_array_or_string, json="x") == "x"
        with pytest.raises(TypeError, match=self.NO_MATCH):
            call(Client, get_array_or_string, json={})

    @pytest.mark.parametrize("body", ["a", 1, 1.5, True, [1, 2], {"k": 1}])
    def test_untyped_member_accepts_any_body(self, Client, get_any_or_string, body):
        """An untyped member matches everything, so there is nothing left to reject."""
        assert call(Client, get_any_or_string, json=body) == body

    def test_branded_string_member_accepts_a_plain_json_string(self, Client, Thing, get_branded_or_model):
        """A branded member's Python type is a `str` *subtype*; the wire only ever carries a `str`."""
        assert call(Client, get_branded_or_model, json="plain") == "plain"
        assert call(Client, get_branded_or_model, json={"propA": "x"}) == Thing(prop_a="x")

    def test_type_error_is_documented_only_where_it_can_happen(self, get_scalars, get_plain):
        assert "TypeError: If a response body matches none of the types" in get_scalars.__doc__
        assert "TypeError" not in get_plain.__doc__
