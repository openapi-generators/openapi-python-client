---
default: patch
---

# Fix duplicate model error for nullable top-level object schemas

A schema in `components/schemas` with `type: ["object", "null"]` and a nested model, such as a property that is itself a nullable object, was dropped with "Attempted to generate duplicate models". The nested model was built twice because union variants ignored the deferred processing used while schemas are created. Variants are now built once.
