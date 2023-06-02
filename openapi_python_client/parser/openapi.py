from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Optional, Union

from .. import schema as oai
from ..config import Config
from .endpoint_collection import Endpoints
from .endpoints import Endpoint
from .errors import GeneratorError, ParseError
from .properties import (
    CredentialsProperty,
    EnumProperty,
    ModelProperty,
    Parameters,
    Schemas,
    SecurityProperty,
    build_credentials_property,
    build_parameters,
    build_schemas,
    property_from_data,
    process_model,
    PropertyError,
)


@dataclass
class GeneratorData:
    """All the data needed to generate a client"""

    title: str
    description: Optional[str]
    version: str
    models: Iterator[ModelProperty]
    errors: List[ParseError]
    # endpoint_collections_by_tag: Dict[utils.PythonIdentifier, EndpointCollection]
    endpoints: Endpoints
    enums: Iterator[EnumProperty]
    security_schemes: Dict[str, SecurityProperty]
    credentials: CredentialsProperty
    openapi: oai.OpenAPI

    @property
    def all_endpoints(self) -> List[Endpoint]:
        """List of all endpoints in the spec"""
        return list(self.endpoints.endpoints_by_name.values())

    @staticmethod
    def from_dict(data: Dict[str, Any], *, config: Config) -> Union["GeneratorData", GeneratorError]:
        """Create an OpenAPI from dict"""
        openapi = oai.OpenAPI.parse_obj(data)
        schemas = Schemas()
        parameters = Parameters()
        if openapi.components and openapi.components.securitySchemes:
            security_schemes_raw = openapi.components.securitySchemes
        else:
            security_schemes_raw = {}
        # security_schemes = {
        #     key: SecurityScheme(
        #         scheme=value, name=key, class_name=utils.ClassName(key + "Credentials", config.field_prefix)
        #     )
        #     for key, value in security_schemes_raw.items()
        # }
        security_schemes = {  # TODO: property_from_data is tuple (result, error)
            key: property_from_data(
                name=key, required=True, data=value, schemas=schemas, parent_name="", config=config
            )[0]
            for key, value in security_schemes_raw.items()
        }
        credentials = build_credentials_property(  # Property for all credentials
            name="credentials",
            security_properties=list(security_schemes.values()),  # type: ignore[arg-type]
            config=config,
        )
        property_errors: List[PropertyError] = []
        if openapi.components and openapi.components.schemas:
            schemas = build_schemas(components=openapi.components.schemas, schemas=schemas, config=config)
            # In the first pass of build_schemas model properties are not resolved from references
            # This populates fields in required/optional properties on the models
            for model in list(schemas.classes_by_name.values()):
                if not isinstance(model, ModelProperty):
                    continue
                schemas_or_err = process_model(model, schemas=schemas, config=config)
                if isinstance(schemas_or_err, PropertyError):
                    property_errors.append(schemas_or_err)
                else:
                    schemas = schemas_or_err
        if openapi.components and openapi.components.parameters:
            parameters = build_parameters(components=openapi.components.parameters, parameters=parameters)
        endpoints, schemas, parameters = Endpoints.from_data(
            # endpoint_collections_by_tag, schemas, parameters = EndpointCollection.from_data(
            data=openapi.paths,
            schemas=schemas,
            parameters=parameters,
            # TODO: Typing
            security_schemes=security_schemes,  # type: ignore[arg-type]
            config=config,
        )

        enums = (prop for prop in schemas.classes_by_name.values() if isinstance(prop, EnumProperty))
        models = (prop for prop in schemas.classes_by_name.values() if isinstance(prop, ModelProperty))

        return GeneratorData(
            title=openapi.info.title,
            description=openapi.info.description,
            version=openapi.info.version,
            endpoints=endpoints,
            # endpoint_collections_by_tag=endpoint_collections_by_tag,
            models=models,
            errors=schemas.errors + parameters.errors,
            enums=enums,
            security_schemes=security_schemes,  # type: ignore[arg-type]
            openapi=openapi,
            credentials=credentials,
        )
