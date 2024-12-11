---
default: minor
---

# Add discriminator property support

The optional `discriminator` field, when used in a schema with `anyOf` or `oneOf` as described in [OpenAPI 3.1.0](https://spec.openapis.org/oas/v3.1.0.html#discriminator-object), now correctly produces deserialization logic for using the specified property value to determine the appropriate type.

In this example, `PolymorphicModel.thing` will be deserialized as a `ThingA` if the value of the `modelType` property is `"ThingA"`, or as a `ThingB` if the value is `"ThingB"`:

```yaml
  ThingA:
    type: object
    properties:
      thingType:
        type: string
      name:
        type: string

  ThingB:
    type: object
    properties:
      thingType:
        type: string
      name:
        type: string

  PolymorphicModel:
    type: object
    properties:
      thing:
        anyOf:
          - "#/components/schemas/ThingA"
          - "#/components/schemas/ThingB"
        discriminator:
          propertyName: modelType
```

If you want to use property values that are not the same as the schema names, you can add a `mapping`. In this example, the value is expected to be `"A"` or `"B"`, instead of `"ThingA"` or `"ThingB"`:

```yaml
        discriminator:
          propertyName: modelType
          mapping:
            A: "#/components/schemas/ThingA"
            B: "#/components/schemas/ThingB"
```

This could also be written more concisely as:

```yaml
        discriminator:
          propertyName: modelType
          mapping:
            A: "ThingA"
            B: "ThingB"
```

If you specify a property name that does not exist in all of the variant schemas, the behavior is undefined.
