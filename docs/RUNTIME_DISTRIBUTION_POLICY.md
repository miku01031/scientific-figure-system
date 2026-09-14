# Runtime distribution policy

The public candidate never vendors Cairo DLLs, a workstation Python runtime,
draw.io Desktop, or fonts. Install `requirements-core.txt` for SVG/native-XML
use. Install `requirements-publication.txt` plus the platform native Cairo
library for PDF/PNG publication export, and `requirements-pdfqa.txt` for PDF
inspection/QA. A user-managed isolated runtime may be selected with
`SCIFIG_RUNTIME_ROOT`; the code verifies module capabilities and a tiny SVG
conversion probe rather than trusting an absolute path identity.

`pip install CairoSVG` installs the Python wrapper only. It may still fail when
the native Cairo library is absent. On Windows use a maintained GTK/Cairo or
conda installation; on Debian/Ubuntu install the distribution `libcairo2`
package; on macOS install Cairo through Homebrew (`brew install cairo`). The
exact native setup is platform-managed and is intentionally not bundled.
