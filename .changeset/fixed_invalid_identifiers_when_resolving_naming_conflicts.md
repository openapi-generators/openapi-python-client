---
default: patch
---

# Fixed invalid Python identifiers when resolving naming conflicts

When two property or parameter names conflicted after conversion to `snake_case` (e.g. `foo-bar` and `fooBar`), the conflict-resolution path preserved delimiters like `-`, `.`, and spaces in the generated Python identifiers, producing invalid code which failed generation. Conflicting names now keep their original casing but have any characters which are invalid in Python identifiers stripped (e.g. `foobar` and `fooBar`).
