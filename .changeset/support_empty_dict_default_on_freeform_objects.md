---
default: patch
---

# Support `default: {}` on freeform object schemas

A schema declared as `type: object` with `additionalProperties: true` and no declared properties (often appearing inside an `anyOf` with `null`) could not carry a `default: {}`. The parser rejected the default with `ModelProperty cannot have a default value`, which silently dropped the enclosing schema and every endpoint that referenced it.

The default `{}` is now accepted on such freeform models and generates an empty-container initializer. The imports of inner models with a non-`None` default are also promoted from lazy `TYPE_CHECKING` imports to runtime imports, so the generated default expression resolves correctly at class-definition time.
