from pathlib import Path

import jinja2

from openapi_python_client.parser.properties import DateProperty


def date_property(required=True, nullable=True, default=None) -> DateProperty:
    return DateProperty(
        name="a_prop",
        required=required,
        nullable=nullable,
        default=default,
        python_name="a_prop",
    )


def test_required_not_nullable():
    prop = date_property(nullable=False)
    here = Path(__file__).parent
    templates_dir = here.parent.parent.parent.parent / "openapi_python_client" / "templates"

    env = jinja2.Environment(
        loader=jinja2.ChoiceLoader([jinja2.FileSystemLoader(here), jinja2.FileSystemLoader(templates_dir)]),
        trim_blocks=True,
        lstrip_blocks=True
    )

    template = env.get_template("date_property_template.py")
    content = template.render(property=prop)
    expected = here / "required_not_null.py"
    assert content == expected.read_text()


def test_required_nullable():

    prop = date_property()
    here = Path(__file__).parent
    templates_dir = here.parent.parent.parent.parent / "openapi_python_client" / "templates"

    env = jinja2.Environment(
        loader=jinja2.ChoiceLoader([jinja2.FileSystemLoader(here), jinja2.FileSystemLoader(templates_dir)]),
        trim_blocks=True,
        lstrip_blocks=True
    )

    template = env.get_template("date_property_template.py")
    content = template.render(property=prop)
    expected = here / "required_nullable.py"
    assert content == expected.read_text()


def test_optional_nullable():
    prop = date_property(required=False)
    here = Path(__file__).parent
    templates_dir = here.parent.parent.parent.parent / "openapi_python_client" / "templates"

    env = jinja2.Environment(
        loader=jinja2.ChoiceLoader([jinja2.FileSystemLoader(here), jinja2.FileSystemLoader(templates_dir)]),
        trim_blocks=True,
        lstrip_blocks=True
    )

    template = env.get_template("date_property_template.py")
    content = template.render(property=prop)
    expected = here / "optional_nullable.py"
    assert content == expected.read_text()
