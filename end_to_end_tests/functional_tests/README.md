## The `functional_tests` module

These are end-to-end tests which run the client generator against many small API documents that are specific to various test cases.

Rather than testing low-level implementation details (like the unit tests in `tests`), or making assertions about the exact content of the generated code (like the "golden record"-based end-to-end tests), these treat both the generator and the generated code as black boxes and make assertions about their behavior.

The tests are in two submodules:

# `generated_code_execution`

These tests use valid API specs, and after running the generator, they _import and execute_ pieces of the generated code to verify that it actually works at runtime.

Each test class follows this pattern:

- Use the decorator `@with_generated_client_fixture`, providing an inline API spec (JSON or YAML) that contains whatever schemas/paths/etc. are relevant to this test class. 
  - The spec can omit the `openapi:`, `info:`, and `paths:`, blocks, unless those are relevant to the test.
  - The decorator creates a temporary file for the inline spec and a temporary directory for the generated code, and runs the client generator.
  - It creates a `GeneratedClientContext` object (defined in `end_to_end_test_helpers.py`) to keep track of things like the location of the generated code and the output of the generator command.
  - This object is injected into the test class as a fixture called `generated_client`, although most tests will not need to reference the fixture directly.
  - `sys.path` is temporarily changed, for the scope of this test class, to allow imports from the generated code.
- Use the decorator `@with_generated_code_imports` or `@with_generated_code_import` to make classes or functions from the generated code available to the tests.
  - `@with_generated_code_imports(".models.MyModel1", ".models.MyModel2)` would execute `from [package name].models import MyModel1, MyModel2` and inject the imported classes into the test class as fixtures called `MyModel1` and `MyModel2`.
  - `@with_generated_code_import(".api.my_operation.sync", alias="endpoint_method")` would execute `from [package name].api.my_operation import sync`, but the fixture would be named `endpoint_method`.
  - After the test class finishes, these imports are discarded.

Example:

```python
@with_generated_client_fixture(
"""
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

# `generator_failure_cases`

These run the generator with an invalid API spec and make assertions about the warning/error output. Some of these invalid conditions are expected to only produce warnings about the affected schemas, while others are expected to produce fatal errors that terminate the generator.

For warning conditions, each test class follows this pattern:

- Call `inline_spec_should_cause_warnings`, providing an inline API spec (JSON or YAML). If there are several test methods in the class using the same spec, use a fixture with scope "class" so the generator is only run once.
- Use `assert_bad_schema_warning` to parse the output and check for a specific warning message for a specific schema name.

Or, for fatal error conditions:

- Call `inline_spec_should_fail`, providing an inline API spec (JSON or YAML).
