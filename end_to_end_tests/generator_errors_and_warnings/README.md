## The `generator_errors_and_warnings` module

These are end-to-end tests which run the code generator command with an invalid API spec and make assertions about the output. Some of these invalid conditions are expected to only produce warnings about the affected schemas, while others are expected to produce fatal errors that terminate the generator.

Unlike the tests in `generated_code_live_tests`, these do not import or execute the generated code, since the generator does not produce classes for invalid schemas.

For warning conditions, each test class follows this pattern:

- Call `inline_spec_should_cause_warnings`, providing an inline API spec (JSON or YAML). If there are several test methods in the class using the same spec, use a fixture with scope "class" so the generator is only run once.
- Use `assert_bad_schema_warning` to parse the output and check for a specific warning message for a specific schema name.

Or, for fatal error conditions:

- Call `inline_spec_should_fail`, providing an inline API spec (JSON or YAML).
