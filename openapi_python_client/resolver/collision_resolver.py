import hashlib
from typing import Any, Dict, List, Tuple

from .reference import Reference
from .resolver_types import SchemaData


class CollisionResolver:
    def __init__(self, root: SchemaData, refs: Dict[str, SchemaData], errors: List[str], parent: str):
        self._root: SchemaData = root
        self._refs: Dict[str, SchemaData] = refs
        self._errors: List[str] = errors
        self._parent = parent
        self._refs_index: Dict[str, str] = dict()
        self._keys_to_replace: Dict[Reference, Tuple[int, SchemaData]] = dict()
        self._debug = set()

    def _browse_schema(self, attr: Any, root_attr: Any) -> None:
        if isinstance(attr, dict):
            attr_copy = {**attr}  # Create a shallow copy
            for key, val in attr_copy.items():
                if key == "$ref":
                    ref = Reference(val, self._parent)
                    value = ref.pointer.value

                    assert value

                    schema = self._get_from_ref(ref, root_attr)
                    # if value == '/components/schemas/EeSubscription':
                    #     print(schema)
                    #     print()
                    hashed_schema = self._reference_schema_hash(schema)

                    if value in self._refs_index.keys():
                        if self._refs_index[value] != hashed_schema:
                            self._debug.add(ref.pointer.value)
                            if ref.is_local():
                                self._increment_ref(ref, root_attr, hashed_schema, attr, key)
                            else:
                                assert ref.abs_path in self._refs.keys()
                                self._increment_ref(ref, self._refs[ref.abs_path], hashed_schema, attr, key)
                    else:
                        self._refs_index[value] = hashed_schema
                else:
                    self._browse_schema(val, root_attr)

        elif isinstance(attr, list):
            for val in attr:
                self._browse_schema(val, root_attr)

    def _get_from_ref(self, ref: Reference, attr: SchemaData) -> SchemaData:
        if ref.is_local():
            cursor = attr
        else:
            assert ref.abs_path in self._refs.keys()
            cursor = self._refs[ref.abs_path]
        query = ref.pointer.unescapated_value
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
                print('ERROR')

        # if list(cursor) == ['$ref']:
        #     ref = Reference(cursor['$ref'],self._parent)
        #     if ref.is_remote():
        #         print('remote_ref')
        #         print(ref.value)
        #         attr = self._refs[ref.abs_path]
        #     return self._get_from_ref(ref,attr)

        return cursor

    def _increment_ref(
        self, ref: Reference, schema: SchemaData, hashed_schema: str, attr: Dict[str, Any], key: str
    ) -> None:
        i = 2
        value = ref.pointer.value
        incremented_value = value + "_" + str(i)

        while incremented_value in self._refs_index.keys():
            if self._refs_index[incremented_value] == hashed_schema:
                attr[key] = ref.value + "_" + str(i)
                return
            else:
                i = i + 1
                incremented_value = value + "_" + str(i)

        attr[key] = ref.value + "_" + str(i)
        self._refs_index[incremented_value] = hashed_schema
        self._keys_to_replace[ref] = (i, schema)

    def _modify_root_ref_name(self, ref_pointer: str, i: int, attr: SchemaData) -> None:
        cursor = attr
        query = ref_pointer
        query_parts = []

        if query.startswith("/paths"):
            query_parts = ["paths", query.replace("/paths//", "/").replace("/paths", "")]
        else:
            query_parts = query.split("/")

        last_key = query_parts[-1]

        for key in query_parts:
            if key == "":
                continue

            if key == last_key:
                assert key in cursor
                cursor[key + "_" + str(i)] = cursor.pop(key)
                return

            if isinstance(cursor, dict) and key in cursor:
                cursor = cursor[key]
            else:
                return

    def resolve(self) -> None:
        debug = set()
        self._browse_schema(self._root, self._root)
        for file, schema in self._refs.items():
            self._browse_schema(schema, schema)
        for a, b in self._keys_to_replace.items():
            debug.add(a.pointer.value)
            self._modify_root_ref_name(a.pointer.value, b[0], b[1])

        print(self._debug)

    def _reference_schema_hash(self, schema: Dict[str, Any]) -> str:
        md5 = hashlib.md5()
        hash_elms = []
        for key in schema.keys():
            if key == "description":
                hash_elms.append(schema[key])
            if key == "type":
                hash_elms.append(schema[key])
            if key == "allOf":
                for item in schema[key]:
                    hash_elms.append(str(item))

            hash_elms.append(key)

        hash_elms.sort()
        md5.update(";".join(hash_elms).encode("utf-8"))
        return md5.hexdigest()
