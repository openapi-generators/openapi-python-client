---
default: patch
---

# Fix `const` variants in `anyOf`/`oneOf` unions

Fixes #1263

A union with a `const` member that wasn't the last option generated broken parsing code: the const check ran unguarded and returned (or raised) before the other variants were tried. For a response like `anyOf: [{const: "x"}, {$ref: ...}]` the model branch was unreachable, and for a model property like `anyOf: [{const: "auto"}, {type: integer}]` any integer raised a `ValueError`. Const members now get the same type check and fallthrough as every other union member.

This also fixes `to_multipart()` for models with a `const` inside a union, which used to raise `TypeError: Subscripted generics cannot be used with class and instance checks`.
