---
default: minor
---

# OpenAPI 3.1 support

The generator will now attempt to generate code for OpenAPI documents with versions 3.1.x (previously, it would exit immediately on seeing a version other than 3.0.x). The following specific OpenAPI 3.1 features are now supported:

- `null` as a type
- Arrays of types (e.g., `type: [string, null]`)
- `const` (defines `Literal` types)

The generator does not currently validate that the OpenAPI document is valid for a specific version of OpenAPI, so it may be possible to generate code for documents that include both removed 3.0 syntax (e.g., `nullable`) and new 3.1 syntax (e.g., `null` as a type).

Thanks to everyone who helped make this possible with discussions and testing, including:

- @frco9
- @vogre
- @naddeoa
- @staticdev
- @philsturgeon
- @johnthagen
