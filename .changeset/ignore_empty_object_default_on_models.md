---
default: patch
---

# Do not drop a schema over an empty object default

A property whose type is a model schema could not carry `default: {}`. The parser rejected it with `ModelProperty cannot have a default value`, or with `Value {} is not valid, only None is allowed` when the model sat in a union. The generator warned, dropped the enclosing schema and every endpoint that referenced it, and still exited 0.

An empty object carries no information for a model default, so it is now ignored and the property generates with no default. This is how an inline `default: {}` on a property and a bare `$ref` with a sibling `default` already behave. A non-empty default is still rejected.
