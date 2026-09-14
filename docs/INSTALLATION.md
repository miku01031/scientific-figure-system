# Installation

1. Create a virtual environment.
2. Install `requirements-core.txt` for SVG/native-XML use. Install
   `requirements-dev.txt` only when running the test suite.
3. Copy `skills/scientific-figure` and `skills/scientific-schematic` into the
   local project or skill directory.

The figure core can render SVG without native Cairo. PDF/PNG publication
conversion is a separate capability: install `requirements-publication.txt`,
which adds CairoSVG, and install the platform native Cairo library. For PDF
inspection/QA, install `requirements-pdfqa.txt`, which adds PyMuPDF. On
Windows use a maintained GTK/Cairo or conda runtime; on Debian/Ubuntu install
`libcairo2`; on macOS install Cairo with Homebrew. A Python CairoSVG import
alone does not prove native Cairo is loadable.

For an isolated user-managed runtime set `SCIFIG_RUNTIME_ROOT`. The runtime
must expose its Python modules and, on Windows, a `native` directory; the code
prepends that directory to the process DLL search path and runs a conversion
probe. Invalid configurations report `RUNTIME_CONFIG_INVALID`.

draw.io Desktop is optional. Set `DRAWIO_EXECUTABLE` for application SVG/PDF
export. Without it, schematic native XML generation still works and the result
records application export as unavailable. The tested local version was 31.4.5;
no minimum version is claimed.
