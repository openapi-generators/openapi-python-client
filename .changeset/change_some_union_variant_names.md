---
default: major
---

# Change some union variant names

When creating a union with `oneOf`, `anyOf`, or a list of `type`, the name of each variant used to be `type_{index}`
where the index is based on the order of the types in the union.

This made some modules difficult to understand, what is a `my_type_type_0` after all?
It also meant that reordering union members, while not a breaking change to the API, _would_ be a breaking change 
for generated clients.

Now, if an individual variant has a `title` attribute, that `title` will be used in the name instead.
This is only an enhancement for documents which use `title` in union variants, and only a breaking change for 
_inline models_ (not `#/components/schemas` which should already have used more descriptive names).

Thanks @wallagib for PR #962!
