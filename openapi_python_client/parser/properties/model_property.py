from typing import ClassVar, List, Set, Union

import attr

from ..reference import Reference
from .property import Property


@attr.s(auto_attribs=True, frozen=True)
class ModelProperty(Property):
    """ A property which refers to another Schema """

    reference: Reference

    required_properties: List[Property]
    optional_properties: List[Property]
    description: str
    relative_imports: Set[str]
    additional_properties: Union[bool, Property]

    template: ClassVar[str] = "model_property.py.jinja"
    json_is_dict: ClassVar[bool] = True

    def get_type_string(self, no_optional: bool = False) -> str:
        """ Get a string representation of type that should be used when declaring this property """
        type_string = self.reference.class_name
        if no_optional:
            return type_string
        if self.nullable:
            type_string = f"Optional[{type_string}]"
        if not self.required:
            type_string = f"Union[{type_string}, Unset]"
        return type_string

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = super().get_imports(prefix=prefix)
        imports.update(
            {
                f"from {prefix}models.{self.reference.module_name} import {self.reference.class_name}",
                "from typing import Dict",
                "from typing import cast",
            }
        )
        return imports
