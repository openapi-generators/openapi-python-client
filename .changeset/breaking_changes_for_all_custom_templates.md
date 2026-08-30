---
default: note
---

# Breaking changes for all custom templates

**ALL** custom templates are expected to break with this version as a result of the security fix.

1. The `utils` global has been renamed to `strings`
2. Most string values can no longer be rendered directly into templates, 
   you must describe how the value is being used so it can be properly escaped using either a Python function or Jinja filter:
   1. `strings.snake_case()` / `| snakecase` (existing)
   2. `strings.kebab_case()` /  `| kebabcase` (existing)
   3. `strings.pascal_case()` / `| pascalcase` (existing)
   4. `python_identifier()` (existing)
   5. `class_name()` (existing)
   6. `strings.safe_for_docstring()` / `| safe_for_docstring` for values which get injected into a `"""` docstring
   7. `strings.in_f_string_literal()` / `| in_f_string_literal` for values that go into `f""` f-strings
   8. `strings.in_double_quote_literal()` / `| in_double_quote_literal` for values that go into **non-f-string** `""` literals
   9. `.as_unembedded_code()` / `| as_unembedded_code` ONLY for `PythonCode` values—those that are intended to be Python code which is not embedded into any string/docstring. Examples include usages of `.python_code`, `.get_type_string()`, `.get_instance_type_string()`, `.get_type_strings_in_union()`. You *should not* assume these values are safe to put in docstrings, string literals, or f-string literals. Use the dedicated helpers for those.
As always, you can check the diff of the built in templates for examples. You will also want to check generated output 
for "UntrustedString", which is how any string now requiring one of those functions will appear.
