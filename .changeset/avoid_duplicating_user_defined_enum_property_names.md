---
default: major
---

# Avoid duplicating user-defined enum property names

#1168 by @wileykestner

The generator will now create names for properties gauranteed to avoid colliding with the names of other existing, user-defined types.

Resolves #1167
