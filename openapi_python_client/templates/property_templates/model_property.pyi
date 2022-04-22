{% macro construct(property, source, initial_value=None) %}
{% if property.required and not property.nullable %}
{% if source == "response.yaml" %}
yaml = YAML(typ="base")
yaml_dict = yaml.load(response.text.encode('utf-8'))
{{ property.python_name }} = {{ property.reference.class_name }}.from_dict(yaml_dict)
{% else %}
{{ property.python_name }} = {{ property.reference.class_name }}.from_dict({{ source }})
{% endif %}
{% else %}
{% if initial_value != None %}
{{ property.python_name }} = {{ initial_value }}
{% elif property.nullable %}
{{ property.python_name }} = None
{% else %}
{{ property.python_name }}: {{ property.get_type_string() }} = UNSET
{% endif %}
_{{ property.python_name }} = {{source}}
if {% if property.nullable %}_{{ property.python_name }} is not None{% endif %}{% if property.nullable and not property.required %} and {% endif %}{% if not property.required %}not isinstance(_{{ property.python_name }},  Unset){% endif %}:
    {{ property.python_name }} = {{ property.reference.class_name }}.from_dict(_{{ property.python_name }})
{% endif %}
{% endmacro %}

{% macro check_type_for_construct(source) %}isinstance({{ source }}, dict){% endmacro %}

{% macro transform(property, source, destination, declare_type=True, query_parameter=False) %}
{% if property.required %}
{% if property.nullable %}
{{ destination }} = {{ source }}.to_dict() if {{ source }} else None
{% else %}
{{ destination }} = {{ source }}.to_dict()
{% endif %}
{% else %}
{{ destination }}{% if declare_type %}: {{ property.get_type_string(query_parameter=query_parameter, json=True) }}{% endif %} = UNSET
if not isinstance({{ source }}, Unset):
{% if property.nullable %}
    {{ destination }} = {{ source }}.to_dict() if {{ source }} else None
{% else %}
    {{ destination }} = {{ source }}.to_dict()
{% endif %}
{% endif %}
{% endmacro %}
