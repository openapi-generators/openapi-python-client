from __future__ import annotations

from types import SimpleNamespace


def _section(content: str, start: str, end: str | None = None) -> str:
    section = content.split(start, 1)[1]
    if end is not None:
        section = section.split(end, 1)[0]
    return section


def test_model_template_renders_lazy_imports_in_stable_order(env) -> None:
    template = env.get_template("model.py.jinja")

    model = SimpleNamespace(
        is_multipart_body=True,
        relative_imports=set(),
        lazy_imports={"from ..models.z import Z", "from ..models.a import A"},
        additional_properties=False,
        class_info=SimpleNamespace(name="MyModel", module_name="my_model"),
        title="",
        description="",
        example="",
        required_properties=[],
        optional_properties=[],
        base_class_module="tandem_platform.schema.protected",
        base_class_name="BaseModel",
    )
    config = SimpleNamespace(docstrings_on_attributes=False)

    content = template.render(model=model, config=config)

    # The Pydantic-based template renders lazy imports in two places, both of which
    # must be sorted: the `if TYPE_CHECKING:` block at the top (used for annotations)
    # and the trailing block right before `model_rebuild()` (which resolves forward
    # references at runtime). The serialization method bodies (`to_dict`/`from_dict`/
    # `to_multipart`) no longer reference the imported models directly.
    sections = [
        _section(content, "if TYPE_CHECKING:", "T = TypeVar"),
        _section(content, "def to_dict(self)", "MyModel.model_rebuild()"),
    ]
    for section in sections:
        assert section.index("from ..models.a import A") < section.index("from ..models.z import Z")
