from __future__ import annotations

__all__ = ["get_reachable_classes"]

from collections.abc import Iterable, Mapping
from typing import TYPE_CHECKING

from ..utils import ClassName
from .properties import (
    EnumProperty,
    ListProperty,
    LiteralEnumProperty,
    ModelProperty,
    Property,
    UnionProperty,
)
from .properties.protocol import PropertyProtocol

if TYPE_CHECKING:  # pragma: no cover
    from .openapi import Endpoint


def get_reachable_classes(
    *,
    endpoints: Iterable[Endpoint],
    classes_by_name: Mapping[ClassName, Property],
) -> set[ClassName]:
    """Class names reachable from the given endpoints. Anything else is safe to prune.

    Walks each endpoint's properties transitively, collecting models and enums by name.
    Re-fetches each model from ``classes_by_name`` on descent, since the copy an endpoint
    holds may have empty properties.
    """
    reachable: set[ClassName] = set()
    stack: list[PropertyProtocol] = []
    for endpoint in endpoints:
        stack.extend(endpoint.list_all_parameters())
        stack.extend(response.prop for response in endpoint.responses)

    while stack:
        prop = stack.pop()
        if isinstance(prop, ModelProperty):
            name = prop.class_info.name
            if name in reachable:
                continue
            reachable.add(name)
            canonical = classes_by_name.get(name, prop)
            if isinstance(canonical, ModelProperty):
                stack.extend(canonical.required_properties or [])
                stack.extend(canonical.optional_properties or [])
                if canonical.additional_properties is not None:
                    stack.append(canonical.additional_properties)
        elif isinstance(prop, EnumProperty | LiteralEnumProperty):
            reachable.add(prop.class_info.name)
        elif isinstance(prop, ListProperty):
            stack.append(prop.inner_property)
        elif isinstance(prop, UnionProperty):
            stack.extend(prop.inner_properties)

    return reachable
