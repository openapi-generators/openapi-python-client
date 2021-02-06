import hashlib
from typing import Any, Dict, Generator, List, Tuple, Union, cast

from .reference import Reference
from .resolver_types import SchemaData


class ResolvedSchema:
    def __init__(self, root: SchemaData, refs: Dict[str, SchemaData], errors: List[str]):
        self._root: SchemaData = root
        self._refs: Dict[str, SchemaData] = refs
        self._errors: List[str] = errors
        self._resolved_remotes_components: SchemaData = cast(SchemaData, {})

        self._resolved_schema: SchemaData = cast(SchemaData, {})
        if len(self._errors) == 0:
            self._process()

    @property
    def schema(self) -> SchemaData:
        return self._root

    @property
    def errors(self) -> List[str]:
        return self._errors.copy()

    def _process(self) -> None:
        self._process_remote_paths()
        self._process_remote_components(self._root)
        self._root.update(self._resolved_remotes_components)

    def _process_remote_paths(self) -> None:
        refs_to_replace = []
        for owner, ref_key, ref_val in self._lookup_schema_references_in(self._root, "paths"):
            ref = Reference(ref_val)

            if ref.is_local_ref():
                continue

            remote_path = ref.remote_relative_path
            path = ref.path

            if remote_path not in self._refs:
                self._errors.append("Failed to resolve remote reference > {0}".format(remote_path))
            else:
                remote_schema = self._refs[remote_path]
                remote_value = self._lookup_dict(remote_schema, path)
                if not remote_value:
                    self._errors.append("Failed to read remote value {}, in remote ref {}".format(path, remote_path))
                else:
                    refs_to_replace.append((owner, remote_schema, remote_value))

        for owner, remote_schema, remote_value in refs_to_replace:
            self._process_remote_components(remote_schema, remote_value, 1)
            self._replace_reference_with(owner, remote_value)

    def _process_remote_components(
        self, owner: SchemaData, subpart: Union[SchemaData, None] = None, depth: int = 0
    ) -> None:
        target = subpart if subpart else owner

        for parent, ref_key, ref_val in self._lookup_schema_references(target):
            ref = Reference(ref_val)

            if ref.is_local_ref():
                # print('Found local reference >> {0}'.format(ref.value))
                if depth > 0:
                    self._transform_to_local_components(owner, ref)
            else:
                remote_path = ref.remote_relative_path
                if remote_path not in self._refs:
                    self._errors.append("Failed to resolve remote reference > {0}".format(remote_path))
                else:
                    remote_owner = self._refs[remote_path]
                    self._transform_to_local_components(remote_owner, ref)
                    self._transform_to_local_ref(parent, ref)

    def _transform_to_local_components(self, owner: SchemaData, ref: Reference) -> None:
        self._ensure_components_dir_exists(ref)

        # print('Processing remote component > {0}'.format(ref.value))
        remote_component = self._lookup_dict(owner, ref.path)
        root_components_dir = self._lookup_dict(self._resolved_remotes_components, ref.path_parent)
        component_name = ref.path.split("/")[-1]

        if component_name == "SorTransparentContainer" or component_name == "sorTransparentContainer":
            print(ref.value)

        if remote_component is None:
            print("Weirdy relookup of >> {0}".format(ref.value))
            assert ref.is_local_ref() and self._lookup_dict(self._resolved_remotes_components, ref.path)
            return

        if "$ref" in remote_component:
            subref = Reference(remote_component["$ref"])
            if not subref.is_local_ref():
                print("Lookup remote ref >>> {0}".format(subref.value))
                return self._process_remote_components(remote_component)

        if root_components_dir:
            if component_name in root_components_dir:
                local_component_hash = self._reference_schema_hash(root_components_dir[component_name])
                remote_component_hash = self._reference_schema_hash(remote_component)

                if local_component_hash == remote_component_hash:
                    return
                else:
                    pass
                # print('=' * 120)
                # print('TODO: Find compoment collision to handle on >>> {0}'.format(ref.path))
                # print('Local componente {0} >> {1}'.format(local_component_hash, root_components_dir[component_name]))
                # print('')
                # print('Remote componente {0} >> {1}'.format(remote_component_hash, remote_component))
                # print('=' * 120)
            else:
                root_components_dir[component_name] = remote_component
                self._process_remote_components(owner, remote_component, 2)

    def _ensure_components_dir_exists(self, ref: Reference) -> None:
        cursor = self._resolved_remotes_components
        for key in ref.path_parent.split("/"):
            if key == "":
                continue

            if key not in cursor:
                cursor[key] = {}

            cursor = cursor[key]

    def _transform_to_local_ref(self, owner: Dict[str, Any], ref: Reference) -> None:
        owner["$ref"] = "#{0}".format(ref.path)

    def _lookup_dict(self, attr: SchemaData, query: str) -> Union[SchemaData, None]:
        cursor = attr
        query_parts = []

        if query.startswith("/paths"):
            query_parts = ["paths", query.replace("/paths//", "/").replace("/paths", "")]
        else:
            query_parts = query.split("/")

        for key in query_parts:
            if key == "":
                continue

            if isinstance(cursor, dict) and key in cursor:
                cursor = cursor[key]
            else:
                return None
        return cursor

    def _replace_reference_with(self, root: Dict[str, Any], new_value: Dict[str, Any]) -> None:
        for key in new_value:
            root[key] = new_value[key]

        root.pop("$ref")

    def _lookup_schema_references_in(
        self, attr: SchemaData, path: str
    ) -> Generator[Tuple[SchemaData, str, Any], None, None]:
        if not isinstance(attr, dict) or path not in attr:
            return

        yield from self._lookup_schema_references(attr[path])

    def _lookup_schema_references(self, attr: Any) -> Generator[Tuple[SchemaData, str, str], None, None]:
        if isinstance(attr, dict):
            for key, val in attr.items():
                if key == "$ref":
                    yield cast(SchemaData, attr), cast(str, key), cast(str, val)
                else:
                    yield from self._lookup_schema_references(val)

        elif isinstance(attr, list):
            for val in attr:
                yield from self._lookup_schema_references(val)

    def _reference_schema_hash(self, schema: Dict[str, Any]) -> str:
        md5 = hashlib.md5()
        hash_elms = []
        for key in schema.keys():
            if key == "description":
                continue

            if key == "type":
                hash_elms.append(schema[key])

            if key == "allOf":
                for item in schema[key]:
                    hash_elms.append(str(item))

            hash_elms.append(key)

        hash_elms.sort()
        md5.update(";".join(hash_elms).encode("utf-8"))
        return md5.hexdigest()
