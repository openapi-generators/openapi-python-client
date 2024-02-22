---
default: patch
---

# Fix naming conflicts with properties in models with mixed casing

If you had an object with two properties, where the names differed only by case, conflicting properties would be generated in the model, which then failed the linting step (when using default config). For example, this:

```yaml
type: "object"
properties:
  MixedCase:
    type: "string"
  mixedCase:
    type: "string"
```

Would generate a class like this:

```python
class MyModel:
    mixed_case: str
    mixed_case: str
```

Now, neither of the properties will be forced into snake case, and the generated code will look like this:

```python
class MyModel:
    MixedCase: str
    mixedCase: str
```