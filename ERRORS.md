# Error codes and next actions

| Code | Meaning | Next action |
|---|---|---|
| `UNSUPPORTED_ARCHETYPE` | The requested data grammar is outside the three supported renderers. | Choose discrete, dense time series, or errorbar point-whisker; do not reinterpret the data silently. |
| `ENCODING_CAPACITY_EXCEEDED` | Unique color/marker/line encodings cannot represent all identities safely. | Split panels, reduce series, or provide a reviewed encoding profile. Colors are never recycled silently. |
| `INVALID_INTERVAL_ENDPOINTS` | An interval does not contain its estimate or has invalid endpoints. | Correct the frozen scientific input and provenance. |
| `CJK_FONT_UNAVAILABLE` | No configured CJK font can render the requested text. | Install/configure a CJK font or use Latin-only labels; output is stopped before final artwork. |
| `CAIROSVG_PYTHON_PACKAGE_MISSING` | The Python CairoSVG package is absent. | Install `requirements-publication.txt` if PDF/PNG publication output is required. |
| `NATIVE_CAIRO_MISSING` | CairoSVG is installed but the native Cairo library cannot load. | Install the platform Cairo library or configure `SCIFIG_RUNTIME_ROOT`; do not reinstall only the Python package. |
| `RUNTIME_CONFIG_INVALID` | A configured runtime root is missing or incomplete. | Correct the path or remove the override to use normal discovery. |
| `DRAWIO_APPLICATION_EXPORT_UNAVAILABLE` | draw.io Desktop is not available. | Native `.drawio` XML remains available; install/configure draw.io only for application export. |
| `SOURCE_SHA_MISMATCH` | A source file differs from its recorded provenance digest. | Restore the frozen source or regenerate the semantic mapping deliberately. |
