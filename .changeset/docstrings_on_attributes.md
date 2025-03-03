---
default: minor
---

# Add `docstrings_on_attributes` config setting

Setting this option to `true` changes the docstring behavior in model classes: for any attribute that have a non-empty `description`, instead of describing the attribute as part of the class's docstring, the description will appear in an individual docstring for that attribute.
