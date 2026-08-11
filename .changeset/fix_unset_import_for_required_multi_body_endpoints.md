---
default: patch
---

# Unset used but not imported for required multi-body endpoints

#1478 by @rolandgeider

Closes #1451 

We ran into this while generating a client from our spec. The multi-body branch of the `arguments` macro read `body_required` before it was ever assigned, so `| Unset = UNSET` was appended to the `body` annotation even for a required request body. 