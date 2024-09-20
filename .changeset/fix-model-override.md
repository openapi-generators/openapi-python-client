---
default: patch
---

# Fix overriding of object property class

Fixed issue #1121, where redefining an object property within an `allOf` would not use the correct class name if the property's type was changed from one object type to another.
