## The `generated_code_live_tests` module

These are end-to-end tests which run the code generator command, but unlike the other tests in `end_to_end_tests`, they are also unit tests _of the behavior of the generated code_.

Each test class follows this pattern:

- Use the decorator `@with_generated_client_fixture`, providing an inline API spec (JSON or YAML) that contains whatever schemas/paths/etc. are relevant to this test class. 
  - The spec can omit the `openapi:` and `info:` blocks, unless those are relevant to the test.
  - The decorator creates a temporary file for the inline spec and a temporary directory for the generated code, and runs the client generator.
  - It creates a `GeneratedClientContext` object (defined in `end_to_end_test_helpers.py`) to keep track of things like the location of the generated code and the output of the generator command.
  - This object is injected into the test class as a fixture called `generated_client`, although most tests will not need to reference the fixture directly.
  - `sys.path` is temporarily changed, for the scope of this test class, to allow imports from the generated code.
- Use the decorator `@with_generated_code_import` to make classes or functions from the generated code available to the tests.
  - `@with_generated_code_import(".models.MyModel")` would execute `from [client package name].models import MyModel` and inject the imported object into the test class as a fixture called `MyModel`.
  - `@with_generated_code_import(".models.MyModel", alias="model1")` would do the same thing, but the fixture would be named `model1`.
  - After the test class finishes, these imports are discarded.

Example:

```python

@with_generated_client_fixture(
"""
paths: {}
components:
  schemas:
    MyModel:
      type: object
      properties:
        stringProp: {"type": "string"}
""")
@with_generated_code_import(".models.MyModel")
class TestSimpleJsonObject:
    def test_encoding(MyModel):
        instance = MyModel(string_prop="abc")
        assert instance.to_dict() == {"stringProp": "abc"}
```
