# Safety and audit

Source files are read only. The caller provides a verified mapping. Validate source SHA immediately before and after drawing; hash each x/y/lower/upper float64 array and validity mask, preserve axis units/ranges and event/reference/invalid-region semantics. Compare Artist x/y, line segment endpoints and axis ranges with the spec. Scientific FAIL prevents final SVG/PDF/PNG export. Unsupported selection does not render.

SVG composition compares every path/use/clip/text/shape attribute fingerprint, scientific group subtree hashes and scientific ancestor transforms. Only outer viewport/physical metadata and verified external legend group translation are changed. Unknown or fingerprint-mismatched structures are skipped. No data primitive is shared from any reference paper. Outlined font glyphs remain vector primitives.

PASS/WARN/FAIL distinguish structure from layout. Layout overflow, marker proximity, annotation intersections and whitespace are warnings; no aesthetic conclusion follows. Missing glyphs, broken clipping, wrong size, unexpected raster and changed scientific DOM fail vector QA. Gray/CVD previews are approximate QA only. No color QA automatically changes artwork.

Limitations: source SHA does not establish semantic correctness; array mapping is explicitly authored and must be audited. Marker proximity is a conservative diameter proxy, not exact polygon occlusion. Annotation intersection is bounding-box based. Viewport overflow is measured from text and artwork bounds; no optical OCR/semantic image matching. Structurally valid vectors with layout WARN can technically pass under the declared protocol. Publish neither a 90% automation claim nor aesthetic approval from this alone.
