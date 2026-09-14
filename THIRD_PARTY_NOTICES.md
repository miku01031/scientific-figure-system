# Third-party notices

The public candidate declares these packages; no package source, native runtime,
font, or draw.io application is vendored.

| Component | Role | License identity / source |
|---|---|---|
| NumPy | core array checks and numeric helpers (`requirements-core.txt`) | BSD-3-Clause — https://numpy.org/doc/stable/license.html |
| Matplotlib | core figure rendering (`requirements-core.txt`) | Matplotlib License (PSF-compatible) — https://matplotlib.org/stable/project/license.html |
| Pillow | core PNG metadata and inspection (`requirements-core.txt`) | Pillow license — https://github.com/python-pillow/Pillow/blob/main/LICENSE |
| jsonschema | core semantic schema validation (`requirements-core.txt`) | MIT — https://github.com/python-jsonschema/jsonschema/blob/main/COPYING |
| PyYAML | core registry/config parsing (`requirements-core.txt`) | MIT — https://github.com/yaml/pyyaml/blob/main/LICENSE |
| CairoSVG | optional SVG-to-PDF/PNG conversion (`requirements-publication.txt`) | LGPL-3.0-or-later — https://cairosvg.org/documentation/ |
| cairocffi | transitive Cairo binding used by CairoSVG | BSD-3-Clause — https://github.com/Kozea/cairocffi/blob/master/LICENSE |
| PyMuPDF | optional PDF QA/inspection (`requirements-pdfqa.txt`) | AGPL-3.0-or-later or Artifex commercial license — https://pymupdf.readthedocs.io/en/latest/about.html#licensing |
| draw.io Desktop | optional user-installed application export | no draw.io code is vendored; project reference: https://github.com/jgraph/drawio |

The bundled `our_moderate_vivid` categorical table is project-owned for this
candidate. Other palette schemes studied internally are not redistributed here;
users supplying their own values are responsible for provenance and license
review. A final project license is pending author decision.
