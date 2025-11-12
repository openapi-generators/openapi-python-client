---
default: patch
---

# Fix bad code generation

#1360 by @EricAtORS

This fixes:
- missing parenthesis in to_multipart
 #1338 #1318
- missing imports in the lazy eval in to_multipart:
#931 and #1051
