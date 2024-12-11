---
default: patch
---

# Fix overriding of object property class

Fixed issue #1123, in which a property could end up with the wrong type when combining two object schemas with `allOf`, if the type of the property was itself an object but had a different schema in each. Example:

```yaml
  ModelA:
    properties:
      status:
        type: string
      result:
        - $ref: "#/components/schemas/BaseResult"

  ModelB:
    allOf:
      - $ref: "#/components/schemas/ModelA"
      - properties:
          result:
            - $ref: "#/components/schemas/ExtendedResult"

  ModelC:
    allOf:
      - $ref: "#/components/schemas/ModelA"
      - properties:
          result:
            - $ref: "#/components/schemas/UnrelatedResult"

  BaseResult:
    properties:
      prop1:
        type: string

  ExtendedResult:
    allOf:
      - $ref: "#/components/schemas/BaseResult"
      - properties:
          prop2:
            type: string

  UnrelatedResult:
    properties:
      prop3:
        type: string
```

Previously, in the generated classes for both `ModelB` and `ModelC`, the type of `result` was being incorrectly set to `BaseResult`.

The new behavior is, when computing `allOf: [A, B]` where `A` and `B` are both objects, any property `P` whose name exists in both schemas will have a schema equivalent to `allOf: [A.P, B.P]`. This is consistent with the basic definition of `allOf`.

When translating this into Python code, the generator will use a type that correctly describes the combined schema for the property. If the combined schema is exactly equal in shape to either `A.P` or `B.P` (implying that one was already derived from the other using `allOf`) then it will reuse the corresponding Python class. Otherwise it will create a new class, just as it would for an inline schema that used `allOf`. Therefore in the example above, the type of `ModelB.result` is `ExtendedResult`, but the type of `ModelC.result` is a new class called `ModelCResult` that includes all the properties from `BaseResult` and `UnrelatedResult`.
