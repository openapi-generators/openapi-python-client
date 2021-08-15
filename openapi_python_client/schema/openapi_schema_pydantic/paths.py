from typing import Dict

from .path_item import PathItem

Paths = Dict[str, PathItem]
"""
Holds the relative paths to the individual endpoints and their operations.
The path is appended to the URL from the [`Server Object`](#serverObject) in order to construct the full URL.

The Paths MAY be empty, due to [ACL constraints](#securityFiltering).

References:
    - https://swagger.io/docs/specification/paths-and-operations/
    - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#pathsObject
"""
