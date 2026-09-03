---
default: patch
---

# Treat `type: array` without `items` as a list of Any

An array schema with neither `items` nor `prefixItems` is valid in JSON Schema
2020-12 (OpenAPI 3.1) and means "array of any type". Previously the generator
failed such schemas with a `PropertyError` ("type array must have items or
prefixItems defined"), silently skipping the property or `anyOf` branch. It now
generates a `list[Any]`, equivalent to `items: {}`.
