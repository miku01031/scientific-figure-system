# Safety boundaries

Edge-label clearance is deterministic and bounded. It may move a label within
the declared canvas but never changes node topology, scientific primitives, or
connector relationships. An explicitly locked label remains unchanged and a
collision becomes `REVIEW_REQUIRED`. Final exported SVG is re-gated for text,
raster, canvas and physical-size safety.
