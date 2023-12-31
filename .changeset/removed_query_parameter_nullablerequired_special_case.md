---
default: major
---

# Removed query parameter nullable/required special case

In previous versions, setting _either_ `nullable: true` or `required: false` on a query parameter would act like both were set, resulting in a type signature like `Union[None, Unset, YourType]`. This special case has been removed, query parameters will now act like all other types of parameters.
