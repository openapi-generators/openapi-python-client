---
default: major
---

# For custom templates, changed type of endpoint parameters

**This does not affect projects that are not using `--custom-template-path`**

The type of these properties on `Endpoint` has been changed from `Dict[str, Property]` to `List[Property]`:

- `path_parameters`
- `query_parameters`
- `header_parameters`
- `cookie_parameters`

If your templates are very close to the default templates, you can probably just remove `.values()` anywhere it appears.

The type of `iter_all_parameters()` is also different, you probably want `list_all_parameters()` instead.
