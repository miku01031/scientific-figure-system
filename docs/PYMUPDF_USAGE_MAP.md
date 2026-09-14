# PyMuPDF usage map

PyMuPDF is used for PDF inspection, not for scientific computation or the
core semantic model. The figure skill reads page size, embedded-image count,
and text/vector QA from an exported PDF. The schematic skill reads page text,
physical size, clipping and image counts during publication QA.

This is an **optional PDF QA capability**. SVG core rendering and native
`.drawio` XML generation do not require PyMuPDF. If it is unavailable, the
pipeline must report `PDF_QA_UNAVAILABLE` and withhold a publication PASS;
it must not invent a successful PDF inspection.
