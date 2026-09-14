# Scientific Figure System (public candidate)

Public repository version: **0.1.0-rc1**. The two internal product identities
remain scientific-figure 1.1.x and scientific-schematic 0.1.x.

## What is this?
A small, evidence-preserving toolkit for reproducible scientific figures and
semantic schematics. It uses explicit inputs, vector-first output, provenance
checks, and fail-closed validation.

## What is it not?
It is not a paper-production service, a universal chart library, or a guarantee
of journal acceptance. Synthetic examples are demonstrations only; authors must
review scientific meaning and visual suitability.

## Why integrity matters
Scientific arrays, intervals, labels, provenance, and topology are checked
before artwork is accepted. Unsupported or ambiguous inputs stop with an
explicit error. Machine QA does not establish journal likeness.

## Supported products
- **scientific-figure**: discrete comparison, dense time series, and errorbar
  point-whisker figures.
- **scientific-schematic**: nine registered semantic grammars and native
  editable draw.io XML. Nodes, topology, and layout coordinates are supplied
  by the semantic spec; this is not automatic intelligent layout. Application
  export is optional and was tested with draw.io Desktop 31.4.5 only.

## Quick start — figure
From the repository root:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements-core.txt
.venv\Scripts\python examples/synthetic/figure_minimal/run_example.py
```

The deterministic synthetic example writes an SVG under
`examples/synthetic/figure_minimal/output/`. This core quick start does not
install optional publication or PDF-QA packages.

## Quick start — schematic
Native editable XML needs no draw.io installation:

```powershell
.venv\Scripts\python examples/synthetic/schematic_minimal/run_example.py
```

This writes `examples/synthetic/schematic_minimal/output/diagram.drawio`.
Set `DRAWIO_EXECUTABLE` only when application export is wanted. Without the
application the native XML result remains valid and export is reported as
unavailable.

## Optional capabilities

For PDF/PNG publication export, install `requirements-publication.txt` and a
platform-native Cairo library. For PDF inspection or QA, install
`requirements-pdfqa.txt`. `pip install CairoSVG` provides the Python wrapper;
it does not guarantee that native Cairo is available. draw.io Desktop is an
optional application capability and is never required for native `.drawio`
generation.

## Install manually
Copy the two directories under `skills/` into a local project or skill
directory. Core SVG/native-XML use requires `requirements-core.txt`; tests use
`requirements-dev.txt`; publication and PDF-QA are separate optional layers.
No package or desktop application is installed automatically. For Cairo
details see `docs/INSTALLATION.md` and `docs/RUNTIME_DISTRIBUTION_POLICY.md`.

## Unsupported behavior
Unknown archetypes/grammars, insufficient encoding capacity, invalid intervals,
missing provenance, missing glyphs, unavailable required fonts, and forbidden
raster/vector conditions fail closed with a code and next action. Chart registry
entries outside the three data archetypes are reference/advisor records, not
production support claims. Optional PDF/PNG, CJK-font, and draw.io integration
tests skip explicitly when their capability is absent.

## Editing draw.io
The `.drawio` file is the editable schematic source. Open it in diagrams.net or
draw.io, edit native cells/connectors, then export publication artwork through
the documented path.
