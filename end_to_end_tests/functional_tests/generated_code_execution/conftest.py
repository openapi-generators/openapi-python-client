"""Mark functional tests that are blocked by deliberate fork redesigns.

These tests come from upstream and assert the *pre-fork* behavior. They are not
failing because of the rebase or a bug — they fail because this fork intentionally
changed the generated client's API and model contract. They are marked here (rather
than deleted) so the divergence stays visible; remove the relevant entry once the
corresponding test has been rewritten to the fork's contract.

Three buckets:

1. Async-only endpoints (commit "only generate async stream"): endpoint modules now
   expose only ``request``/``_request_detailed``. Upstream tests import
   ``sync``/``sync_detailed``/``asyncio``/``asyncio_detailed``, which are no longer
   generated, so the class-scoped import fixtures raise at setup. We ``skip`` these
   (xfail can't reliably catch a fixture-setup error).

2. Pydantic ``X | None`` field typing instead of upstream's ``X | Unset`` — the
   ``test_type_hints`` assertions.

3. Pydantic validation/serialization semantics — strict ``from_dict`` raises
   ``ValidationError`` on missing required fields, datetimes serialize as ``...Z``,
   literal-enum validation and ``extra="allow"`` equality differ.
"""

import pytest

# Bucket 1 — whole classes error at fixture setup; skip the entire class.
_SKIP_ASYNC_ONLY_ENDPOINTS = (
    "test_docstrings.py::TestEndpointDocstrings",
    "test_path_parameters.py::TestPathParameterEncoding",
)

# Bucket 2 — optional fields are `X | None`, not `X | Unset`.
_XFAIL_TYPE_HINT_CONTRACT = (
    "test_arrays.py::TestArraySchemas::test_type_hints",
    "test_arrays.py::TestArraysWithPrefixItems::test_type_hints",
    "test_enums_and_consts.py::TestIntEnumClass::test_type_hints",
    "test_enums_and_consts.py::TestIntLiteralEnum::test_type_hints",
    "test_enums_and_consts.py::TestNullableEnums::test_type_hints",
    "test_enums_and_consts.py::TestStringEnumClass::test_type_hints",
    "test_enums_and_consts.py::TestStringLiteralEnum::test_type_hints",
    "test_properties.py::TestBasicModelProperties::test_type_hints",
    "test_properties.py::TestRequiredAndOptionalProperties::test_type_hints",
    "test_properties.py::TestSpecialStringFormats::test_type_hints",
    "test_unions.py::TestOneOf::test_type_hints",
    "test_unions.py::TestSimpleTypeList::test_type_hints",
)

# Bucket 3 — Pydantic validation/serialization differs from attrs.
_XFAIL_VALIDATION_SERIALIZATION = (
    "test_enums_and_consts.py::TestIntLiteralEnum::test_invalid_values",
    "test_enums_and_consts.py::TestStringLiteralEnum::test_invalid_values",
    "test_enums_and_consts.py::TestNullableLiteralEnum::test_nullable_enum_prop",
    "test_properties.py::TestBasicModelProperties::test_decode_encode",
    "test_properties.py::TestRequiredAndOptionalProperties::test_required_missing",
    "test_properties.py::TestSpecialStringFormats::test_date_time",
)

_SKIP_REASON = (
    "Fork generates async-only endpoints (`request`/`_request_detailed`); upstream test "
    "imports sync/asyncio/*_detailed which are no longer generated. Rewrite for the "
    "async-only API to re-enable."
)
_XFAIL_TYPE_HINT_REASON = (
    "Fork's Pydantic models type optional fields as `X | None`, not upstream's `X | Unset`."
)
_XFAIL_VALIDATION_REASON = (
    "Fork's Pydantic models use strict validation/serialization (ValidationError on missing "
    "required, datetime `...Z`, literal-enum validation, extra=allow equality) vs upstream attrs."
)


def pytest_collection_modifyitems(config, items):
    for item in items:
        nodeid = item.nodeid
        if any(key in nodeid for key in _SKIP_ASYNC_ONLY_ENDPOINTS):
            item.add_marker(pytest.mark.skip(reason=_SKIP_REASON))
        elif any(key in nodeid for key in _XFAIL_TYPE_HINT_CONTRACT):
            item.add_marker(pytest.mark.xfail(reason=_XFAIL_TYPE_HINT_REASON, strict=False))
        elif any(key in nodeid for key in _XFAIL_VALIDATION_SERIALIZATION):
            item.add_marker(pytest.mark.xfail(reason=_XFAIL_VALIDATION_REASON, strict=False))
