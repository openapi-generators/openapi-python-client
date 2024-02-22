---
default: patch
---

# Allow parameters with names differing only by case

If you have two parameters to an endpoint named `mixedCase` and `mixed_case`, previously, this was a conflict and the endpoint would not be generated.
Now, the generator will skip snake-casing the parameters and use the names as-is. Note that this means if neither of the parameters _was_ snake case, neither _will be_ in the generated code.

Fixes #922 reported by @macmoritz & @benedikt-bartscher.
