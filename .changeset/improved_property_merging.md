---
default: minor
---

# Improved property-merging behavior with `allOf`

When using `allOf` to extend a base object type, `openapi-python-client` is now able to handle some kinds of modifications to an existing property that would have previously caused an error:

- Overriding attributes that do not affect validation, such as `description`.
- Combining properties that this generator ignores, like `maxLength` or `pattern`.
- Combining a generic numeric type with `int` (resulting in `int`).
- Adding a `format` to a string.
- Combining `any` with a specific type (resulting in that specific type).

> [!NOTE]
> `pattern` and `max_length` are no longer fields on `StringProperty`, which may impact custom templates.
