"""Import-time behavior of models that reference each other in a cycle.

Each generated model module re-imports its referenced models at the *bottom* of the
module (at runtime, not just under ``TYPE_CHECKING``) and then calls ``model_rebuild()``.
Those bottom-of-module imports are real import cycles.

A two-model cycle happens to resolve, because the only name still missing is the one
defined by the module that drives the rebuild. From three models onward that is no longer
true: importing ``A`` -> ``B`` -> ``C`` reaches ``C.model_rebuild()`` while ``A`` is still
incomplete and ``B`` is not yet bound in ``A``'s module globals, so resolving ``A``'s
annotations raises ``PydanticUndefinedAnnotation`` and the whole client fails to import.

Models therefore defer with ``model_rebuild(raise_errors=False)`` and ``models/__init__.py``
finishes them once every module is loaded. These tests fail at fixture setup if that
deferral is removed.
"""

import pytest

from end_to_end_tests.functional_tests.helpers import (
    assert_model_decode_encode,
    dump_for_transport,
    with_generated_client_fixture,
    with_generated_code_imports,
)

CIRCULAR_REFS_SPEC = """
components:
  schemas:
    TwoWayA:
      type: object
      properties:
        circular: {"$ref": "#/components/schemas/TwoWayB"}
    TwoWayB:
      type: object
      properties:
        circular: {"$ref": "#/components/schemas/TwoWayA"}
    ThreeWayA:
      type: object
      properties:
        circular: {"$ref": "#/components/schemas/ThreeWayB"}
    ThreeWayB:
      type: object
      properties:
        circular: {"$ref": "#/components/schemas/ThreeWayC"}
    ThreeWayC:
      type: object
      properties:
        circular: {"$ref": "#/components/schemas/ThreeWayA"}
    ArrayCycleA:
      type: object
      properties:
        children:
          type: array
          items: {"$ref": "#/components/schemas/ArrayCycleB"}
    ArrayCycleB:
      type: object
      properties:
        circular: {"$ref": "#/components/schemas/ArrayCycleC"}
    ArrayCycleC:
      type: object
      properties:
        circular: {"$ref": "#/components/schemas/ArrayCycleA"}
    UnionCycleA:
      type: object
      properties:
        circular: {"$ref": "#/components/schemas/UnionCycleB"}
    UnionCycleB:
      type: object
      properties:
        alt:
          oneOf:
            - {"$ref": "#/components/schemas/UnionCycleC"}
            - {"type": "string"}
    UnionCycleC:
      type: object
      properties:
        circular: {"$ref": "#/components/schemas/UnionCycleA"}
"""


@with_generated_client_fixture(CIRCULAR_REFS_SPEC)
@with_generated_code_imports(
    ".models.TwoWayA",
    ".models.TwoWayB",
    ".models.ThreeWayA",
    ".models.ThreeWayB",
    ".models.ThreeWayC",
    ".models.ArrayCycleA",
    ".models.ArrayCycleB",
    ".models.ArrayCycleC",
    ".models.UnionCycleA",
    ".models.UnionCycleB",
    ".models.UnionCycleC",
)
class TestCircularReferences:
    def test_two_way_cycle(self, TwoWayA, TwoWayB):
        assert_model_decode_encode(
            TwoWayA,
            {"circular": {"circular": {}}},
            TwoWayA(circular=TwoWayB(circular=TwoWayA())),
        )

    def test_three_way_cycle(self, ThreeWayA, ThreeWayB, ThreeWayC):
        assert_model_decode_encode(
            ThreeWayA,
            {"circular": {"circular": {"circular": {}}}},
            ThreeWayA(circular=ThreeWayB(circular=ThreeWayC(circular=ThreeWayA()))),
        )

    def test_three_way_cycle_through_array(self, ArrayCycleA, ArrayCycleB, ArrayCycleC):
        assert_model_decode_encode(
            ArrayCycleA,
            {"children": [{"circular": {"circular": {}}}]},
            ArrayCycleA(children=[ArrayCycleB(circular=ArrayCycleC(circular=ArrayCycleA()))]),
        )

    def test_three_way_cycle_through_union(self, UnionCycleA, UnionCycleB, UnionCycleC):
        assert_model_decode_encode(
            UnionCycleA,
            {"circular": {"alt": {"circular": {}}}},
            UnionCycleA(circular=UnionCycleB(alt=UnionCycleC(circular=UnionCycleA()))),
        )
        assert_model_decode_encode(
            UnionCycleA,
            {"circular": {"alt": "a string"}},
            UnionCycleA(circular=UnionCycleB(alt="a string")),
        )

    @pytest.mark.parametrize(
        "model_name",
        [
            "TwoWayA",
            "TwoWayB",
            "ThreeWayA",
            "ThreeWayB",
            "ThreeWayC",
            "ArrayCycleA",
            "ArrayCycleB",
            "ArrayCycleC",
            "UnionCycleA",
            "UnionCycleB",
            "UnionCycleC",
        ],
    )
    def test_every_model_in_a_cycle_is_fully_built(self, generated_client, model_name):
        """Importing the models package must leave no model waiting on a deferred rebuild.

        Pydantic would eventually rebuild these lazily on first use, so a decode/encode test
        alone cannot tell a completed model from a deferred one. Assert completeness directly
        so the ``models/__init__.py`` sweep can't silently stop running.
        """
        model = generated_client.import_symbol(".models", model_name)
        assert model.__pydantic_complete__


@with_generated_client_fixture(CIRCULAR_REFS_SPEC)
@with_generated_code_imports(".models.three_way_c.ThreeWayC")
class TestCircularReferencesImportedByModule:
    """The same models, reached by importing a single model module instead of the package.

    Importing ``package.models.three_way_c`` runs ``package/models/__init__.py`` first, so the
    deferred rebuilds still complete -- but only if the sweep lives in the package ``__init__``
    rather than in whichever module the caller happened to name.
    """

    def test_model_is_fully_built(self, ThreeWayC):
        assert ThreeWayC.__pydantic_complete__

    def test_model_round_trips(self, ThreeWayC):
        data = {"circular": {"circular": {"circular": {}}}}
        instance = ThreeWayC.from_dict(data)
        assert instance.circular.circular.circular is not None
        assert dump_for_transport(instance) == data
