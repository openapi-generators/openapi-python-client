from datetime import date, datetime

from dlt.common.data_types import py_type_to_sc_type
from dlt.common.schema import TColumnSchema, TTableSchema, TTableSchemaColumns

from .parser.properties import ListProperty, ModelProperty
from .parser.properties import types as prop_types
from .parser.properties.schemas import Schemas

types_map = {
    prop_types.StringProperty: str,
    prop_types.DateTimeProperty: datetime,
    prop_types.DateProperty: date,
    prop_types.FloatProperty: float,
    prop_types.IntProperty: int,
    prop_types.BooleanProperty: bool,
    prop_types.ListProperty: list,
}


def create_dlt_schemas(model: ModelProperty):
    # TODO
    columns: TTableSchemaColumns = dict()
    new_schema: TTableSchema = dict(name=model.name, description=model.description, columns=columns)
    tables = []
    for prop in model.required_properties + model.optional_properties:
        if isinstance(prop, ModelProperty):
            py_type = dict
        else:
            py_type = types_map[prop.__class__]

        dlt_type = py_type_to_sc_type(py_type)

        columns[prop.name] = dict(
            name=prop.name, data_type=dlt_type, nullable=not prop.required, description=prop.description
        )
