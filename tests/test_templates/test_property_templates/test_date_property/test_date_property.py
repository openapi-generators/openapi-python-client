from pathlib import Path

import jinja2


def test_required_not_nullable():
    from openapi_python_client.parser.properties import DateProperty

    prop = DateProperty(
        name="a_prop",
        required=True,
        nullable=False,
        default=None,
        description=None,
    )
    here = Path(__file__).parent
    templates_dir = here.parent.parent.parent.parent / "openapi_python_client" / "templates"

    env = jinja2.Environment(
        loader=jinja2.ChoiceLoader([jinja2.FileSystemLoader(here), jinja2.FileSystemLoader(templates_dir)])
    )

    template = env.get_template("date_property_template.py")
    content = template.render(property=prop)
    expected = here / "required_not_null.py"
    assert content == expected.read_text()


def test_required_nullable():
    from openapi_python_client.parser.properties import DateProperty

    prop = DateProperty(
        name="a_prop",
        required=True,
        nullable=True,
        default=None,
        description=None,
    )
    here = Path(__file__).parent
    templates_dir = here.parent.parent.parent.parent / "openapi_python_client" / "templates"

    env = jinja2.Environment(
        loader=jinja2.ChoiceLoader([jinja2.FileSystemLoader(here), jinja2.FileSystemLoader(templates_dir)])
    )

    template = env.get_template("date_property_template.py")
    content = template.render(property=prop)
    expected = here / "required_nullable.py"
    assert content == expected.read_text()


def test_optional_nullable():
    from openapi_python_client.parser.properties import DateProperty

    prop = DateProperty(
        name="a_prop",
        required=False,
        nullable=True,
        default=None,
        description=None,
    )
    here = Path(__file__).parent
    templates_dir = here.parent.parent.parent.parent / "openapi_python_client" / "templates"

    env = jinja2.Environment(
        loader=jinja2.ChoiceLoader([jinja2.FileSystemLoader(here), jinja2.FileSystemLoader(templates_dir)])
    )

    template = env.get_template("date_property_template.py")
    content = template.render(property=prop)
    expected = here / "optional_nullable.py"
    assert content == expected.read_text()
