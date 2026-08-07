import pytest
from pydantic import ValidationError

from end_to_end_tests.functional_tests.helpers import (
    assert_model_decode_encode,
    assert_model_property_type_hint,
    call,
    with_generated_client_fixture,
    with_generated_code_import,
    with_generated_code_imports,
)


def annotation(model_class, name: str) -> str:
    """The declared annotation for one field, normalized.

    These are strings, because generated models are written under `from __future__ import annotations`. How
    they are stringified is a Python-version detail -- 3.14 unparses the AST, which rewrites string literals
    with single quotes and drops the formatter's line wrapping, while earlier versions keep the source text --
    so flatten whitespace and settle on one quote style before comparing.
    """
    return " ".join(model_class.__annotations__[name].split()).replace("'", '"')


def error_types(model_class, json_data: dict) -> list[str]:
    """The pydantic error types raised by decoding `json_data`.

    `union_tag_invalid` / `union_tag_not_found` are only ever produced by a *tagged* union, so these
    double as the observable evidence that a discriminator was applied.
    """
    with pytest.raises(ValidationError) as exc_info:
        model_class.from_dict(json_data)
    return [error["type"] for error in exc_info.value.errors()]


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
        assert_model_property_type_hint(MyModel, "string_or_int_prop", "int | str | None")


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
            "ThingA | ThingB | None",
        )
        assert_model_property_type_hint(
            ModelWithRequiredUnion,
            "thing",
            "ThingA | ThingB",
        )
        assert_model_property_type_hint(
            ModelWithUnionOfOne, "thing", "ThingA | None"
        )
        assert_model_property_type_hint(
            ModelWithUnionOfOne, "required_thing", "ThingA"
        )


@with_generated_client_fixture(
"""
components:
  schemas:
    Cat:
      type: object
      required: [petType, meows]
      properties:
        petType: { const: cat }
        meows: { type: integer }
    Dog:
      type: object
      required: [petType, barks]
      properties:
        petType: { const: dog }
        barks: { type: integer }
    Lizard:
      type: object
      required: [petType]
      properties:
        petType: { type: string, enum: [lizard, gecko] }
    Pet:
      discriminator:
        propertyName: petType
        mapping:
          cat: "#/components/schemas/Cat"
          dog: "#/components/schemas/Dog"
      oneOf:
        - $ref: "#/components/schemas/Cat"
        - $ref: "#/components/schemas/Dog"
    ModelWithTaggedUnion:
      type: object
      required: [pet]
      properties:
        pet: { $ref: "#/components/schemas/Pet" }
        maybePet:
          anyOf:
            - $ref: "#/components/schemas/Pet"
            - type: "null"
        inlinePet:
          discriminator: { propertyName: petType }
          oneOf:
            - $ref: "#/components/schemas/Cat"
            - $ref: "#/components/schemas/Lizard"
""")
@with_generated_code_imports(".models.Cat", ".models.Dog", ".models.Lizard", ".models.ModelWithTaggedUnion")
class TestDiscriminatedUnion:
    """A `discriminator` whose members carry `Literal` tags becomes a pydantic tagged union.

    Which body decodes to which member is unchanged -- pydantic tags a member by the `Literal` values of its
    own field, which is what an untagged union matches on anyway. What changes is that pydantic dispatches on
    the tag instead of attempting every member, and so reports the errors of the member the tag asked for.
    """

    def test_tag_selects_the_member(self, Cat, Dog, ModelWithTaggedUnion):
        assert_model_decode_encode(
            ModelWithTaggedUnion,
            {"pet": {"petType": "cat", "meows": 3}},
            ModelWithTaggedUnion(pet=Cat(pet_type="cat", meows=3)),
        )
        assert_model_decode_encode(
            ModelWithTaggedUnion,
            {"pet": {"petType": "dog", "barks": 1}},
            ModelWithTaggedUnion(pet=Dog(pet_type="dog", barks=1)),
        )

    def test_a_nullable_tagged_union_still_takes_null(self, Cat, Dog, ModelWithTaggedUnion):
        """`Optional[Annotated[Union[...], Field(discriminator=...)]]` is written by pydantic itself as
        `anyOf: [{oneOf: [...], discriminator: ...}, {type: "null"}]`, so the tag has to survive flattening."""
        assert_model_decode_encode(
            ModelWithTaggedUnion,
            {"pet": {"petType": "cat", "meows": 3}, "maybePet": None},
            ModelWithTaggedUnion(pet=Cat(pet_type="cat", meows=3), maybe_pet=None),
        )
        assert_model_decode_encode(
            ModelWithTaggedUnion,
            {"pet": {"petType": "cat", "meows": 3}, "maybePet": {"petType": "dog", "barks": 1}},
            ModelWithTaggedUnion(pet=Cat(pet_type="cat", meows=3), maybe_pet=Dog(pet_type="dog", barks=1)),
        )

    def test_a_member_may_claim_several_tag_values(self, Cat, Lizard, ModelWithTaggedUnion):
        """An `enum` tag under `literal_enums` is one member holding two tags -- see `TestLiteralEnumTag`."""
        assert_model_decode_encode(
            ModelWithTaggedUnion,
            {"pet": {"petType": "cat", "meows": 3}, "inlinePet": {"petType": "cat", "meows": 3}},
            ModelWithTaggedUnion(pet=Cat(pet_type="cat", meows=3), inline_pet=Cat(pet_type="cat", meows=3)),
        )

    def test_declares_a_pydantic_discriminator(self, ModelWithTaggedUnion):
        assert annotation(ModelWithTaggedUnion, "pet") == 'Annotated[Cat | Dog, Field(discriminator="pet_type")]'
        assert (
            annotation(ModelWithTaggedUnion, "maybe_pet")
            == 'Annotated[Cat | Dog | None, Field(discriminator="pet_type")]'
        )

    def test_reports_the_tag_rather_than_every_member(self, ModelWithTaggedUnion):
        assert error_types(ModelWithTaggedUnion, {"pet": {"petType": "fish"}}) == ["union_tag_invalid"]
        assert error_types(ModelWithTaggedUnion, {"pet": {"meows": 3}}) == ["union_tag_not_found"]

    def test_a_matched_tag_still_validates_the_rest_of_the_body(self, ModelWithTaggedUnion):
        assert error_types(ModelWithTaggedUnion, {"pet": {"petType": "dog", "barks": "lots"}}) == ["int_parsing"]


