"""Tests for union_property.py.jinja's `transform` macro.

See issue: redundant `isinstance` dispatch when every union member is a model.
"""

import pytest
from jinja2 import Environment, PackageLoader

from openapi_python_client import TEMPLATE_FILTERS


@pytest.fixture
def jinja_env() -> Environment:
    """A jinja2 environment matching the one used for real code generation.

    Needs the `loopcontrols` extension (for `{% continue %}`) which the shared `env` fixture in
    `tests/test_templates/conftest.py` does not enable.
    """
    env = Environment(
        loader=PackageLoader("openapi_python_client"),
        trim_blocks=True,
        lstrip_blocks=True,
        extensions=["jinja2.ext.loopcontrols"],
    )
    env.filters.update(TEMPLATE_FILTERS)
    return env


def test_transform_homogeneous_model_union_skips_isinstance_dispatch(
    jinja_env: Environment, union_property_factory, model_property_factory
) -> None:
    """When every union member is a model, `.to_dict()` is called unconditionally (no per-member isinstance
    dispatch), since every branch's body is identical regardless of which member actually matched.
    """
    model_a = model_property_factory(name="model_a", required=True)
    model_b = model_property_factory(name="model_b", required=True)
    union = union_property_factory(name="both_models", required=False, inner_properties=[model_a, model_b])

    template = jinja_env.get_template("property_templates/union_property.py.jinja")
    result = template.module.transform(union, "self.both_models", "both_models")

    assert "isinstance(self.both_models, Unset)" in result
    assert "isinstance(self.both_models, MyClass)" not in result
    assert result.count(".to_dict()") == 1


def test_transform_mixed_union_keeps_isinstance_dispatch(
    jinja_env: Environment, union_property_factory, model_property_factory, string_property_factory
) -> None:
    """Mixed unions (model + non-model members) must keep the existing per-member isinstance dispatch,
    since those branches genuinely differ in behavior.
    """
    model_a = model_property_factory(name="model_a", required=True)
    string_b = string_property_factory(name="string_b", required=True)
    union = union_property_factory(name="mixed", required=False, inner_properties=[model_a, string_b])

    template = jinja_env.get_template("property_templates/union_property.py.jinja")
    result = template.module.transform(union, "self.mixed", "mixed")

    assert "isinstance(self.mixed, MyClass)" in result
    assert result.count(".to_dict()") == 1


def test_transform_required_homogeneous_model_union_has_no_guard(
    jinja_env: Environment, union_property_factory, model_property_factory
) -> None:
    """A required homogeneous-model union can never be Unset, so `.to_dict()` is called with no guard at all."""
    model_a = model_property_factory(name="model_a", required=True)
    model_b = model_property_factory(name="model_b", required=True)
    union = union_property_factory(name="both_models", required=True, inner_properties=[model_a, model_b])

    template = jinja_env.get_template("property_templates/union_property.py.jinja")
    result = template.module.transform(union, "self.both_models", "both_models")

    assert "isinstance" not in result
    assert result.strip() == "both_models: dict[str, Any]\nboth_models = self.both_models.to_dict()"


def test_transform_skip_unset_homogeneous_model_union_still_guards_unset(
    jinja_env: Environment, union_property_factory, model_property_factory
) -> None:
    """Request bodies render `transform` with `skip_unset=True` (the `UNSET` default is assigned elsewhere), but an
    optional homogeneous-model union can still *be* `Unset` at runtime, so `.to_dict()` must still be guarded --
    unconditionally calling it here would raise `AttributeError`/fail type-checking (`Unset` has no `to_dict`).
    """
    model_a = model_property_factory(name="model_a", required=True)
    union = union_property_factory(name="body", required=False, inner_properties=[model_a])

    template = jinja_env.get_template("property_templates/union_property.py.jinja")
    result = template.module.transform(union, "body", '_kwargs["json"]', skip_unset=True, declare_type=False)

    assert result.strip() == 'if not isinstance(body, Unset):\n    _kwargs["json"] = body.to_dict()'
