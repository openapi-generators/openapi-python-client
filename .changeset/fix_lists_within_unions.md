---
default: patch
---

# Fix lists within unions

Fixes #756 and #928. Arrays within unions (which, as of 0.17 includes nullable arrays) would generate invalid code.

Thanks @kgutwin and @diesieben07!