@with_generated_client_fixture(
"""
components:
  schemas:
    LooseA:
      type: object
      required: [tag]
      properties: { tag: { type: string }, a: { type: string } }
    LooseB:
      type: object
      required: [tag]
      properties: { tag: { type: string }, b: { type: string } }
    EnumA:
      type: object
      required: [tag]
      properties: { tag: { type: string, enum: [ea] }, a: { type: string } }
    EnumB:
      type: object
      required: [tag]
      properties: { tag: { type: string, enum: [eb] }, b: { type: string } }
    OptionalA:
      type: object
      properties: { tag: { const: oa }, a: { type: string } }
    OptionalB:
      type: object
      properties: { tag: { const: ob }, b: { type: string } }
    SameA:
      type: object
      required: [tag]
      properties: { tag: { const: same }, a: { type: string } }
    SameB:
      type: object
      required: [tag]
      properties: { tag: { const: same }, b: { type: string } }
    RenamedTagA:
      type: object
      required: [modelType]
      properties: { modelType: { const: rta }, model_type: { type: string } }
    RenamedTagB:
      type: object
      required: [modelType]
      properties: { modelType: { const: rtb } }
    OtherTagA:
      type: object
      required: [otherTag]
      properties: { otherTag: { const: ota } }
    ModelWithUntaggableUnions:
      type: object
      properties:
        looseTag:
          discriminator: { propertyName: tag }
          oneOf: [{ $ref: "#/components/schemas/LooseA" }, { $ref: "#/components/schemas/LooseB" }]
        enumTag:
          discriminator: { propertyName: tag }
          oneOf: [{ $ref: "#/components/schemas/EnumA" }, { $ref: "#/components/schemas/EnumB" }]
        optionalTag:
          discriminator: { propertyName: tag }
          oneOf: [{ $ref: "#/components/schemas/OptionalA" }, { $ref: "#/components/schemas/OptionalB" }]
        duplicateTagValue:
          discriminator: { propertyName: tag }
          oneOf: [{ $ref: "#/components/schemas/SameA" }, { $ref: "#/components/schemas/SameB" }]
        renamedTagField:
          discriminator: { propertyName: modelType }
          oneOf: [{ $ref: "#/components/schemas/RenamedTagA" }, { $ref: "#/components/schemas/RenamedTagB" }]
        untaggableMember:
          discriminator: { propertyName: tag }
          oneOf: [{ $ref: "#/components/schemas/SameA" }, { type: string }]
        onlyOneTaggedMember:
          discriminator: { propertyName: tag }
          oneOf: [{ $ref: "#/components/schemas/SameA" }, { type: "null" }]
        tagFieldsDisagree:
          anyOf:
            - discriminator: { propertyName: tag }
              oneOf: [{ $ref: "#/components/schemas/SameA" }, { $ref: "#/components/schemas/LooseA" }]
            - discriminator: { propertyName: otherTag }
              oneOf: [{ $ref: "#/components/schemas/OtherTagA" }]
""")
@with_generated_code_imports(".models.LooseA", ".models.LooseB", ".models.ModelWithUntaggableUnions")
class TestUnionsPydanticCannotTag:
    """Pydantic rejects the whole model class when a union's members cannot carry a tag.

    So every condition it enforces has to be ruled out before asking for one: each member must be a model whose
    tag field is required and annotated as a bare `Literal`, all of them have to name that field identically,
    and no tag value may claim two members. These specs each break one of those, and must come out as plain
    unions -- if any of them asked for a discriminator anyway, importing the model below would raise.
    """

    @pytest.mark.parametrize(
        ("field_name", "expected_annotation"),
        [
            # A `type: string` tag is not a `Literal`, so there is nothing to dispatch on.
            ("loose_tag", "LooseA | LooseB | None"),
            # An `enum` renders as an `Enum` subclass; only `literal_enums` makes it a `Literal`.
            ("enum_tag", "EnumA | EnumB | None"),
            # An optional tag renders as `Literal[...] | None`, which pydantic will not tag on.
            ("optional_tag", "OptionalA | OptionalB | None"),
            # Pydantic maps each value to exactly one member.
            ("duplicate_tag_value", "SameA | SameB | None"),
            # A name collision renamed the tag field in one member; pydantic needs one name across all of them.
            ("renamed_tag_field", "RenamedTagA | RenamedTagB | None"),
            # A scalar cannot be a member of a tagged union at all.
            ("untaggable_member", "SameA | str | None"),
            # One tagged member and a null is not a union to dispatch over.
            ("only_one_tagged_member", "None | SameA"),
            # Flattening brought in two candidate tag fields; neither one covers every member.
            ("tag_fields_disagree", "LooseA | OtherTagA | SameA | None"),
        ],
    )
    def test_falls_back_to_a_plain_union(self, ModelWithUntaggableUnions, field_name, expected_annotation):
        assert annotation(ModelWithUntaggableUnions, field_name) == expected_annotation

    def test_the_plain_union_still_decodes(self, LooseA, LooseB, ModelWithUntaggableUnions):
        assert_model_decode_encode(
            ModelWithUntaggableUnions,
            {"looseTag": {"tag": "anything", "b": "x"}},
            ModelWithUntaggableUnions(loose_tag=LooseB(tag="anything", b="x")),
        )
        # Every member was attempted and reported, which is what an untagged union does.
        errors = error_types(ModelWithUntaggableUnions, {"looseTag": {"a": 1}})
        assert "union_tag_not_found" not in errors
        assert errors.count("missing") == 2


