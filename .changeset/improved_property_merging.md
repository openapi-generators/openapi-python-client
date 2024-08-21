---
default: minor
---

# Improved property-merging behavior with `allOf`

When using `allOf` to extend a base object type, `openapi-python-client` is now able to handle some kinds of modifications to an existing property that would have previously caused an error:

- Overriding attributes that do not affect validation, such as `description`.
- Specifying stricter validation for the same type, such as setting a `maxLength` for a string that previously had no max length (or previously had a larger max length), or setting a `pattern` regex for a string that previously had none.
- Changing a nonspecific numeric type to `int`.
- Changing a property from `any` to a specific type.
