__all__ = [
    "Class",
    "Parameters",
    "ReferencePath",
    "Schemas",
    "parameter_from_data",
    "parameter_from_reference",
    "parse_reference_path",
    "update_parameters_with_data",
    "update_schemas_with_data",
]

from typing import TYPE_CHECKING, NewType
from urllib.parse import urlparse

from attrs import define, evolve, field

from ... import Config
from ... import schema as oai
from ...schema.openapi_schema_pydantic import Parameter
from ...schema.ref import Ref
from ...schema.untrusted_string import UntrustedString
from ...strings import ClassName, PythonIdentifier
from ..errors import ParameterError, ParseError, PropertyError

if TYPE_CHECKING:  # pragma: no cover
    from .model_property import ModelProperty
    from .property import Property
else:
    ModelProperty = "ModelProperty"
    Property = "Property"


ReferencePath = NewType("ReferencePath", UntrustedString)


def parse_reference_path(ref_path_raw: Ref) -> ReferencePath | ParseError:
    """
    Takes a raw string provided in a `$ref` and turns it into a validated `_ReferencePath` or a `ParseError` if
    validation fails.

    See Also:
        - https://swagger.io/docs/specification/using-ref/
    """
    parsed = urlparse(ref_path_raw.get_untrusted_value())
    if parsed.scheme or parsed.path:
        return ParseError(detail=f"Remote references such as {parsed} are not supported yet.")
    return ReferencePath(UntrustedString(parsed.fragment))


def get_reference_simple_name(ref_path: Ref | UntrustedString) -> UntrustedString:
    """
    Takes a path like `/components/schemas/NameOfThing` and returns a string like `NameOfThing`.
    """
    return UntrustedString(ref_path.get_untrusted_value().rsplit("/", maxsplit=1)[-1])


@define
class Class:
    """Represents Python class which will be generated from an OpenAPI schema"""

    name: ClassName
    module_name: PythonIdentifier

    @staticmethod
    def from_string(*, string: str | UntrustedString, config: Config) -> "Class":
        """Get a Class from an arbitrary string"""
        untrusted_class_name = get_reference_simple_name(Ref(string))  # Get rid of ref path stuff
        class_name = ClassName(untrusted_class_name, config.field_prefix)
        override = config.class_overrides.get(class_name)

        if override is not None and override.class_name is not None:
            class_name = ClassName(override.class_name, config.field_prefix)

        if override is not None and override.module_name is not None:
            module_name = override.module_name
        else:
            module_name = class_name
        module_name = PythonIdentifier(module_name, config.field_prefix)

        return Class(name=class_name, module_name=module_name)


@define
class Schemas:
    """Structure for containing all defined, shareable, and reusable schemas (attr classes and Enums)"""

    classes_by_reference: dict[ReferencePath, Property] = field(factory=dict)
    dependencies: dict[ReferencePath, set[ReferencePath | ClassName]] = field(factory=dict)
    classes_by_name: dict[ClassName, Property] = field(factory=dict)
    models_to_process: list[ModelProperty] = field(factory=list)
    errors: list[ParseError] = field(factory=list)

    def add_dependencies(self, ref_path: ReferencePath, roots: set[ReferencePath | ClassName]) -> None:
        """Record new dependencies on the given ReferencePath

        Args:
            ref_path: The ReferencePath being referenced
            roots: A set of identifiers for the objects dependent on the object corresponding to `ref_path`
        """
        self.dependencies.setdefault(ref_path, set())
        self.dependencies[ref_path].update(roots)


def ensure_unique_module_name(*, class_info: Class, schemas: Schemas, config: Config) -> Class:
    """Give a class a module name that no other schema in this document is using.

    Different class names can be turned into the same module name, since module names are snake_case versions of
    class names (`VLAN` and `Vlan` both become `vlan`). Without this, both classes would be generated into the same
    module, where the second one silently overwrites the first one and the `models` package fails to import.

    Args:
        class_info: The class for which a module name is needed.
        schemas: Existing Schemas which have already been processed (to check module name conflicts).
        config: Config data for this run of the generator, used for renaming.

    Returns:
        Either `class_info` unchanged, or a copy of it with a unique module name.
    """
    if class_info.name in schemas.classes_by_name:
        # Classes with the same name conflict in a more fundamental way, which the callers already report;
        # renaming their module would not help and would make the error messages harder to understand.
        return class_info

    used_module_names: set[str] = set()
    for existing in schemas.classes_by_name.values():
        # Only models and enums have a module of their own; `getattr` is used instead of an `isinstance` check
        # because importing those property classes here would be circular.
        existing_class_info = getattr(existing, "class_info", None)
        if isinstance(existing_class_info, Class):
            used_module_names.add(existing_class_info.module_name)

    module_name = class_info.module_name
    if module_name not in used_module_names:
        return class_info

    suffix = 1
    while f"{module_name}_{suffix}" in used_module_names:
        suffix += 1
    new_module_name = PythonIdentifier(f"{module_name}_{suffix}", config.field_prefix)
    schemas.errors.append(
        ParseError(
            header="Renamed a conflicting module",
            detail=(
                f"The module name `{module_name}` is already used by another schema, so `{class_info.name}` "
                f"will be generated in `{new_module_name}.py` instead of overwriting it."
            ),
        )
    )
    return evolve(class_info, module_name=new_module_name)


