"""Test-only shim of the private ``tandem_platform`` package.

This is **not** the real implementation. It exists solely so the generator's own
test suite (functional tests that import generated code, and the ``mypy --strict``
checks in the end-to-end tests) can run without access to Tandem's internal
package or its cloudsmith index. See ``tandem_platform.schema.protected`` for the
symbols the generated clients depend on.
"""
