__all__ = [
    "AnyProperty",
    "Class",
    "EnumProperty",
    "ModelProperty",
    "Parameters",
    "Property",
    "Schemas",
    "build_schemas",
    "build_parameters",
    "property_from_data",
    "ListProperty",
    "IntProperty",
    "SecurityProperty",
]

from typing import Dict, Iterable, List, Tuple, Union

from ... import Config
from ... import schema as oai
from ... import utils
from ..errors import ParameterError, ParseError, PropertyError
from .enum_property import EnumProperty
from .list_property import ListProperty
from .model_property import ModelProperty, process_model
from .property import Property
from .schemas import (
    Class,
    Parameters,
    ReferencePath,
    Schemas,
    parse_reference_path,
    update_parameters_with_data,
    update_schemas_with_data,
)
from .build import property_from_data
from .types import AnyProperty, IntProperty
from .security_property import SecurityProperty


def _create_schemas(
    *, components: Dict[str, Union[oai.Reference, oai.Schema]], schemas: Schemas, config: Config
) -> Schemas:
    to_process: Iterable[Tuple[str, Union[oai.Reference, oai.Schema]]] = components.items()
    still_making_progress = True
    errors: List[PropertyError] = []
    breakpoint()

    # References could have forward References so keep going as long as we are making progress
    while still_making_progress:
        still_making_progress = False
        errors = []
        next_round = []
        # Only accumulate errors from the last round, since we might fix some along the way
        for name, data in to_process:
            if isinstance(data, oai.Reference):
                schemas.errors.append(PropertyError(data=data, detail="Reference schemas are not supported."))
                continue
            ref_path = parse_reference_path(f"#/components/schemas/{name}")
            if isinstance(ref_path, ParseError):
                schemas.errors.append(PropertyError(detail=ref_path.detail, data=data))
                continue
            schemas_or_err = update_schemas_with_data(ref_path=ref_path, data=data, schemas=schemas, config=config)
            if isinstance(schemas_or_err, PropertyError):
                next_round.append((name, data))
                errors.append(schemas_or_err)
                continue
            schemas = schemas_or_err
            still_making_progress = True
        to_process = next_round

    schemas.errors.extend(errors)
    return schemas


def _propogate_removal(*, root: Union[ReferencePath, utils.ClassName], schemas: Schemas, error: PropertyError) -> None:
    if isinstance(root, utils.ClassName):
        schemas.classes_by_name.pop(root, None)
        return
    if root in schemas.classes_by_reference:
        error.detail = error.detail or ""
        error.detail += f"\n{root}"
        del schemas.classes_by_reference[root]
        for child in schemas.dependencies.get(root, set()):
            _propogate_removal(root=child, schemas=schemas, error=error)


def _process_model_errors(
    model_errors: List[Tuple[ModelProperty, PropertyError]], *, schemas: Schemas
) -> List[PropertyError]:
    for model, error in model_errors:
        error.detail = error.detail or ""
        error.detail += "\n\nFailure to process schema has resulted in the removal of:"
        for root in model.roots:
            _propogate_removal(root=root, schemas=schemas, error=error)
    return [error for _, error in model_errors]


def _process_models(*, schemas: Schemas, config: Config) -> Schemas:
    to_process = (prop for prop in schemas.classes_by_name.values() if isinstance(prop, ModelProperty))
    still_making_progress = True
    final_model_errors: List[Tuple[ModelProperty, PropertyError]] = []
    latest_model_errors: List[Tuple[ModelProperty, PropertyError]] = []

    # Models which refer to other models in their allOf must be processed after their referenced models
    while still_making_progress:
        still_making_progress = False
        # Only accumulate errors from the last round, since we might fix some along the way
        latest_model_errors = []
        next_round = []
        for model_prop in to_process:
            schemas_or_err = process_model(model_prop, schemas=schemas, config=config)
            if isinstance(schemas_or_err, PropertyError):
                schemas_or_err.header = f"\nUnable to process schema {model_prop.name}:"
                if isinstance(schemas_or_err.data, oai.Reference) and schemas_or_err.data.ref.endswith(
                    f"/{model_prop.class_info.name}"
                ):
                    schemas_or_err.detail = schemas_or_err.detail or ""
                    schemas_or_err.detail += "\n\nRecursive allOf reference found"
                    final_model_errors.append((model_prop, schemas_or_err))
                    continue
                latest_model_errors.append((model_prop, schemas_or_err))
                next_round.append(model_prop)
                continue
            schemas = schemas_or_err
            still_making_progress = True
        to_process = (prop for prop in next_round)

    final_model_errors.extend(latest_model_errors)
    errors = _process_model_errors(final_model_errors, schemas=schemas)
    schemas.errors.extend(errors)
    return schemas


def build_schemas(
    *, components: Dict[str, Union[oai.Reference, oai.Schema]], schemas: Schemas, config: Config
) -> Schemas:
    """Get a list of Schemas from an OpenAPI dict"""
    schemas = _create_schemas(components=components, schemas=schemas, config=config)
    schemas = _process_models(schemas=schemas, config=config)
    return schemas


def build_parameters(
    *,
    components: Dict[str, Union[oai.Reference, oai.Parameter]],
    parameters: Parameters,
) -> Parameters:
    """Get a list of Parameters from an OpenAPI dict"""
    to_process: Iterable[Tuple[str, Union[oai.Reference, oai.Parameter]]] = []
    if components is not None:
        to_process = components.items()
    still_making_progress = True
    errors: List[ParameterError] = []

    # References could have forward References so keep going as long as we are making progress
    while still_making_progress:
        still_making_progress = False
        errors = []
        next_round = []
        # Only accumulate errors from the last round, since we might fix some along the way
        for name, data in to_process:
            if isinstance(data, oai.Reference):
                parameters.errors.append(ParameterError(data=data, detail="Reference parameters are not supported."))
                continue
            ref_path = parse_reference_path(f"#/components/parameters/{name}")
            if isinstance(ref_path, ParseError):
                parameters.errors.append(ParameterError(detail=ref_path.detail, data=data))
                continue
            parameters_or_err = update_parameters_with_data(ref_path=ref_path, data=data, parameters=parameters)
            if isinstance(parameters_or_err, ParameterError):
                next_round.append((name, data))
                errors.append(parameters_or_err)
                continue
            parameters = parameters_or_err
            still_making_progress = True
        to_process = next_round

    parameters.errors.extend(errors)
    return parameters