def update_schemas_with_data(
    *, ref_path: ReferencePath, data: oai.Schema, schemas: Schemas, config: Config
) -> Schemas | PropertyError:
    """
    Update a `Schemas` using some new reference.

    Args:
        ref_path: The output of `parse_reference_path` (validated $ref).
        data: The schema of the thing to add to Schemas.
        schemas: `Schemas` up until now.
        config: User-provided config for overriding default behavior.

    Returns:
        Either the updated `schemas` input or a `PropertyError` if something went wrong.

    See Also:
        - https://swagger.io/docs/specification/using-ref/
    """
    from . import property_from_data  # noqa: PLC0415

    prop: PropertyError | Property
    prop, schemas = property_from_data(
        data=data,
        name=ref_path,
        schemas=schemas,
        required=True,
        parent_name="",
        config=config,
        # Don't process ModelProperty properties because schemas are still being created
        process_properties=False,
        roots={ref_path},
    )

    if isinstance(prop, PropertyError):
        detail = f"{prop.header}: {prop.detail}" if prop.detail is not None else prop.header
        prop.header = f"Unable to parse schema {ref_path.get_untrusted_value()}"
        if isinstance(prop.data, oai.Reference) and prop.data.ref.endswith(
            ref_path.get_untrusted_value()
        ):  # pragma: nocover
            detail += (
                "\n\nRecursive and circular references are not supported directly in an array schema's 'items' section"
            )
        prop.detail = detail
        return prop

    schemas = evolve(schemas, classes_by_reference={ref_path: prop, **schemas.classes_by_reference})
    return schemas


@define
class Parameters:
    """Structure for containing all defined, shareable, and reusable parameters"""

    classes_by_reference: dict[ReferencePath, Parameter] = field(factory=dict)
    classes_by_name: dict[ClassName, Parameter] = field(factory=dict)
    errors: list[ParseError] = field(factory=list)


def parameter_from_data(
    *,
    name: UntrustedString,
    data: oai.Reference | oai.Parameter,
    parameters: Parameters,
    config: Config,
) -> tuple[Parameter | ParameterError, Parameters]:
    """Generates parameters from an OpenAPI Parameter spec."""

    if isinstance(data, oai.Reference):
        return ParameterError("Unable to resolve another reference"), parameters

    if data.param_schema is None:
        return ParameterError("Parameter has no schema"), parameters

    new_param = Parameter(
        name=name.get_untrusted_value(),
        required=data.required,
        explode=data.explode,
        style=data.style.get_untrusted_value() if data.style is not None else None,
        param_schema=data.param_schema,
        param_in=data.param_in,
    )
    parameters = evolve(
        parameters, classes_by_name={**parameters.classes_by_name, ClassName(name, config.field_prefix): new_param}
    )
    return new_param, parameters


def update_parameters_with_data(
    *, ref_path: ReferencePath, data: oai.Parameter, parameters: Parameters, config: Config
) -> Parameters | ParameterError:
    """
    Update a `Parameters` using some new reference.

    Args:
        ref_path: The output of `parse_reference_path` (validated $ref).
        data: The schema of the thing to add to Schemas.
        parameters: `Parameters` up until now.

    Returns:
        Either the updated `parameters` input or a `PropertyError` if something went wrong.

    See Also:
        - https://swagger.io/docs/specification/using-ref/
    """
    param, parameters = parameter_from_data(data=data, name=data.name, parameters=parameters, config=config)

    if isinstance(param, ParameterError):  # pragma: no cover
        param.detail = f"{param.header}: {param.detail}"
        param.header = f"Unable to parse parameter {ref_path.get_untrusted_value()}"
        if isinstance(param.data, oai.Reference) and param.data.ref.endswith(
            ref_path.get_untrusted_value()
        ):  # pragma: nocover
            param.detail += (
                "\n\nRecursive and circular references are not supported. "
                "See https://github.com/openapi-generators/openapi-python-client/issues/466"
            )
        return param

    parameters = evolve(parameters, classes_by_reference={ref_path: param, **parameters.classes_by_reference})
    return parameters


def parameter_from_reference(
    *,
    param: oai.Reference | Parameter,
    parameters: Parameters,
) -> Parameter | ParameterError:
    """
    Returns a Parameter from a Reference or the Parameter itself if one was provided.

    Args:
        param: A parameter by `Reference`.
        parameters: `Parameters` up until now.

    Returns:
        Either the updated `schemas` input or a `PropertyError` if something went wrong.

    See Also:
        - https://swagger.io/docs/specification/using-ref/
    """
    if isinstance(param, Parameter):
        return param

    ref_path = parse_reference_path(param.ref)

    if isinstance(ref_path, ParseError):
        return ParameterError(detail=ref_path.detail)

    _resolved_parameter_class = parameters.classes_by_reference.get(ref_path, None)
    if _resolved_parameter_class is None:
        return ParameterError(detail=f"Reference `{ref_path.get_untrusted_value()}` not found.")
    return _resolved_parameter_class
