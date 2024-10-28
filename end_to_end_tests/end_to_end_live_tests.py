import importlib
from typing import Any

import pytest


def live_tests_3_x():
    _test_model_with_discriminated_union()


def _import_model(module_name, class_name: str) -> Any:
    module = importlib.import_module(f"my_test_api_client.models.{module_name}")
    module = importlib.reload(module)  # avoid test contamination from previous import
    return getattr(module, class_name)


def _test_model_with_discriminated_union():
    ModelType1Class = _import_model("a_discriminated_union_type_1", "ADiscriminatedUnionType1")
    ModelType2Class = _import_model("a_discriminated_union_type_2", "ADiscriminatedUnionType2")
    ModelClass = _import_model("model_with_discriminated_union", "ModelWithDiscriminatedUnion")

    assert (
        ModelClass.from_dict({"discriminated_union": {"modelType": "type1"}}) ==
        ModelClass(discriminated_union=ModelType1Class.from_dict({"modelType": "type1"}))
    )
    assert (
        ModelClass.from_dict({"discriminated_union": {"modelType": "type2"}}) ==
        ModelClass(discriminated_union=ModelType2Class.from_dict({"modelType": "type2"}))
    )
    with pytest.raises(TypeError):
        ModelClass.from_dict({"discriminated_union": {"modelType": "type3"}})
    with pytest.raises(TypeError):
        ModelClass.from_dict({"discriminated_union": {}})
