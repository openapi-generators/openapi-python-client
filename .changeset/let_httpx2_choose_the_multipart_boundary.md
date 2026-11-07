---
default: patch
---

# Let httpx2 choose the boundary for `multipart/form-data` requests

Since 0.29.0, generated endpoints sent every `multipart/form-data` body with the fixed boundary `+++`, so an uploaded file containing `\r\n--+++` was cut short at that point (#1509). These bodies no longer set `Content-Type`, so httpx2 sets it with a random boundary for each request, as single-body endpoints did before 0.29.0. Endpoints with several body types still get a boundary (#947).
