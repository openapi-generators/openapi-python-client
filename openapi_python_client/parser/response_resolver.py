from typing import Optional, TYPE_CHECKING, Sequence, Tuple

from dlt.common.jsonpath import TJsonPath

from .properties import ListProperty, ModelProperty, Property
from .responses import Response

"""
ResponseResolver describes the schemas used in an endpoint's response.

List endpoints have a reference to the `ListProperty` and jsonpath to pluck the list
out of a response object at runtime.

Each endpoint gets a resolver like this attached at parsing stage.


Identifying list endpoints takes two passes.

First pass each endpoint is processed individually, simple heuristics to locate an object array within the response.

The second pass compares the top level schema in the endpoint with data item schemas from all other endpoints.

For example, suppose we have two endpoints:

1. Returns a single Ability object

/api/abilities/{id} -> {Ability}

2. Returns list of Ability objects nested within envelope

/api/abilities -> {results: [{Ability}, {Ability}]}


The Ability schema itself contains a list property, so the first endpoint will be
incorrectly identified as a list endpoint. But its top level schema is correctly identified (`Ability`)

The second endpoint is identified correctly as a list of `Ability` objects.

To correct this we run a second pass. The second pass sees that the top level schema `Ability`
is part of a list in another endpoint, so in this case we know the first endpoint is not a list.


---

Check if the list property is also a prop of another schema of some other endpoint

For example: #/components/schemas/BerryFlavorMap is a property of Berry ('/berry/{id}')

Also a property `BerryFlavor`
"""


# class ResponseResolver:
#     list_property: Optional[ListProperty[ModelProperty]] = None
#     list_property_path: Optional[TJsonPath] = None

#     data_item_schema: str = None
#     """The schema name for the data object. May be contained within a list or same as top level"""

#     top_level_schema: str
#     """The schema name of the top level object in the response"""

#     def __init__(self, response: Response) -> None:
#         self.response = response
#         # TODO: response.prop might be other types like ListProperty, maybe a naked variable
#         assert isinstance(response.prop, ModelProperty)
#         prop: ModelProperty = response.prop
#         self.top_level_schema = response.prop.class_info.name
#         # TODO: This assumes the list is one of the top level keys.
#         # Should recurse and give list property closest to top level priority

#         # TODO: Non array endpoints can still have some lists within the object.
#         # Needs a way to discriminate.
#         # E.g. check if the top level object is a part of some other endpoint.
#         for sub in prop.required_properties + prop.optional_properties:
#             if isinstance(sub, ListProperty) and isinstance(sub.inner_property, ModelProperty):
#                 self.list_property = sub
#                 self.list_property_path = sub.name
#                 self.table_name = sub.inner_property.class_info.name
#                 break


class ResponseResolver:
    list_property: Optional[ListProperty[ModelProperty]] = None
    list_property_path: Optional[TJsonPath] = None

    data_item_schema: str = None
    """The schema name for the data object. May be contained within a list or same as top level"""

    top_level_schema: str
    """The schema name of the top level object in the response"""

    def __init__(self, response: Response) -> None:
        self.response = response

        list_prop, path_components = self.get_list_property(response)
        self.list_property = list_prop
        self.list_property_path = ".".join(path_components)
        if self.list_property:
            self.data_item_schema = self.list_property.inner_property.class_info.name

    def _get_list_property_recursive(
        self, prop: Property, path_components: Tuple[str, ...] = (), first: bool = False
    ) -> Tuple[Optional[ListProperty[ModelProperty]], Tuple[str, ...]]:
        if isinstance(prop, ListProperty) and isinstance(prop.inner_property, ModelProperty):
            return prop, path_components + (prop.name,) if not first else ()  # No path for root prop
        if not isinstance(prop, ModelProperty):
            return None, path_components
        for sub in (prop.required_properties or []) + (prop.optional_properties or []):
            result, path_components = self._get_list_property_recursive(sub, path_components)
            if result:
                return result, path_components
        return None, path_components

    def get_list_property(self, response: Response) -> Tuple[Optional[ListProperty[ModelProperty]], Tuple[str, ...]]:
        prop = response.prop
        return self._get_list_property_recursive(prop, first=True)
