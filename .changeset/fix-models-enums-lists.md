---
default: patch
---

# Make lists of models and enums work correctly in custom templates

Lists of model and enum classes should be available to custom templates via the Jinja
variables `openapi.models` and `openapi.enums`, but these were being passed in a way that made
them always appear empty. This has been fixed so a custom template can now iterate over them.

Closes #1188.
