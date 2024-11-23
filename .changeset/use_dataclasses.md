---
default: minor
---

# Add `use_dataclasses` config setting

Instead of using the `attrs` package in the generated code, you can choose to use the built-in `dataclasses` module by setting `use_dataclasses: true` in your config file. This may be useful if you are trying to reduce external dependencies, or if your client package might be used in applications that require different versions of `attrs`.

The generated client code should behave exactly the same from an application's point of view except for the following differences:

- The generated project file does not have an `attrs` dependency.
- If you were using `attrs.evolve` to create an updated instance of a model class, you should use `dataclasses.replace` instead.
- Undocumented attributes of the `Client` class that had an underscore prefix in their names are no longer available.
- The builder methods `with_cookies`, `with_headers`, and `with_timeout` do _not_ modify any Httpx client that may have been created from the previous Client instance; they affect only the new instance.
