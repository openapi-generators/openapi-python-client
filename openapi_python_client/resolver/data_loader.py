import yaml

from .resolver_types import SchemaData


class DataLoader:
    @classmethod
    def load(cls, path: str, data: bytes) -> SchemaData:
        data_type = path.split(".")[-1].casefold()

        if data_type == "json":
            return cls.load_json(data)
        else:
            return cls.load_yaml(data)

    @classmethod
    def load_json(cls, data: bytes) -> SchemaData:
        raise NotImplementedError()

    @classmethod
    def load_yaml(cls, data: bytes) -> SchemaData:
        return yaml.safe_load(data)
