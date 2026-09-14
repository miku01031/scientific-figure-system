# Publication contract
Use an optional draw.io Desktop installation discovered from explicit configuration, environment, PATH, or standard OS install locations. Native .drawio generation does not require the application.
Only physical width/height metadata is normalized; viewBox, routing, text and geometry stay unchanged. PDF/PNG conversion requires a working CairoSVG/native-Cairo capability probe; it may be supplied by a user-managed runtime or normal installation. Publication width is 145 ±0.1 mm. SVG/PDF are publication outputs; semantic spec and .drawio are editable sources.

The optional Desktop export command uses a private temporary user-data
directory. Chromium sandbox flags are platform/application options, not part of
the native XML contract; enable application export only for trusted generated
documents and record the discovered draw.io version.
QA records text bbox intersections, proper connector crossings, arrow tips in unrelated blocks, outside text, missing text/glyph sentinels, raster/foreignObject counts and native structure preservation. These geometric checks are conservative screening, not complete visual proof; collinear overlaps and all font shaping cases require visual review. Move-node follow is separately tested against application SVG endpoints.
