---
default: patch
---

# Fix overriding of object property class

Fixed issue #1123, in which a property could end up with the wrong type when combining two object schemas with `allOf`, if the type of the property was itself an object but had a different schema in each. Previously, if the property's type was A in the first schema and B in the second, the resulting schema would use type A for the property.

The new behavior is, that the generator will test whether one of the types A/B is derived from the other. "Derived" here means that the result of `allOf[A, B]` would be exactly identical to B. If so, it will use the class name of B. If not, it will attempt to merge A and B with the usual `allOf` logic to create a new inline schema.
