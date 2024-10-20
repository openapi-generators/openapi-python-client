---
default: minor
---

# Add `literal_enums` config setting

Instead of the default `Enum` classes for enums, you can now generate `Literal` sets wherever `enum` appears in the OpenAPI spec by setting `literal_enums: true` in your config file.

```yaml
literal_enums: true
```

Thanks to @emosenkis for PR #1114 closes #587, #725, #1076, and probably many more. 
Thanks also to @eli-bl, @expobrain, @theorm, @chrisguillory, and anyone else who helped getting to this design!
