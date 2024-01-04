---
default: minor
---

# Generate properties for some boolean enums

If a schema has both `type = "boolean"` and `enum` defined, a normal boolean property will now be created. 
Previously, the generator would error. 

Note that the generate code _will not_ correctly limit the values to the enum values. To work around this, use the 
OpenAPI 3.1 `const` instead of `enum` to generate Python `Literal` types.

Thanks for reporting #922 @macmoritz!