@with_generated_client_fixture(
"""
components:
  schemas:
    EnumA:
      type: object
      required: [tag]
      properties: { tag: { type: string, enum: [ea, also_ea] } }
    EnumB:
      type: object
      required: [tag]
      properties: { tag: { type: string, enum: [eb] } }
    ModelWithLiteralEnumTag:
      type: object
      required: [thing]
      properties:
        thing:
          discriminator: { propertyName: tag }
          oneOf: [{ $ref: "#/components/schemas/EnumA" }, { $ref: "#/components/schemas/EnumB" }]
""",
    config="literal_enums: true",
)
@with_generated_code_imports(".models.EnumA", ".models.ModelWithLiteralEnumTag")
class TestLiteralEnumTag:
    """`literal_enums` renders an `enum` tag as a `Literal`, which pydantic can dispatch on."""

    def test_enum_tag_is_tagged_under_literal_enums(self, EnumA, ModelWithLiteralEnumTag):
        assert (
            annotation(ModelWithLiteralEnumTag, "thing") == 'Annotated[EnumA | EnumB, Field(discriminator="tag")]'
        )
        assert_model_decode_encode(
            ModelWithLiteralEnumTag,
            {"thing": {"tag": "also_ea"}},
            ModelWithLiteralEnumTag(thing=EnumA(tag="also_ea")),
        )
        assert error_types(ModelWithLiteralEnumTag, {"thing": {"tag": "nope"}}) == ["union_tag_invalid"]


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
