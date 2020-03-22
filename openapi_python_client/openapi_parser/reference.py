""" A Reference is ultimately a Class which will be in models, usually defined in a body input or return type """

from __future__ import annotations

from dataclasses import dataclass

import stringcase


@dataclass
class Reference:
    """ A reference to a class which will be in models """

    class_name: str
    module_name: str

    @staticmethod
    def from_ref(ref: str) -> Reference:
        """ Get a Reference from the openapi #/schemas/blahblah string """
        ref_value = ref.split("/")[-1]
        return Reference(class_name=stringcase.pascalcase(ref_value), module_name=stringcase.snakecase(ref_value),)
