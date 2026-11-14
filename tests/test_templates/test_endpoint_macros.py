import ast
from types import SimpleNamespace

from jinja2 import Environment, PackageLoader

from openapi_python_client import TEMPLATE_FILTERS
from openapi_python_client.parser.properties import AnyProperty, DateTimeProperty, UnionProperty
from openapi_python_client.strings import PythonCode, PythonIdentifier


def _template_env() -> Environment:
    env = Environment(
        loader=PackageLoader("openapi_python_client"),
        trim_blocks=True,
        lstrip_blocks=True,
        extensions=["jinja2.ext.loopcontrols"],
    )
    env.filters.update(TEMPLATE_FILTERS)
    return env


def _render_docstring(env, return_string, is_detailed: bool) -> str:
    template = env.get_template("endpoint_macros.py.jinja")
    endpoint = SimpleNamespace(summary=None, description=None, list_all_parameters=lambda: [])
    return template.module.docstring(endpoint, return_string, is_detailed)


def test_endpoint_docstring_escapes_return_string(env) -> None:
    """The return type is rendered inside endpoint docstrings; it must not be able to break out.

    Type strings can embed literal values (e.g. const `Literal[...]`), so the docstring macro must pass the
    return string through `safe_for_docstring` rather than rendering the raw code. Note that a raw breakout
    would still be *valid* Python (that's the point of an escape), so this asserts on the docstring content,
    not just parseability.
    """
    nasty = 'Literal[\'""" + print("uh oh") + """\']'

    for is_detailed in (True, False):
        result = _render_docstring(env, nasty, is_detailed)
        # Only the two docstring delimiters; the value's triple-quotes must be escaped
        assert result.count('"""') == 2
        assert '\\"\\"\\"' in result


def test_endpoint_docstring_unwraps_python_code_return_string(env) -> None:
    """A PythonCode return type must render its (escaped) code in the docstring, not the safe pointer repr"""
    code = PythonCode("MyModel | None")

    result = _render_docstring(env, code, is_detailed=False)

    assert "MyModel | None" in result
    assert "object at 0x" not in result


def test_json_body_optional_union_without_transform_emits_valid_python() -> None:
    """Optional union JSON body with only non-transformed members must not emit an orphan else."""
    template = _template_env().get_template("endpoint_macros.py.jinja")
    prop = UnionProperty(
        name="body",
        required=False,
        default=None,
        description=None,
        example=None,
        inner_properties=[
            AnyProperty(
                name="body_type_0",
                required=True,
                default=None,
                description=None,
                example=None,
                python_name=PythonIdentifier(value="body_type_0", prefix="field_"),
            )
        ],
        python_name=PythonIdentifier(value="body", prefix="field_"),
    )
    body = SimpleNamespace(prop=prop)

    rendered = template.module.json_body(body).strip()
    ast.parse(rendered)
    assert rendered == 'if not isinstance(body, Unset):\n    _kwargs["json"] = body'


def test_json_body_optional_union_with_mixed_transform_guards_unset() -> None:
    """Optional union JSON body with transformed and non-transformed members must not fall into else for Unset."""
    template = _template_env().get_template("endpoint_macros.py.jinja")
    prop = UnionProperty(
        name="body",
        required=False,
        default=None,
        description=None,
        example=None,
        inner_properties=[
            DateTimeProperty(
                name="body_type_0",
                required=True,
                default=None,
                description=None,
                example=None,
                python_name=PythonIdentifier(value="body_type_0", prefix="field_"),
            ),
            AnyProperty(
                name="body_type_1",
                required=True,
                default=None,
                description=None,
                example=None,
                python_name=PythonIdentifier(value="body_type_1", prefix="field_"),
            ),
        ],
        python_name=PythonIdentifier(value="body", prefix="field_"),
    )
    body = SimpleNamespace(prop=prop)

    rendered = template.module.json_body(body).strip()
    ast.parse(rendered)
    assert "elif not isinstance(body, Unset):" in rendered
    assert "\nelse:" not in rendered
