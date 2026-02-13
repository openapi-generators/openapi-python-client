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
    )
    config = SimpleNamespace(docstrings_on_attributes=False)

    content = template.render(model=model, config=config)

    sections = [
        _section(content, "if TYPE_CHECKING:", "T = TypeVar"),
        _section(content, "def to_dict(self)", "def to_multipart(self)"),
        _section(content, "def to_multipart(self)", "@classmethod"),
        _section(content, "def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:", "return my_model"),
    ]
    for section in sections:
        assert section.index("from ..models.a import A") < section.index("from ..models.z import Z")
