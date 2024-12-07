---
default: patch
---

# Fix class generation for some union types

Fixed issue #1120, where certain combinations of types-- such as a `oneOf` between a model or an enum and null, or the OpenAPI 3.0 equivalent of using `nullable: true`-- could cause unnecessary suffixes like "Type0" to be added to the class name, and/or could cause extra copies of the class to be generated.
