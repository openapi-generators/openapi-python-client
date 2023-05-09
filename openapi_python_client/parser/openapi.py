from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Optional, Union
from itertools import chain

from .. import schema as oai

# from ..schema.openapi_schema_pydantic.security_scheme import SecurityScheme
from .security_schemes import SecurityScheme
from .. import utils
from ..config import Config
from .errors import GeneratorError, ParseError
from .properties import (
    EnumProperty,
    ModelProperty,
    Parameters,
    Schemas,
    build_parameters,
    build_schemas,
    SecurityProperty,
    CredentialsProperty,
    build_credentials_property,
)
from .endpoint_collection import EndpointCollection
from .endpoints import Endpoint
from .properties import property_from_data


@dataclass
class GeneratorData:
    """All the data needed to generate a client"""

    title: str
    description: Optional[str]
    version: str
    models: Iterator[ModelProperty]
    errors: List[ParseError]
    endpoint_collections_by_tag: Dict[utils.PythonIdentifier, EndpointCollection]
    enums: Iterator[EnumProperty]
    security_schemes: Dict[str, SecurityProperty]
    credentials: CredentialsProperty
    openapi: oai.OpenAPI

    @property
    def all_endpoints(self) -> List[Endpoint]:
        """List of all endpoints in the spec"""
        return list(
            chain.from_iterable(collection.endpoints for collection in self.endpoint_collections_by_tag.values())
        )

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
            name="credentials", security_properties=list(security_schemes.values()), config=config
        )
        if openapi.components and openapi.components.schemas:
            schemas = build_schemas(components=openapi.components.schemas, schemas=schemas, config=config)
        if openapi.components and openapi.components.parameters:
            parameters = build_parameters(components=openapi.components.parameters, parameters=parameters)
        endpoint_collections_by_tag, schemas, parameters = EndpointCollection.from_data(
            data=openapi.paths, schemas=schemas, parameters=parameters, security_schemes=security_schemes, config=config
        )

        enums = (prop for prop in schemas.classes_by_name.values() if isinstance(prop, EnumProperty))
        models = (prop for prop in schemas.classes_by_name.values() if isinstance(prop, ModelProperty))

        return GeneratorData(
            title=openapi.info.title,
            description=openapi.info.description,
            version=openapi.info.version,
            endpoint_collections_by_tag=endpoint_collections_by_tag,
            models=models,
            errors=schemas.errors + parameters.errors,
            enums=enums,
            security_schemes=security_schemes,
            openapi=openapi,
            credentials=credentials,
        )
